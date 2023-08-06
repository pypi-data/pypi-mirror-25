"""The clean command"""

from .base import Base
from nhl_logo_scraper.utils import delete_archive, delete_image_category

class Clean(Base):
    """Clean the output directory"""

    def run(self):
        image_location = self.options['--dir']

        if self.options['--full'] == True:
            # add warning
            delete_archive(image_location)

        if self.options['--category'] == '*':
            # request confirmation that they want to delete everything
            delete_image_category(image_location)
        else:
            print(self.options['--category'])
            delete_image_category(image_location, self.options['--category'].split(','))
