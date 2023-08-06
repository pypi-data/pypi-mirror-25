import os, shutil, tempfile, urllib, requests

from datetime import datetime

from cairosvg import svg2png

from lxml import html as lxml_html

NHL_URL = 'https://www.nhl.com/'
CSS_FILE = 'nhl-logos.css'
SUPPORTED_EXTS = ['svg', 'png']
DATE_NOW_FORMAT = '%Y-%m-%d_%H-%M-%S'

def create_png_from_svg(svg):
    """Creates a bytes object representing a png image"""
    image_bytearray = bytearray(svg, 'utf8')
    return svg2png(bytestring=image_bytearray);

def create_svg_from_svg(svg):
    """Creates a string representing an svg path"""
    # This exists to accomodate testing and future updates
    return svg;

def retrieve_stylesheet():
    """Pulls down nhl.com then retrieves and parses the stylesheet"""
    # Think about caching the stylesheet
    response = requests.get(NHL_URL)
    markup = lxml_html.fromstring(response.content)
    header_links = markup.head.cssselect('link')

    for item in header_links:
        href = item.get('href')[2:]
        if CSS_FILE in href:
            break

    css_response = requests.get('https://' + href)

    return css_response.content

def get_attrs_from_rule(rule):
    """Take a CSS rule and grab attributes for the svg (team, category, etc)"""
    selector = rule.selectorText.split()[-1]
    chunks = selector.split('--')

    # chunks[0] => .logo-bg, .logo-bg-dark, .logo-bg-alt
    logo_attr = chunks[0][9:] # dark, secondary, alt, or (blank)

    # chunks[1] => team-nyr, team-cgy, network-nbc, league-nhl-com
    logo_identifier = chunks[1].split('-', 1) # split at first occurrence
    logo_type = logo_identifier[0] # team, league, network
    logo_name = logo_identifier[1] # nyr, cgy, nbc, nhl-com
    # add attribute to the logo_name, if exists
    if len(logo_attr) >= 1:
        logo_name = logo_name + '-' + logo_attr

    for property in rule.style:
        if 'background-image' in property.name:
            # the [:-2] removes the trailing ")
            logo_svg = property.value.split(',', 1)[1][:-2]

    return {
        'selector': selector,
        'logo_attr': logo_attr,
        'logo_type': logo_type,
        'logo_name': logo_name,
        'svg': urllib.parse.unquote(logo_svg),
        'filename': logo_name,
        'dir': logo_type,
    }

def delete_image_category(path, category=[]):
    """Deletes a category or all categories if none are specified"""

    if len(category) == 0:
        for _, dirnames, filenames in os.walk(path):
            for subdir in dirnames:
                shutil.rmtree(path + '/' + subdir)
            break
    else:
        for category_dir in category:
            print('path=%r' % path)
            print('category_dir=%r' % category_dir)
            shutil.rmtree(path + '/' + category_dir)

def archive_images(path, dest, filename_prepend=''):
    """Archives all of the images that have been downloaded"""
    archive_filename = datetime.now().strftime(DATE_NOW_FORMAT)
    print('filename_prepend=%s' % filename_prepend)
    if len(filename_prepend) > 0:
        archive_filename = filename_prepend + '_' + archive_filename

    try:
        for _, dirnames, filenames in os.walk(path):
            if len(dirnames) > 0:
                tmp_storage = tempfile.mkdtemp()

            for subdir in dirnames:
                shutil.copytree(path + '/' + subdir, tmp_storage + '/' + subdir)

            tmp_archive_file = shutil.make_archive(archive_filename, 'zip', tmp_storage)
            archive_file = shutil.move(tmp_archive_file, dest)

            break # break first level dirs
    finally:
        shutil.rmtree(tmp_storage)

    return archive_file

def delete_archive(path):
    """Delete all archives"""
    for sub in os.listdir(path):
        if sub.endswith('.zip'):
            os.remove(path + '/' + sub)

def write_image_to_file(logo_attrs, file_types, dest):
    """Writes a logo to the local file system"""
    dir_path = dest + '/' + logo_attrs.get('dir')
    filepaths = []

    for extension in file_types:
        if extension not in SUPPORTED_EXTS:
            continue

        file = logo_attrs.get('filename') + '.' + extension
        write_mode = 'w+'

        if extension == 'png':
            write_mode = 'wb+' # adjust write mode to binary
            object_to_write = create_png_from_svg(logo_attrs.get('svg'))
        else: #default to SVG
            object_to_write = create_svg_from_svg(logo_attrs.get('svg'))

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(dir_path + '/' + file, write_mode) as active_file:
            active_file.write(object_to_write)
            filepaths.append(dir_path + '/' + file)

    return filepaths
