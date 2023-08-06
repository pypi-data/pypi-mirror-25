"""The scrape command."""

import logging, cssutils

from .base import Base
from nhl_logo_scraper.utils import (
    SUPPORTED_EXTS,
    archive_images,
    retrieve_stylesheet,
    get_attrs_from_rule,
    write_image_to_file,
)

class Scrape(Base):
    """Scrape the images from nhl.com."""

    def run(self):
        logging.info('Scraping images from nhl.com')
        img_types = []
        destination = self.options['--output']

        if self.options['--archive'] is True:
            logging.debug('Archiving old images')
            archive_images(destination, destination)

        # filter out extensions that are not supported
        for ext in self.options['--format'].split(','):
            if ext.lower() in SUPPORTED_EXTS:
                img_types.append(ext.lower())
            else:
                logging.warn('Unsupported image type: %s', ext)

        if len(img_types) < 1:
            logging.error('None of the provided image types are supported.')
            return

        logging.info('Retrieving and parsing stylesheet from nhl.com')
        sheet = retrieve_stylesheet()
        parsed_sheet = cssutils.parseString(sheet)

        logging.info('Parsing rules')
        for rule in parsed_sheet:
            logo_attrs = get_attrs_from_rule(rule)
            write_image_to_file(logo_attrs, img_types, destination)

        logging.info('Finished parsing, files located at %s', destination)
