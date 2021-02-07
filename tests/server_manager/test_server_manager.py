import unittest

from applets.server_manager import ServerManager
from client.Client import Client


class ServerManagerTest(unittest.TestCase):

    def test_connect(self):
        sm = Client.get_instance()
        sm.remote



if __name__ == '__main__':
    unittest.main()
