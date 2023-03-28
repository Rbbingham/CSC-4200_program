import urllib.request
import struct
import socket
from multipledispatch import dispatch


class Packet(object):
    """
    Constructs packet
    """

    @dispatch(int, int, str)
    def __init__(self, version: int = 0, type: int = 0, message: str = "") -> None:
        self.__version = version
        self.__type = type
        self.__len_message = len(message)
        self.__message = message

    @dispatch()
    def __init__(self, **kwargs) -> None:
        self.__seq_num = kwargs["sequence_number"]
        self.__ack_num = kwargs["ack_number"]
        self.__padding = ["x"] * 29
        self.__ack = kwargs["ack"]
        self.__syn = kwargs["syn"]
        self.__fin = kwargs["fin"]
        self.__data = kwargs["data"]

    @property
    def seq_num(self):
        return self.__seq_num

    @property
    def ack_num(self):
        return self.__ack_num

    @property
    def ack(self):
        return self.__ack

    @property
    def syn(self):
        return self.__syn

    @property
    def fin(self):
        return self.__fin

    @dispatch()
    def build(self):
        version = socket.htons(self.__version)
        type = socket.htons(self.__type)
        data = struct.pack('!III', version, type, self.__len_message)
        data += self.__message.encode()

    @dispatch()
    def build(self):
        data = struct.pack('!I', self.__seq_num)
        data += struct.pack('!I', self.__ack_num)
        data += struct.pack('!{0}s'.format(len(self.__padding), self.__padding))
        data += struct.pack("!c", self.__ack)
        data += struct.pack("!c", self.__syn)
        data += struct.pack("!c", self.__fin)
        data += struct.pack("{0}s".format(len(self.__data), self.__data))
        data += self.__data.encode()
        return data

    @staticmethod
    def get_webpage(**kwargs):
        page = kwargs["webpage"]

        with urllib.request.urlopen(page) as resp, open('test', w) as w:
            html = resp.read()
            w.write(html.decode())

        return html
