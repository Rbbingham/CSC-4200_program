from unittest import TestCase
from client.client import Client


class TestClient(TestCase):
    def setUp(self):
        self.__client = Client("127.0.0.1", 6000, "/tmp/logfile")
        self.__none_client = Client()

    def test_port(self):
        self.assertEqual(6000, self.__client.port)
        self.assertEqual(0, self.__none_client.port)

    def test_log(self):
        self.assertEqual("/tmp/logfile", self.__client.log)
        self.assertEqual("", self.__none_client.log)
