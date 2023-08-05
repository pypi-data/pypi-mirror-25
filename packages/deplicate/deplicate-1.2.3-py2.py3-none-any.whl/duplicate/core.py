# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from collections import defaultdict
from contextlib import closing
from filecmp import cmp as filecmp
from math import ceil
from multiprocessing.pool import ThreadPool
from os.path import abspath
from stat import S_IFMT, S_ISLNK

import xxhash

from .structs import Cache, DupInfo, FileInfo, FilterType, SkipException
from .utils.fs import (blksize, checksum, fsdecode, is_archived, is_hidden,
                       is_os64, is_system, remove, sidesum, signature,
                       splitpaths, walk)


_xxhash_xxh = xxhash.xxh64 if is_os64 else xxhash.xxh32

_LINKSIZE = 900 if os.name == 'nt' else 60  #: bytes
_LITTLESIZE = 100 << 10  #: bytes
_BIGSIZE = 100 << 20  #: bytes
_SIZERATE = 10  #: percentage
_BLKSIZE = 4 << 10
_XXHSIZE = _xxhash_xxh().block_size << 11

CACHE = Cache()


def _iterdups(dupinfo):
    for key, value in dupinfo.dups.items():
        if isinstance(value, DupInfo):
            for subobj, subkey, subvalue in _iterdups(value):
                yield subobj, subkey, subvalue
        else:
            yield dupinfo, key, value


def _bufsize(fileinfo):
    # NOTE: `stat.st_dev` is always zero in Python 2 under Windows. :(
    if fileinfo.dev:
        try:
            blocksize = CACHE.get(fileinfo).blksize

        except Exception:
            blocksize = 1
    else:
        blocksize = blksize(fileinfo.path)

    maxsize = max(blocksize, _XXHSIZE)
    minsize = min(blocksize, _XXHSIZE)
    return maxsize - maxsize % minsize


def _checksum(fileinfo):
    try:
        if S_ISLNK(fileinfo.mode):
            link = os.readlink(fileinfo.path)
            hashsum = _xxhash_xxh(link).hexdigest()
        else:
            raise AttributeError

    except AttributeError:
        bufsize = _bufsize(fileinfo)
        hashsum = checksum(fileinfo.path, bufsize)

    return hashsum


def _chksize(fileinfo):
    rate = _SIZERATE
    blocksize = _BLKSIZE
    percsize = int(ceil(fileinfo.size / 100.0 * rate))
    if blocksize < percsize:
        percsize -= percsize % blocksize
    return percsize // 2


def _sidesum(fileinfo):
    chksize = _chksize(fileinfo)
    bufsize = _bufsize(fileinfo)
    hashsums = sidesum(fileinfo.path, chksize, bufsize)
    return hashsums


def _signature(fileinfo):
    return signature(fileinfo.path)


def _filter(func, filelist, dupdict, errlist, onerror):
    for fileinfo in filelist:
        try:
            idkey = func(fileinfo)

        except SkipException:
            pass

        except Exception as exc:
            if onerror is not None:
                onerror(exc, fileinfo.path)
            errlist.append(fileinfo)

        else:
            dupdict[idkey].append(fileinfo)

    return dupdict, errlist


def _rulefilter(fltrtype, dupinfo, check, rule, onerror, progress):
    dups_it = _iterdups(dupinfo)

    for dupobj, dupkey, filelist in dups_it:
        try:
            check(filelist)

        except SkipException:
            continue

        dupdict, errlist = _filter(rule, filelist, defaultdict(list), [],
                                   onerror)

        DupInfo(fltrtype, dupdict, errlist, dupobj, dupkey)

        if progress is not None:
            progress(len(filelist))


def _binarycmp(filelist, onerror):
    file0, file1 = filelist

    try:
        if filecmp(file0.path, file1.path, shallow=False):
            dupdict = {True: filelist}
        else:
            dupdict = {}
        errlist = []

    except (IOError, OSError) as exc:
        if onerror is not None:
            onerror(exc, abspath(exc.filename))
        dupdict = {}
        errlist = filelist

    return dupdict, errlist


