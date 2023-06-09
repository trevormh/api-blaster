from typing import List

from api_blaster.cli.cli import CLI
from api_blaster.cli.commands.command import Command
from api_blaster.cli.commands.request_command import RequestCommand
from api_blaster.cli.commands.settings_command import SettingsCommand
from api_blaster.cli.menu_builder import MenuBuilder
from api_blaster.settings.cfg import get_config, initialize_configs
from tests.resources import request_collections
from unittest import TestCase, mock
import os


def setUpModule():
    initialize_configs()


class TestMenuBuilder(TestCase):
    request_collections_base_dir = os.path.dirname(request_collections.__file__)

    def setUp(self) -> None:
        self.menu = MenuBuilder(self.request_collections_base_dir)
        self.cli = CLI(self.menu)
        # self.commands, self.display_text = self.cli.menu_items()

    def test_get_commands(self):
        """
        Test that data is returned by the get_commands method.
        Should be a list
        """
        commands = self.cli.get_commands()
        self.assertGreater(len(commands), 1)
        self.assertIsInstance(commands, List)

    def test_get_commands_types(self):
        """
        Test that the get_commands method returns only
        Command instance objects.
        """
        commands = self.cli.get_commands()
        self.assertGreater(len(commands), 1)
        for cmd in commands:
            with self.subTest(cmd):
                self.assertIsInstance(cmd, Command)

    def test_get_menu_items(self):
        """
        Test that the menu_items method returns data.
        It should be a list consisting of 2 lists.
        """
        items = self.cli.menu_items()
        self.assertEqual(len(items), 2)
        # verify the 0th index is a list
        self.assertIsInstance(items[0], List)
        self.assertGreater(len(items[0]), 1)
        # verify the 1st index is a list
        self.assertIsInstance(items[1], List)
        self.assertGreater(len(items[1]), 1)

    def test_menu_item_command_types(self):
        """
        The response should be a list containing 2 lists,
        where index 0 is a list of Command class instances.
        """
        items = self.cli.menu_items()[0]
        for cmd in items:
            with self.subTest(cmd):
                self.assertIsInstance(cmd, Command)

    def test_menu_item_display_text_types(self):
        """
        The response should be a list containing 2 lists,
        where index 1 is a list of strings.
        """
        items = self.cli.menu_items()[1]
        for display_text in items:
            with self.subTest(display_text):
                self.assertIsInstance(display_text, str)

    def test_execute_settings_command(self):
        """
        Test when the settings command is run that
        the settings menu is properly set up.
        """
        self.cli.handle_execute_command("settings")
        # verify the menu has been changed to the settings directory
        self.assertEqual(self.menu.get_dir(), get_config('SETTINGS_DIR'))
        # Verify the response isn't empty
        # index 0 should contain a list of SettingsCommand instances
        items = self.cli.menu_items()[0]
        self.assertGreater(len(items), 1)
        # verify all the commands returned are Settings class instances
        for item in items:
            with self.subTest(item):
                self.assertIsInstance(item, SettingsCommand)

    def test_execute_request_command(self):
        """
        Tests that when a RequestCommand is executed
        from the CLI class that the execute command in
        HttpRequest class is called.

        Patch the execute method from the HttpRequest method
        and verified it's called once.
        """
        def execute():
            pass
        mock_called = False

        func_path = 'api_blaster.cli.commands.request_command.RequestCommand.execute'
        with mock.patch(func_path, side_effect=execute) as mock_execute:
            menu_items = self.cli.menu_items()
            # commands instances are in index 0 of the menu_items response
            for idx, item in enumerate(menu_items[0]):
                if isinstance(item, RequestCommand):
                    cmd_name = menu_items[1][idx]
                    self.cli.handle_execute_command(cmd_name)
                    mock_execute.assert_called_once()
                    mock_called = True
                    break
        # verify the mock was actually reached
        self.assertEqual(mock_called, True)

    def test_cd_command(self):
        """
        Tests the cd command is working properly.

        Need to patch the requests_dir attribute for both
        the menu and cli to be the test specific request collection
        because it gets those values from the app settings, which
        will be set to a different directory.
        """
        menu = MenuBuilder(self.request_collections_base_dir)
        with mock.patch.object(menu, 'requests_dir', self.request_collections_base_dir):
            cli = CLI(menu)
            with mock.patch.object(cli, 'requests_dir', self.request_collections_base_dir):
                # verify we're in the request collections directory
                self.assertEqual(menu.get_dir(), self.request_collections_base_dir)

                # change to settings directory
                cli.handle_execute_command("settings")
                self.assertEqual(menu.get_dir(), get_config('SETTINGS_DIR'))

                # now execute the cd command
                cli.handle_execute_command("cd ..")

                # should be back in the root directory
                self.assertEqual(menu.get_dir(), self.request_collections_base_dir)
                # Verify user can't back up an additional directory
                # outside the project root.
                cli.handle_execute_command("cd ..")
                cli.handle_execute_command("cd ..")
                cli.handle_execute_command("cd ..")
                # should still be in the project root
                self.assertEqual(menu.get_dir(), self.request_collections_base_dir)

