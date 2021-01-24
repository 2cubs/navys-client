import unittest

from client.Client import Client


def my_event_cb():
    pass


class TestServiceManager(unittest.TestCase):

    app = Client.get_instance()
    app.subscribe_to_event(Client.EVENT_SERVICE_STATUS_CHANGED, my_event_cb)
    remote = app.remote

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
