import urllib.request
import struct
import socket
from multipledispatch import dispatch


class Packet(object):
    """
    Constructs packet
    """

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
    def padding(self):
        return self.__padding

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
        data = struct.pack('!I', self.__seq_num)
        data += struct.pack('!I', self.__ack_num)
        # data += struct.pack('!{0}s'.format(len(self.__padding)), self.__padding.encode())
        data += struct.pack("!s", self.__ack.encode('utf-8'))
        data += struct.pack("!s", self.__syn.encode('utf-8'))
        data += struct.pack("!s", self.__fin.encode('utf-8'))
        data += struct.pack("{0}s".format(len(self.__data)), self.__data)
        data += self.__data
        return data

    @staticmethod
    def get_webpage(**kwargs):
        page = kwargs["webpage"]

        with urllib.request.urlopen(page) as resp, open("test1", "w") as w:
            html = resp.read()
            w.write(html.decode())

        return html

    @staticmethod
    def create_packet(version: int = 0, type: int = 0, message: str = "") -> None:
        data = struct.pack("!I", version)
        data += struct.pack("!I", type)
        data += struct.pack("!I", len(message))
        data += message.encode()
        return data        
