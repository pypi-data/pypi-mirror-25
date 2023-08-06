#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='agnostic-file-store',
    packages = ['afs'],
    version = '0.2',
    description = 'An agnostic, easy-to-use module for different file systems'
                  ' (At present just local an SMB)',
    author = 'Juan Ignacio Rodríguez de León',
    author_email = 'euribates@gmail.com',
    url = 'https://bitbucket.org/euribaes/agnostic-file-store/',
    download_url = 'https://bitbucket.org/euribates/agnostic-file-store/get/04ce6edb7264.zip',
    keywords = ['agnostic', 'SAN', 'NAS', 'Samba', 'SMB', 'CIFS'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Communications :: File Sharing',
        'Topic :: System :: Filesystems',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    )
