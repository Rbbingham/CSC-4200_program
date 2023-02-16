import struct


class Packet:
    """
    Constructs packet
    """

    def __init__(self, dest_pt: int = 80,
                 src_pt: int = 65535,
                 dest_ip: str = "127.0.0.1",
                 src_ip: str = "192.168.1.101",
                 version: int = 0,
                 message_type: int = 0,
                 message: str = "") -> None:
        self.__dest_port: int = dest_pt
        self.__src_port: int = src_pt
        self.__dest_ip: str = dest_ip
        self.__src_ip: str = src_ip
        self.__version: int = version
        self.__type: int = message_type
        self.__message: str = message

    def build(self):
        packet = struct.pack()