import struct


class Packet(object):
    """
    Constructs packet
    """

    def __init__(self, data=0, formatter=""):
        self.__data = data
        self.__formatter = formatter

    @property
    def data(self):
        return self.__data

    @property
    def formatter(self):
        return self.__formatter

    @data.setter
    def data(self, data):
        self.__data = data

    @formatter.setter
    def formatter(self, formatter):
        self.__formatter = formatter

    def build(self):
        return struct.pack(self.__formatter, self.__data)

    @staticmethod
    def unpack(formatter, data):
        return struct.unpack(formatter, data)
