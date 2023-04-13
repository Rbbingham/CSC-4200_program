import socket
from packet.packet import Packet
import struct


class Server:
    def __init__(self, port: int = 0, log: str = "", webpage: str = "") -> None:
        self.__port: int = port
        self.__log_location: str = log
        self.__webpage: str = webpage

    @property
    def port(self) -> int:
        return self.__port

    @property
    def log(self) -> str:
        return self.__log_location

    @property
    def webpage(self) -> str:
        return self.__webpage

    @port.setter
    def port(self, port: int) -> None:
        self.__port = int(port)

    @log.setter
    def log(self, log: str) -> None:
        self.__log_location = log

    @webpage.setter
    def webpage(self, webpage: str) -> None:
        self.__webpage = webpage     

    def createserver(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", self.__port))

        with open(self.__log_location, "w") as logfile:
            try:
                while True:
                    # three-way handshake
                    data, address = sock.recvfrom(512)
                    logfile.write("Received connection from (IP, PORT): {}\n".format(address))

                    _seq, _ackn = struct.unpack("!II", data[:8])
                    _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[8:11])]
                    logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(_seq, _ackn, _ack, _syn, _fin))

                    seq_num = 100
                    ack_num = _seq + 1
                    send_data = Packet(sequence_number=seq_num, ack_number=ack_num, ack='Y', syn='Y', fin='N', data=b"")
                    sock.sendto(send_data.build(), address)
                    logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, ack_num, 'N', 'Y', 'N'))

                    data, address = sock.recvfrom(512)

                    ack_num, seq_num = struct.unpack("!II", data[:8])
                    _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[8:11])]
                    logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))
                    ack_num += 1

                    webpage = Packet.get_webpage(webpage=self.__webpage)
                    webpage_iter = [webpage[i:i+502] for i in range(0, len(webpage), 501)]

                    for x in webpage_iter:
                        if len(x) != 502:
                            send_data = Packet(sequence_number=seq_num, ack_number=ack_num, ack='Y', syn='N', fin='Y',
                                               data=x)
                        else:
                            send_data = Packet(sequence_number=seq_num, ack_number=ack_num, ack='Y', syn='N', fin='N',
                                               data=x)

                        sock.sendto(send_data.build(), address)
                        logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, ack_num, 'N', 'Y', 'N'))

                        data, address = sock.recvfrom(512)

                        ack_num, seq_num = struct.unpack("!II", data[:8])
                        _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[8:11])]
                        logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))
                        ack_num += 1

                        if _fin == 'Y':
                            break

            except socket.timeout:
                sock.close()
                logfile.close()