def _binaryfilter(fltrtype, dupinfo, onerror, progress):
    dups_it = _iterdups(dupinfo)

    for dupobj, dupkey, filelist in dups_it:
        try:
            file0, _ = filelist
        except ValueError:
            continue

        # NOTE: This check can return true one time only; should be optimized?
        if not file0.size:
            continue

        dupdict, errlist = _binarycmp(filelist, onerror)

        DupInfo(fltrtype, dupdict, errlist, dupobj, dupkey)

        if progress is not None:
            progress(2)


def _typefilter(fltrtype, dupinfo, onerror, progress):
    dups_it = _iterdups(dupinfo)

    for dupobj, dupkey, filelist in dups_it:
        dupdict, errlist = _filter(lambda f: f[fltrtype], filelist,
                                   defaultdict(list), [], onerror)

        DupInfo(fltrtype, dupdict, errlist, dupobj, dupkey)

        if progress is not None:
            progress(len(filelist))


def _signcheck(filelist):
    # if len(filelist) < 2:
        # raise SkipException

    file0 = filelist[0]

    if not file0.size or _LINKSIZE < file0.size < _LITTLESIZE:
        raise SkipException

    elif S_ISLNK(file0.mode):
        raise SkipException


def _sidecheck(filelist):
    # if len(filelist) < 2:
        # raise SkipException

    file0 = filelist[0]

    if file0.size < _BIGSIZE:
        raise SkipException

    elif S_ISLNK(file0.mode):
        raise SkipException


def _hashcheck(filelist):
    if len(filelist) < 3:
        raise SkipException

    elif not filelist[0].size:
        raise SkipException


def _sizecheck(size, minsize, maxsize, scanempties):
    if not size and not scanempties:
        raise SkipException

    elif not minsize <= size <= maxsize:
        raise SkipException


def _rulecheck(path, included_match, excluded_match):
    if excluded_match(path):
        raise SkipException

    elif not included_match(path):
        raise SkipException


def _attrcheck(path, scansystem, scanarchived, scanhidden):
    if not scanhidden and is_hidden(path):
        raise SkipException

    elif not scanarchived and is_archived(path):
        raise SkipException

    elif not scansystem and is_system(path):
        raise SkipException


def _filecheck(fileinfo, minsize, maxsize, included_match, excluded_match,
               scanempties, scansystem, scanarchived, scanhidden):

    _sizecheck(fileinfo.size, minsize, maxsize, scanempties)
    _rulecheck(fileinfo.path, included_match, excluded_match)
    _attrcheck(fileinfo.path, scansystem, scanarchived, scanhidden)

    return S_IFMT(fileinfo.mode), fileinfo.size


def _splitpaths(paths, followlinks):
    with closing(ThreadPool()) as pool:
        upaths = pool.imap(fsdecode, paths)
    return splitpaths(set(upaths), followlinks)


def _names_to_info(names, onerror):
    filelist = []
    errlist = []

    for filename in names:
        try:
            fileinfo = FileInfo(filename)

        except (IOError, OSError) as exc:
            filepath = abspath(filename)
            if onerror is not None:
                onerror(exc, filepath)
            errlist.append(filepath)

        else:
            filelist.append(fileinfo)

    return filelist, errlist


def _entries_to_info(entries, onerror):
    filelist = []
    errlist = []

    for entry in entries:
        try:
            st = entry.stat(follow_symlinks=False)
            fileinfo = FileInfo(entry.name, entry.path, st)

        except (IOError, OSError) as exc:
            if onerror is not None:
                onerror(exc, entry.path)
            errlist.append(entry.path)

        else:
            filelist.append(fileinfo)

    return filelist, errlist


def _filescan(filenames, dupdict, errlist, scnerrlist,
              scnargs, onerror, progress):

    filelist, _scnerrlist = _names_to_info(filenames, onerror)
    scnerrlist.extend(_scnerrlist)

    def rule(fileinfo):
        return _filecheck(fileinfo, *scnargs)

    _filter(rule, filelist, dupdict, errlist, onerror)

    if progress is not None:
        progress(len(filelist))

    return dupdict, errlist, scnerrlist


