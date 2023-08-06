"""
nhlscraper

Usage:
    nhlscraper scrape [--output=DIR] [--format EXTENSIONS] [--archive] [--debug]
    nhlscraper clean [--dir=DIR] [--category CATEGORIES] [--full] [--debug]
    nhlscraper -h | --help
    nhlscraper --version

Options:
    --output=DIR            The directory to dump all of the files [default: ./output]
    --format EXTENSIONS     Image output formats (svg and/or png) [default: svg]
    --archive               Archive any previous logos that were downloaded [default: True]
    --dir=DIR               The directory that the files live in [default: ./output]
    --category CATEGORIES   Categories to remove all files (league, network, team) [default: *]
    --full                  Clean all files created by this tool (includes archives)
    --debug                 Allow debugging logs through
    -h --help               Show this screen
    -V --version            Show version

Examples:
    nhlscraper scrape --format svg,png

Help:
    For help using this tool, please search or open an issue at: https://github.com/blindman/nhl-logo-scraper
"""

import logging

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""

    import nhl_logo_scraper.commands
    options = docopt(__doc__, version=VERSION)
    log_level = logging.INFO

    if options['--debug'] is True:
        log_level = logging.DEBUG

    logging.basicConfig(format='[%(levelname)s]: %(message)s', level=log_level)

    # Parse and loop the CLI options
    for k, v in options.items():
        if hasattr(nhl_logo_scraper.commands, k) and v:
            # Determine if module matches an option
            module = getattr(nhl_logo_scraper.commands, k)
            nhl_logo_scraper.commands = getmembers(module, isclass)
            # Determine the name of the command class
            command = [command[1] for command in nhl_logo_scraper.commands if command[0] != 'Base'][0]
            # Create instance of command class
            command = command(options)
            # Run the command
            command.run()
