import socket
from packet.packet import Packet
import struct


class Server:
    def __init__(self, port: int = 0, log: str = "", file: str = "") -> None:
        self.__port: int = port
        self.__log_location: str = log
        self.__file: str = file

    @property
    def port(self) -> int:
        return self.__port

    @property
    def log(self) -> str:
        return self.__log_location

    @property
    def file(self) -> str:
        return self.__file

    @port.setter
    def port(self, port: int) -> None:
        self.__port = int(port)

    @log.setter
    def log(self, log: str) -> None:
        self.__log_location = log

    @file.setter
    def file(self, file: str) -> None:
        self.__file = file     

    def createserver(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", self.__port))

        with open(self.__log_location, "w") as logfile:
            try:
                while True:
                    # three-way handshake
                    data, address = sock.recvfrom(512)
                    logfile.write("Received connection from (IP, PORT): {}\n".format(address))

                    _seq, _ackn, window_size = struct.unpack("!III", data[:12])
                    _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[12:15])]
                    logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(_seq, _ackn, _ack, _syn, _fin))

                    seq_num = 100
                    ack_num = _seq + 1
                    send_data = Packet(sequence_number=seq_num, ack_number=ack_num, window=0, ack='Y', syn='Y', fin='N', data=b"")
                    sock.sendto(send_data.build(), address)
                    logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, ack_num, 'N', 'Y', 'N'))

                    data, address = sock.recvfrom(512)

                    ack_num, seq_num, window_size = struct.unpack("!III", data[:12])
                    _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[12:15])]
                    logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))

                    ack_num += 1
                    sum = 0

                    while True:
                        with open(self.__file, "rb") as f:
                            f.seek(sum)
                            data = f.read(window_size)

                            if len(data) != window_size:
                                send_data = Packet(sequence_number=seq_num, ack_number=ack_num, window=window_size, ack='Y', syn='N', fin='Y',
                                                   data=data)
                            else:
                                send_data = Packet(sequence_number=seq_num, ack_number=ack_num, window=window_size, ack='Y', syn='N', fin='N',
                                                   data=data)

                            sock.sendto(send_data.build(), address)
                            logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, ack_num, 'N', 'Y', 'N'))

                            data, address = sock.recvfrom(512)

                            ack_num, seq_num, window_size = struct.unpack("!III", data[:12])
                            _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[12:15])]
                            logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))

                            ack_num += 1
                            sum += window_size - 1

                            if _fin == 'Y':
                                break

            except socket.timeout:
                sock.close()
                logfile.close()
