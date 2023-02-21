import struct
import socket


class Packet(object):
    """
    Constructs packet
    """

    def __init__(self, version: int = 0, type: int = 0, message: str = ""):
        self.__version = version
        self.__type = type
        self.__len_message = len(message)
        self.__message = message
        self.__formatter = formatter

        def build(self):
        version = socket.htons(self.__version)
        type = socket.htons(self.__type)
        data = struct.pack('!III', version, type, self.__len_message)
        data += self.__message.encode()
        return data
