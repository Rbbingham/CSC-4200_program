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
        hello = Packet.create_packet(version=17, type=1, message="Hello")

        command_packet_on = Packet.create_packet(version=17, type=2, message="LIGHTON")
        command_packet_off = Packet.create_packet(version=17, type=2, message="LIGHTOFF")

        webpage = Packet.get_webpage(webpage="http://www.python.org")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__ip, super().port)

        buf = 512
        r = open("test1", "rb")
        total_read = 0
        data_size = len(webpage)
        data = r.read(buf)
        total_read += 512

        send_data = Packet(sequence_number=100, ack_number=0, ack='Y', syn='N', fin='N'	, data=data)
        sock.sendto(data, server_address)
        
        sock.sendto(hello, server_address)

#         while total_read < data_size:
#             if sock.sendto(data, server_address):
#                 send_data = Packet(sequence_number=101, ack_number=0, ack='Y', syn='N', fin='N', data=data)
#                 send_data = send_data.build()
#                 data = r.read(buf)
#                 total_read += len(send_data) - 12

        with open(super().log, "w") as logfile:
            try:
                while True:
                    data = sock.recv(struct.calcsize('!III'))
                    version_raw, message_type_raw, length_raw = struct.unpack('!III', data)
                    version = socket.ntohs(version_raw)
                    message_type = socket.ntohs(message_type_raw)
                    length = socket.ntohs(length_raw)
                    message = sock.recv(length).decode()

                    print("Received data: {}".format(message), end=" ")
                    print("version: {} type: {} length: {}".format(version, message_type, length))

                    logfile.write("Received data: {} ".format(message))
                    logfile.write("version: {} type: {} length: {}\n".format(version, message_type, length))

                    if version == 17:
                        print("VERSION ACCEPTED")
                        logfile.write("VERSION ACCEPTED\n")
                    else:
                        print("VERSION MISMATCH")
                        logfile.write("VERSION MISMATCH\n")

                    print("Message", message)
                    logfile.write("Message " + message + "\n")

                    if message_type == 1:
                        print("Sending command")
                        logfile.write("Sending command\n")
                        time.sleep(3)
                    elif message_type == 2 and message == "SUCCESS":
                        print("Command Successful")
                        print("Closing Socket")
                        logfile.write("Command Successful\nClosing socket\n")
                        break

            finally:
                sock.close()
                logfile.close()
                r.close()