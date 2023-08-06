"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from nhl_logo_scraper import __version__


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
        """Run all tests."""
        errno = call(['py.test', '--cov=nhl_logo_scraper'])
        raise SystemExit(errno)


setup(
    name = 'nhl-logo-scraper',
    version = __version__,
    description = 'Scrape logos for all NHL teams',
    long_description = long_description,
    url = 'https://github.com/blindman/nhl-logo-scraper',
    author = 'Jon Heller',
    author_email = 'jon.heller02@gmail.com',
    license = 'MIT',
    classifiers = [
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'requests', 'lxml', 'cssselect', 'cssutils', 'cairosvg'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov', 'codecov'],
    },
    entry_points = {
        'console_scripts': [
            'nhlscraper=nhl_logo_scraper.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
