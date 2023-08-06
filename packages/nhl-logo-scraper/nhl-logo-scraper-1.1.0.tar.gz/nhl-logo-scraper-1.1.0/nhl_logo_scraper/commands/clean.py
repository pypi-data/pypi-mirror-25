"""The clean command"""

import logging

from .base import Base

from nhl_logo_scraper.utils import delete_archive, delete_image_category

class Clean(Base):
    """Clean the output directory"""

    def run(self):
        logging.info('Cleaning up')
        image_location = self.options['--dir']

        if self.options['--full'] == True:
            # add warning
            logging.debug('Doing a full clean')
            delete_archive(image_location)

        if self.options['--category'] == '*':
            logging.info('Deleting all images')
            # request confirmation that they want to delete everything
            delete_image_category(image_location)
        else:
            categories = self.options['--category'].split(',')

            logging.info('Deleting %r', categories)
            delete_image_category(image_location, categories)
