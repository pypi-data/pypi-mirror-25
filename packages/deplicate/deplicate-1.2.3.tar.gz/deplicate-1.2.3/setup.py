# -*- coding: utf-8 -*-

from __future__ import absolute_import

import codecs

from setuptools import setup

setup(
    name='deplicate',
    version=codecs.open('VERSION').read().strip(),
    description='Advanced Duplicate File Finder for Python. '
                'Nothing is impossible to solve.',
    long_description=codecs.open(
        'README.rst', encoding='utf-8', errors='ignore').read(),
    keywords='duplicate duplicatefinder duplicates dups',
    url='https://github.com/deplicate/deplicate',
    download_url='https://github.com/deplicate/deplicate/releases',
    author='Walter Purcaro',
    author_email='vuolter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities'],
    platforms=['any'],
    packages=['duplicate'],
    include_package_data=True,
    install_requires=[
        'directio;os_name!="nt"',
        'enum34;python_version<"3.4"',
        'psutil',
        'pyobjc;sys_platform=="darwin"',
        'pypiwin32>=154;os_name=="nt"',
        'scandir;python_version<"3.5"',
        'send2trash',
        # 'ssd',
        'xxhash>=1'],
    setup_requires=['setuptools>=20.8.1'],
    extras_require={'cli': ['deplicate-cli'], 'full': ['deplicate-cli']},
    python_requires='>=2.6,!=3.0,!=3.1,!=3.2',
    zip_safe=True)
