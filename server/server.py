import socket
import struct
import binascii
from packet.packet import Packet


class Server:
    def __init__(self, port: int = 0, log: str = "") -> None:
        self.__port: int = port
        self.__log_location: str = log

    @property
    def port(self) -> int:
        return self.__port

    @property
    def log(self) -> str:
        return self.__log_location

    @port.setter
    def port(self, port: int) -> None:
        self.__port = int(port)

    @log.setter
    def log(self, log: str) -> None:
        self.__log_location = log

    def createserver(self) -> None:
        hello = Packet(17, 1, "Hello")
        hello_packet = hello.build()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', self.__port))
        sock.listen()

        while True:
            INCONN, INADDR = sock.accept()
            print("Received connection from (IP, PORT): ", INADDR)

            try:
                while True:
                    data = INCONN.recv(struct.calcsize('!III'))

                    if len(data) == 0:
                        break

                    version_raw, message_type_raw, length_raw = struct.unpack('!III', data)
                    version = socket.ntohs(version_raw)
                    message_type = socket.ntohs(message_type_raw)
                    length = socket.ntohs(length_raw)
                    print('Received data: version: {0:d} message_type: {1:d} length: {2:d}'.format(version, message_type, length))
                    if version == 17:
                        print("VERSION ACCEPTED")
                        message = INCONN.recv(length).decode()
                    else:
                        print("VERSION MISMATCH")
                        continue

                    if message_type == 1:
                        INCONN.sendall(hello_packet)
                    elif message_type == 2:
                        print("EXECUTING SUPPORTED COMMAND: ", message)

                        if message == "LIGHTON":
                            print("Returning SUCCESS")
                            SUCCESS = Packet(17, 2, "SUCCESS")
                            INCONN.sendall(SUCCESS.build())
                        elif message == "LIGHTOFF":
                            print("Returning SUCCESS")
                            SUCCESS = Packet(17, 2, "SUCCESS")
                            INCONN.sendall(SUCCESS.build())

                    else:
                        print("IGNORING UNKNOWN COMMAND: ", message)

            finally:
                INCONN.close()
