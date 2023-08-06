"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from pdown import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=pdown', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'pdown',
    version = __version__,
    description = 'A command line program to download/manipulate periscope data', 
    long_description = long_description,
    author = 'Stephen Cockerill',
    author_email = 'scockerill@luciddg.com',
    license = 'UNLICENSE',
    classifiers = [
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'pdown=pdown.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
