import struct
import socket
from multipledispatch import dispatch


class Packet(object):
    """
    Constructs packet
    """

    def __init__(self, version: int = 0, type: int = 0, message: str = ""):
        self.__version = version
        self.__type = type
        self.__len_message = len(message)
        self.__message = message

    @property
    def version(self):
        return self.__version

    @property
    def type(self):
        return self.__type

    @property
    def message(self):
        return self.__message

    @version.setter
    def version(self, value):
        self.__version = value

    @type.setter
    def type(self, value):
        self.__type = value

    @message.setter
    def message(self, value):
        self.__message = value

    @dispatch()
    def build(self):
        version = socket.htons(self.__version)
        type = socket.htons(self.__type)
        data = struct.pack('!III', version, type, self.__len_message)
        data += self.__message.encode()
        return data
