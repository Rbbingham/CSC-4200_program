from multipledispatch import dispatch
from server.server import Server
from packet.packet import Packet
import socket


class Client(Server):
    """

    """

    @dispatch()
    def __init__(self) -> None:
        super(Server, self).__init__()
        self.__ip: str = ""

    @dispatch(str, int, str)
    def __init__(self, ip: str, port: int, log: str):
        super(Server, self).__init__(port, log)
        self.__ip: str = ip

    @property
    def ip(self) -> str:
        return self.__ip

    @ip.setter
    def ip(self, ip: str) -> None:
        self.__ip = ip

    def conserver(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.__ip, super().port))
            packet = Packet()
            packet.formatter = "!I"
            packet.data = 1234
            packed_message = packet.build()
            client_socket.sendall(packed_message)

            data = client_socket.recv(1024)
            print(data)
