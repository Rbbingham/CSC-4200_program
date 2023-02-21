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

        with open(self.__log_location, "w") as logfile:
            while True:
                INCONN, INADDR = sock.accept()
                print("Received connection from (IP, PORT): ", INADDR)
                logfile.write("Received connection from (IP, PORT): " + "".join(map(str, INADDR)) + "\n")

                try:
                    while True:
                        data = INCONN.recv(struct.calcsize('!III'))

                        if len(data) == 0:
                            break

                        version_raw, message_type_raw, length_raw = struct.unpack('!III', data)
                        version = socket.ntohs(version_raw)
                        message_type = socket.ntohs(message_type_raw)
                        length = socket.ntohs(length_raw)
                        message = INCONN.recv(length).decode()

                        print("Received data: {}".format(message), end=" ")
                        print("version: {} message_type: {} length: {}".format(version, message_type, length))

                        logfile.write("Received data: {}".format(message))
                        logfile.write(" version: {} message_type: {} length: {}".format(version,
                                                                                        message_type,
                                                                                        length) + "\n")
                        if version == 17:
                            print("VERSION ACCEPTED")
                            logfile.write("VERSION ACCEPTED\n")
                        else:
                            print("VERSION MISMATCH")
                            logfile.write("VERSION MISMATCH\n")
                            continue

                        if message_type == 1:
                            INCONN.sendall(hello_packet)
                        elif message_type == 2:
                            print("EXECUTING SUPPORTED COMMAND: ", message)
                            logfile.write("EXECUTING SUPPORTED COMMAND: " + message + "\n")

                            if message == "LIGHTON":
                                print("Returning SUCCESS")
                                logfile.write("Returning SUCCESS\n")
                                SUCCESS = Packet(17, 2, "SUCCESS")
                                INCONN.sendall(SUCCESS.build())
                            elif message == "LIGHTOFF":
                                print("Returning SUCCESS")
                                logfile.write("Returning SUCCESS\n")
                                SUCCESS = Packet(17, 2, "SUCCESS")
                                INCONN.sendall(SUCCESS.build())

                        else:
                            print("IGNORING UNKNOWN COMMAND: ", message)
                            logfile.write("IGNORING UNKNOWN COMMAND: " + message + "\n")

                finally:
                    INCONN.close()