def _dirscan(dirnames, dupdict, errlist, scnerrlist,
             scnargs, onerror, followlinks, scanlinks, progress):

    if onerror is None:
        def callback(exc):
            scnerrlist.append(abspath(exc.filename))
    else:
        def callback(exc):
            filepath = abspath(exc.filename)
            onerror(exc, filepath)
            scnerrlist.append(filepath)

    def rule(fileinfo):
        return _filecheck(fileinfo, *scnargs)

    seen = set()
    for dirname in dirnames:
        walk_it = walk(dirname, callback, followlinks, seen)

        for _, files, links in walk_it:
            if scanlinks:
                files += links

            filelist, _scnerrlist = _entries_to_info(files, onerror)
            scnerrlist.extend(_scnerrlist)

            _filter(rule, filelist, dupdict, errlist, onerror)

            if progress is not None:
                progress(len(filelist))

    return dupdict, errlist, scnerrlist


def filterdups(fltrtype, dupinfo, onerror, progress):

    # progress(0)

    if fltrtype is FilterType.SIGNATURE:
        _rulefilter(fltrtype, dupinfo, _signcheck, _signature, onerror,
                    progress)

    elif fltrtype is FilterType.RULE:
        # NOTE: Just a one-pass check for now...
        _rulefilter(fltrtype, dupinfo, _sidecheck, _sidesum, onerror, progress)

    elif fltrtype is FilterType.HASH:
        _rulefilter(fltrtype, dupinfo, _hashcheck, _checksum, onerror,
                    progress)

    elif fltrtype is FilterType.BINARY:
        _binaryfilter(fltrtype, dupinfo, onerror, progress)

    else:
        _typefilter(fltrtype, dupinfo, onerror, progress)

    return dupinfo


def _filepurge(filepath, duplist, errlist, trash, onerror):
    try:
        remove(filepath, trash)

    except Exception as exc:
        if onerror is not None:
            onerror(exc, filepath)
        errlist.append(filepath)

    else:
        duplist.append(filepath)


def _purge(filelist, duplist, errlist, trash, ondel, onerror):
    if ondel:
        for fileinfo in filelist:
            filepath = fileinfo.path

            try:
                ondel(filepath)
            except SkipException:
                continue

            _filepurge(filepath, duplist, errlist, trash, onerror)
    else:
        for fileinfo in filelist:
            _filepurge(fileinfo.path, duplist, errlist, trash, onerror)

    return duplist, errlist


def purgedups(dupinfo, trash, ondel, onerror, progress):

    # progress(0)

    delduplist = []
    delerrlist = []

    # NOTE: Keep the oldest of firsts
    def sort_fn(obj):
        return obj.index, -obj.mtime, obj.path

    dups_it = _iterdups(dupinfo)

    for _, _, filelist in dups_it:
        duplist = sorted(filelist, key=sort_fn)[1:]

        _purge(duplist, delduplist, delerrlist, trash, ondel, onerror)

        if progress is not None:
            progress(len(filelist))

    return delduplist, delerrlist


def scandups(paths, sizes, matchers, recursive, followlinks, scanlinks, flags,
             onerror, progress):

    # progress(0)

    dupdict = defaultdict(list)
    errlist = []
    scnerrlist = []

    scnargs = sizes + matchers + flags

    splitted_paths = _splitpaths(paths, followlinks)
    dirnames, filenames, linknames, _, errnames = splitted_paths

    scnerrlist.extend(errnames)

    if scanlinks:
        filenames += linknames

    _filescan(filenames, dupdict, errlist, scnerrlist, scnargs, onerror,
              progress)

    if recursive:
        _dirscan(dirnames, dupdict, errlist, scnerrlist, scnargs, onerror,
                 followlinks, scanlinks, progress)

    dupinfo = DupInfo(FilterType.ID, dupdict, errlist)

    return dupinfo, scnerrlist
