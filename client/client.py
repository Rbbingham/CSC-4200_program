import struct
import time
from server.server import Server
from packet.packet import Packet
import socket


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
            send_data = Packet(sequence_number=seq_num, ack_number=ack_num, ack='N', syn='Y', fin='N', data=b"")
            sock.sendto(send_data.build(), server_address)
            logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, 0, 'N', 'Y', 'N'))

            data, address = sock.recvfrom(512)
            logfile.write("Received connection from (IP, PORT): {}\n".format(address))

            ack_num, seq_num = struct.unpack("!II", data[:8])
            _ack, _syn, _fin = [x.decode("utf-8") for x in struct.unpack("!ccc", data[8:11])]
            logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))
            ack_num += 1

            send_data = Packet(sequence_number=seq_num, ack_number=ack_num, ack='Y', syn='N', fin='N', data=b"")
            sock.sendto(send_data.build(), server_address)
            logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, 0, 'Y', 'N', 'N'))

            while True:
                data, address = sock.recvfrom(512)
                (ack_num, seq_num) = struct.unpack("!II", data[:8])
                (_ack, _syn, _fin) = [x.decode("utf-8") for x in struct.unpack("!ccc", data[8:11])]
                (payload, ) = struct.unpack("!501s", data[11:])
                logfile.write("\"RECV\" <{}> <{}> [{}] [{}] [{}]\n".format(ack_num, seq_num, _ack, _syn, _fin))
                ack_num += 512

                send_data = Packet(sequence_number=seq_num, ack_number=ack_num, ack='Y', syn='N', fin='N', data=b"")
                sock.sendto(send_data.build(), server_address)
                logfile.write("\"SEND\" <{}> <{}> [{}] [{}] [{}]\n".format(seq_num, 0, 'Y', 'N', 'N'))

        # with open(super().log, "w") as logfile:
        #     try:
        #         while True:
        #
        #             print("Received data: {}".format(message), end=" ")
        #             print("version: {} type: {} length: {}".format(version, message_type, length))
        #
        #             logfile.write("Received data: {} ".format(message))
        #             logfile.write("version: {} type: {} length: {}\n".format(version, message_type, length))
        #
        #             if version == 17:
        #                 print("VERSION ACCEPTED")
        #                 logfile.write("VERSION ACCEPTED\n")
        #             else:
        #                 print("VERSION MISMATCH")
        #                 logfile.write("VERSION MISMATCH\n")
        #
        #             print("Message", message)
        #             logfile.write("Message " + message + "\n")
        #
        #             if message_type == 1:
        #                 print("Sending command")
        #                 logfile.write("Sending command\n")
        #                 time.sleep(3)
        #             elif message_type == 2 and message == "SUCCESS":
        #                 print("Command Successful")
        #                 print("Closing Socket")
        #                 logfile.write("Command Successful\nClosing socket\n")
        #                 break
        #
        #     finally:
        #         sock.close()
        #         logfile.close()
        #         r.close()

        sock.close()
        logfile.close()