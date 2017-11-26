from setuptools import setup, find_packages
from codecs import open
import os


# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# Package version
version = '1.0.0'


setup(
    name = 'piano_fingering',
    version = version,

    description = 'Automatic fingering for notes played on piano',
    long_description = long_description,

    url = 'https://github.com/Kanma/piano_fingering',
    download_url = 'https://github.com/Kanma/piano_fingering/archive/v%s.tar.gz' % version,

    author = 'Philip Abbet',
    author_email = 'philip.abbet@gmail.com',

    license='MIT',

    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia',
        'Intended Audience :: Developers',
    ],

    keywords = ['piano', 'music'],

    packages = [
        'piano_fingering',
        'piano_fingering.test',
    ],

    install_requires = [],
    extras_require={},

    test_suite = 'piano_fingering.test',
)
