from unittest import TestCase
import os

from api_blaster.cli.commands.directory_command import DirectoryCommand
from api_blaster.cli.commands.request_command import RequestCommand
from api_blaster.cli.commands.settings_command import SettingsCommand
from api_blaster.cli.menu_builder import MenuBuilder
from api_blaster.settings.cfg import get_config, initialize_configs
from tests.resources import request_collections


def setUpModule():
    initialize_configs()


class TestMenuBuilder(TestCase):

    request_collections_base_dir = os.path.dirname(request_collections.__file__)

    def setUp(self) -> None:
        self.menu = MenuBuilder(self.request_collections_base_dir)
        self.menu_items = self.menu.get_items()

    def test_change_directory(self):
        """
        Test that changing to the settings directory
        correctly updates the `dir` instance property
        of the MenuBuilder class
        """
        self.menu.set_dir(self.request_collections_base_dir)
        self.assertEqual(self.menu.get_dir(), self.request_collections_base_dir)
        self.menu.set_dir(get_config('SETTINGS_DIR'))
        self.assertEqual(self.menu.get_dir(), get_config('SETTINGS_DIR'))

    def test_standard_command_types(self):
        """
        This test checks that in a "regular" request collections
        directory the MenuBuilder class only returns
        DirectoryCommand objects or RequestCommand objects.
        """
        self.menu.set_dir(self.request_collections_base_dir)
        for item in self.menu_items:
            with self.subTest(item):
                if repr(item).rpartition(".")[2] == "json":
                    self.assertIsInstance(item, RequestCommand)
                else:
                    self.assertIsInstance(item, DirectoryCommand)

    def test_settings_command_type(self):
        """
        Tests that when in the settings directory only
        SettingsCommand instances are returned.
        """
        self.menu.set_dir(get_config('SETTINGS_DIR'))
        settings_items = self.menu.get_items()
        for item in settings_items:
            with self.subTest(item):
                self.assertIsInstance(item, SettingsCommand)
