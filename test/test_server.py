from unittest import TestCase
from server.server import Server
import socket


class TestServer(TestCase):
    def setUp(self):
        self.__con = Server(4500, "/tmp/logfile")
        self.__con.createserver()
        self.__none_con = Server()

    def tearDown(self) -> None:
        pass

    def test_port(self):
        self.assertEqual(4500, self.__con.port)
        self.assertEqual(0, self.__none_con.port)

        self.__none_con.port = 6000
        self.assertEqual(6000, self.__none_con.port)

    def test_logfile(self):
        self.assertEqual("/tmp/logfile", self.__con.log)
        self.assertEqual("", self.__none_con.log)

        self.__none_con.log = "/dir/file"
        self.assertEqual("/dir/file", self.__none_con.log)

    def test_server(self):
        pass