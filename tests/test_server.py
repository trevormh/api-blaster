import time

from api_blaster.__main__ import is_port_available
from api_blaster.server.main import server_setup, stop_server
from api_blaster.settings.cfg import get_config, initialize_configs
from tests.resources import request_collections
from unittest import TestCase, mock
import os


def setUpModule():
    initialize_configs()


def patch_restart_server():
    """
    This function is used as a patch for test_change_port
    """
    stop_server()
    response_dir = os.getcwd()
    port_number = 8051
    server_setup(response_dir, port_number)


class TestServer(TestCase):

    def test_server_startup_shutdown(self):
        """
        This test verifies that the tornado server
        used to display responses starts up and stops
        correctly.
        """
        # verify nothing is running on port 8050
        self.assertEqual(is_port_available(8050), True)
        # start the server
        server_setup(get_config('ROOT_DIR'), 8050)
        # pause for a second to let the server start up
        time.sleep(1)
        # verify the port has now been taken
        self.assertEqual(is_port_available(8050), False)
        stop_server()
        # pause for a second to let the server shut down
        time.sleep(1)
        # verify the port is now available again
        self.assertEqual(is_port_available(8050), True)

    @mock.patch('api_blaster.server.main.restart_server', side_effect=patch_restart_server)
    def test_change_port(self, restart_server):
        """
        This test verifies the tornado server port
        can be changed.
        """
        starting_port = 8050
        change_port = 8051
        # verify both ports are available
        self.assertEqual(is_port_available(starting_port), True)
        self.assertEqual(is_port_available(change_port), True)
        # start the server with the starting port
        server_setup(get_config('ROOT_DIR'), starting_port)
        # pause for a second to let the server start up
        time.sleep(1)
        # verify the starting port is now take
        self.assertEqual(is_port_available(starting_port), False)
        self.assertEqual(is_port_available(change_port), True)
        # Restart the server with the patch_restart_server function
        # which has the new port number. It will stop the old port
        # and start the new one.
        restart_server()
        # pause for a second to let the server do its thing...
        time.sleep(1)
        # verify the starting port is now available and the change_port is taken
        self.assertEqual(is_port_available(starting_port), True)
        self.assertEqual(is_port_available(change_port), False)
