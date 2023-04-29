import struct
from server.server import Server
from packet.packet import Packet
import socket
import math
import RPi.GPIO as GPIO


class Client(Server):
    def __init__(self, ip: str = "", port: int = 0, log: str = "", file: str = ""):
        super(Client, self).__init__(port, log)
        self.__ip: str = ip
        self.__file: str = file

    @property
    def ip(self) -> str:
        return self.__ip
    
    @property
    def file(self) -> str:
        return self.__file

    @ip.setter
    def ip(self, ip: str) -> None:
        self.__ip = ip

    @file.setter
    def file(self, file: str) -> None:
        self.__file = file

    def conserver(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__ip, super().port)

        with open(super().log, "w") as logfile:
            # three-way handshake
            seq_num = 12345
            ack_num = 0
            window_size = 0

            send_data = Packet(sequence_number=seq_num, ack_number=ack_num, window=window_size, ack='N', syn='Y', fin='N', data=b"")
            sock.sendto(send_data.build(), server_address)
            logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, 0, 'N', 'Y', 'N'))

            data, address = sock.recvfrom(512)
            logfile.write("Received connection from (IP, PORT): {}\n".format(address))

            ack_num, seq_num = struct.unpack("!II", data[:8])
            _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[12:15])]
            logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))

            ack_num += 1
            window_size += 1

            send_data = Packet(sequence_number=seq_num, ack_number=ack_num, window=window_size, ack=_ack, syn='N', fin='N', data=b"")
            sock.sendto(send_data.build(), server_address)
            logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, ack_num, 'Y', 'N', 'N'))

            with open(self.__file, "w") as file:
                while True:
                    data, address = sock.recvfrom(512)
                    ack_num, seq_num = struct.unpack("!II", data[:8])
                    _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[12:15])]
                    (payload, ) = struct.unpack("!{}s".format(len(data[15:])), data[15:])

                    logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))
                    file.write(payload.decode("utf-8"))

                    ack_num += len(data)
                    window_size += 1

                    if window_size > 497:
                        window_size = math.floor(window_size / 2)

                    if _fin == 'Y':
                        send_data = Packet(sequence_number=seq_num, ack_number=ack_num, window=window_size, ack=_ack, syn='N', fin=_fin, data=b"")
                        sock.sendto(send_data.build(), server_address)
                        logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, ack_num, 'Y', 'N', 'Y'))
                        break
                    else:
                        send_data = Packet(sequence_number=seq_num, ack_number=ack_num, window=window_size, ack=_ack, syn='N', fin=_fin, data=b"")
                        sock.sendto(send_data.build(), server_address)
                        logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, ack_num, 'Y', 'N', 'N'))

                file.close()

        try:
            with open(self.__file, "r") as file:
                COMMAND = file.readline().split("=")[1].strip("\n")

            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(2, GPIO.OUT)

            if COMMAND == "LIGHTON":
                GPIO.output(2, GPIO.HIGH)
            elif COMMAND == "LIGHTOFF":
                GPIO.output(2, GPIO.LOW)
            else:
                print("UNKNOWN COMMAND")
        except IndexError:
            print("UNKNOWN COMMAND")

        sock.close()
        logfile.close()
        file.close()
