"""The scrape command."""

import cssutils

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
        img_types = []
        destination = self.options['--output']

        if self.options['--archive'] is True:
            archive_images(destination, destination)

        # filter out extensions that are not supported
        for ext in self.options['--format'].split(','):
            if ext.lower() in SUPPORTED_EXTS:
                img_types.append(ext.lower())
            else:
                print('Unsupported image type: ' + ext)

        if len(img_types) < 1:
            print('None of the provided image types are supported.\nOnly svg and png formats are currently supported.')

        sheet = retrieve_stylesheet()
        parsed_sheet = cssutils.parseString(sheet)

        for rule in parsed_sheet:
            logo_attrs = get_attrs_from_rule(rule)
            write_image_to_file(logo_attrs, img_types, destination)
