from server.server import Server
from packet.packet import Packet
import socket


class Client(Server):
    """

    """

    def __init__(self, ip: str = "", port: int = 0, log: str = ""):
        super(Client, self).__init__(port, log)
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

            packet = Packet(b"HELLO", "!5s")
            packed_message = packet.build()
            client_socket.sendall(packed_message)

            data = client_socket.recv(1024)
            unpack_data = packet.unpack(packet.formatter, data)
            print(unpack_data[0])

            print("Closing socket")
            client_socket.close()
