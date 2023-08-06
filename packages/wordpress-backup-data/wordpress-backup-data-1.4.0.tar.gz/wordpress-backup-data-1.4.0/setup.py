#!/usr/bin/env python

from setuptools import setup
from os.path import dirname, abspath, join
from codecs import open

DIR = dirname(abspath(__file__))
VERSION = '1.4.0'

with open(join(DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'wordpress-backup-data',
    version = VERSION,
    description = 'Back up your WordPress data',
    long_description = long_description,
    license = 'GPLv3',
    keywords = 'wordpress backup',
    author = 'Paul-Emmanuel Raoul',
    author_email = 'skyper@skyplabs.net',
    url = 'https://github.com/SkypLabs/wordpress-backup-data',
    download_url = 'https://github.com/SkypLabs/wordpress-backup-data/archive/v{0}.zip'.format(VERSION),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    scripts = ['wp-backup-data'],
    install_requires = ['mechanize>=0.2.5'],
)
