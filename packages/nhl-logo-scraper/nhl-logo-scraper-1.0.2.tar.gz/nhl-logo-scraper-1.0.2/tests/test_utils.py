"""Tests for the `nhlscraper.scrape` subcommand"""

import os, tempfile, shutil, logging, cssutils

from datetime import datetime

from subprocess import PIPE, getoutput

from unittest import TestCase

from nhl_logo_scraper.utils import (
    DATE_NOW_FORMAT,
    SUPPORTED_EXTS,
    create_png_from_svg,
    create_svg_from_svg,
    retrieve_stylesheet,
    get_attrs_from_rule,
    delete_image_category,
    archive_images,
    delete_archive,
    write_image_to_file,
)

svg_example = '<svg xmlns="http://www.w3.org/2000/svg" id="Layer_2" width="253" height="62" viewBox="0 0 253 62"></svg>'

class TestUtils(TestCase):
    def test_returns_png(self):
        output = create_png_from_svg(svg_example)
        self.assertTrue(isinstance(output, (bytes,)))

    def test_returns_svg(self):
        output = create_svg_from_svg(svg_example)
        self.assertTrue(output == svg_example)
        self.assertTrue(isinstance(output, (str)))
        self.assertTrue('</svg>' in output)

    def test_retrieves_stylesheet(self):
        output = retrieve_stylesheet()
        self.assertTrue(isinstance(output, (bytes,)))

    def test_retrieves_attrs_from_rule(self):
        svg_team_encoded_example = cssutils.parseString('.logo-bg--team-1,.logo-bg-dark--team-njd {background-image: url(data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2016%22%3E%3C%2Fsvg%3E)}')
        svg_network_encoded_example = cssutils.parseString('.logo-bg--team-4,.logo-bg-dark--network-cbc {background-image: url(data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2016%22%3E%3C%2Fsvg%3E)}')
        svg_league_encoded_example = cssutils.parseString('.logo-bg--league-nhl {background-image: url(data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2016%22%3E%3C%2Fsvg%3E)}')
        svg_league_complex_encoded_example = cssutils.parseString('.logo-bg--league-nhl-com-xl {background-image: url(data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2016%22%3E%3C%2Fsvg%3E)}')

        for rule in svg_team_encoded_example:
            output_team = get_attrs_from_rule(rule)
            self.assertTrue('.logo-bg-dark--team-njd' == output_team.get('selector'))
            self.assertTrue('dark' == output_team.get('logo_attr'))
            self.assertTrue('team' == output_team.get('logo_type'))
            self.assertTrue('njd-dark' == output_team.get('logo_name'))
            self.assertTrue('</svg>' in output_team.get('svg'))
            self.assertTrue('njd-dark' == output_team.get('filename'))
            self.assertTrue('team' == output_team.get('dir'))

        for rule in svg_network_encoded_example:
            output_network = get_attrs_from_rule(rule)
            self.assertTrue('.logo-bg--team-4,.logo-bg-dark--network-cbc', output_network.get('selector'))
            self.assertTrue('dark' == output_network.get('logo_attr'))
            self.assertTrue('network' == output_network.get('logo_type'))
            self.assertTrue('cbc-dark' == output_network.get('logo_name'))

        for rule in svg_league_encoded_example:
            output_league = get_attrs_from_rule(rule)
            self.assertTrue('.logo-bg--league-nhl' == output_league.get('selector'))
            self.assertTrue('' == output_league.get('logo_attr'))
            self.assertTrue('league' == output_league.get('logo_type'))
            self.assertTrue('nhl' == output_league.get('logo_name'))

        for rule in svg_league_complex_encoded_example:
            output_league = get_attrs_from_rule(rule)
            self.assertTrue('.logo-bg--league-nhl-com-xl' == output_league.get('selector'))
            self.assertTrue('' == output_league.get('logo_attr'))
            self.assertTrue('league' == output_league.get('logo_type'))
            self.assertTrue('nhl-com-xl' == output_league.get('logo_name'))

    def test_delete_image_category(self):
        tmp_root_dir = tempfile.gettempdir()
        tmp_output_dir = tmp_root_dir + '/output'
        image_types = ['league', 'network', 'team']

        def create_tmp_dirs():
            if not os.path.exists(tmp_output_dir):
                os.makedirs(tmp_output_dir)

            with open(tmp_output_dir + '/.gitkeep', 'w+') as active_file:
                active_file.write('hello')

            for item in image_types:
                if not (os.path.exists(tmp_output_dir + '/' + item)):
                    os.makedirs(tmp_output_dir + '/' + item)

                with open(tmp_output_dir + '/' + item + '/tmp' + item + '.svg', 'w+') as active_file:
                    active_file.write(svg_example)

        # add test for png

        create_tmp_dirs()

        delete_image_category(tmp_output_dir, ['league'])
        self.assertFalse(os.path.isfile(tmp_output_dir + '/league/tmp_league.svg'))
        self.assertFalse(os.path.isdir(tmp_output_dir + '/league'))

        delete_image_category(tmp_output_dir, ['network'])
        self.assertFalse(os.path.isfile(tmp_output_dir + '/network/tmp_network.svg'))
        self.assertFalse(os.path.isdir(tmp_output_dir + '/network'))

        delete_image_category(tmp_output_dir, ['team'])
        self.assertFalse(os.path.isfile(tmp_output_dir + '/team/tmp_team.svg'))
        self.assertFalse(os.path.isdir(tmp_output_dir + '/team'))
        self.assertTrue(os.path.isfile(tmp_output_dir + '/.gitkeep'))


        # manually testing these instead of looping through image_types
        create_tmp_dirs()
        delete_image_category(tmp_output_dir)
        self.assertFalse(os.path.isfile(tmp_output_dir + '/league/tmp_league.svg'))
        self.assertFalse(os.path.isdir(tmp_output_dir + '/league'))
        self.assertFalse(os.path.isfile(tmp_output_dir + '/network/tmp_network.svg'))
        self.assertFalse(os.path.isdir(tmp_output_dir + '/network'))
        self.assertFalse(os.path.isfile(tmp_output_dir + '/team/tmp_team.svg'))
        self.assertFalse(os.path.isdir(tmp_output_dir + '/team'))
        self.assertTrue(os.path.isfile(tmp_output_dir + '/.gitkeep'))

        # cleanup
        shutil.rmtree(tmp_output_dir)

    def test_archive_images(self):
        tmp_root_dir = tempfile.gettempdir()
        tmp_output_dir = tmp_root_dir + '/output'
        image_types = ['league', 'network', 'team']

        def create_tmp_dirs():
            if not os.path.exists(tmp_output_dir):
                os.makedirs(tmp_output_dir)

            for item in image_types:
                if not (os.path.exists(tmp_output_dir + '/' + item)):
                    os.makedirs(tmp_output_dir + '/' + item)

                with open(tmp_output_dir + '/' + item + '/tmp' + item + '.svg', 'w+') as active_file:
                    active_file.write(svg_example)

        create_tmp_dirs()

        test_prepend_str = 'prepend'
        archived_path = archive_images(tmp_output_dir, tmp_output_dir, test_prepend_str)
        archived_path_chunks = archived_path.split('/')
        archived_file_chunks = archived_path_chunks[-1].split('.')
        print('archived_file_chunks=%r' % archived_file_chunks)
        archived_datetime_str = archived_file_chunks[0]
        print('archived_datetime_str=%s' % archived_datetime_str)
        archived_datetime = datetime.strptime(archived_datetime_str.split('_', 1)[-1], DATE_NOW_FORMAT)
        archived_extension = archived_file_chunks[1]

        self.assertTrue(os.path.isfile(archived_path))
        self.assertTrue(archived_path_chunks[-1].startswith(test_prepend_str))
        self.assertTrue(datetime.now() > archived_datetime)
        self.assertTrue(archived_extension == 'zip')

        # cleanup
        shutil.rmtree(tmp_output_dir)

        create_tmp_dirs()
        archived_path = archive_images(tmp_output_dir, tmp_output_dir)
        archived_path_chunks = archived_path.split('/')
        archived_file_chunks = archived_path_chunks[-1].split('.')
        archived_datetime_str = archived_file_chunks[0]
        archived_datetime = datetime.strptime(archived_datetime_str, DATE_NOW_FORMAT)
        archived_extension = archived_file_chunks[1]

        self.assertTrue(os.path.isfile(archived_path))
        self.assertFalse(archived_path_chunks[-1].startswith(test_prepend_str))
        self.assertTrue(datetime.now() > archived_datetime)
        self.assertTrue(archived_extension == 'zip')

        # cleanup
        shutil.rmtree(tmp_output_dir)


    def test_delete_archive(self):
        tmp_root_dir = tempfile.gettempdir()
        tmp_output_dir = tmp_root_dir + '/output'
        image_types = ['league', 'network', 'team']

        def create_tmp_dirs():
            if not os.path.exists(tmp_output_dir):
                os.makedirs(tmp_output_dir)

            for item in image_types:
                if not (os.path.exists(tmp_output_dir + '/' + item)):
                    os.makedirs(tmp_output_dir + '/' + item)

                with open(tmp_output_dir + '/' + item + '/tmp' + item + '.svg', 'w+') as active_file:
                    active_file.write(svg_example)

        create_tmp_dirs()

        archived_images = archive_images(path=tmp_output_dir, dest=tmp_output_dir)
        delete_archive(tmp_output_dir)

        self.assertFalse(os.path.isfile(archived_images))

        # cleanup
        shutil.rmtree(tmp_output_dir)

    def test_writes_image_to_file(self):
        tmp_root_dir = tempfile.gettempdir()
        tmp_output_dir = tmp_root_dir + '/output'
        image_types = ['league', 'network', 'team']

        def create_tmp_dirs():
            if not os.path.exists(tmp_output_dir):
                os.makedirs(tmp_output_dir)

            with open(tmp_output_dir + '/.gitkeep', 'w+') as active_file:
                active_file.write('hello')

            for item in image_types:
                if not (os.path.exists(tmp_output_dir + '/' + item)):
                    os.makedirs(tmp_output_dir + '/' + item)

                with open(tmp_output_dir + '/' + item + '/tmp' + item + '.svg', 'w+') as active_file:
                    active_file.write(svg_example)

        team_attrs_example = {
            'selector': '.logo-bg--team-njd',
            'logo_attr': 'darks',
            'logo_type': 'team',
            'logo_name': 'njd',
            'svg': '<svg xmlns="http://www.w3.org/2000/svg" id="Layer_2" width="253" height="62" viewBox="0 0 253 62"></svg>',
            'filename': 'njd',
            'dir': 'team',
        }

        output = write_image_to_file(team_attrs_example, ['svg'], dest=tmp_output_dir)
        self.assertTrue(len(output) == 1)
        self.assertTrue(output[0].endswith('.svg'))
        self.assertTrue(os.path.isfile(output[0]))

        output = write_image_to_file(team_attrs_example, ['png'], tmp_output_dir)
        self.assertTrue(len(output) == 1)
        self.assertTrue(output[0].endswith('.png'))
        self.assertTrue(os.path.isfile(output[0]))

        # cleanup
        delete_image_category(path=tmp_output_dir)

        output = write_image_to_file(team_attrs_example, ['svg', 'png', 'jpg'], tmp_output_dir)
        self.assertTrue(len(output) == 2)
        self.assertTrue(output[0].endswith('.svg'))
        self.assertTrue(output[1].endswith('.png'))
        self.assertTrue(os.path.isfile(output[0]))
        self.assertTrue(os.path.isfile(output[1]))

        # cleanup
        delete_image_category(path=tmp_output_dir)
