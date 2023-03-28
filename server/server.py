import socket
import struct
from packet.packet import Packet
import RPi.GPIO as GPIO


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
        hello = Packet.create_packet(version=17, type=1, message="Hello")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', self.__port))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2, GPIO.OUT)

        with open(self.__log_location, "w") as logfile, open("recv_file", "wb") as w:
            while True:
                INCONN, INADDR = sock.recvfrom(512)
                print("Received connection from (IP, PORT): ", INADDR)
                logfile.write("Received connection from (IP, PORT): " + "".join(map(str, INADDR)) + "\n")
                w.write(INCONN)

                try:
                    while True:
                        data = sock.recv(struct.calcsize('!III'))

                        if len(data) == 0:
                            break
                        
                        version_raw, message_type_raw, length_raw = struct.unpack('!III', data)
                        version = socket.ntohs(version_raw)
                        message_type = socket.ntohs(message_type_raw)
                        length = socket.ntohs(length_raw)
                        message = sock.recv(length).decode()

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
                            sock.sendall(hello)
                        elif message_type == 2:
                            print("EXECUTING SUPPORTED COMMAND: ", message)
                            logfile.write("EXECUTING SUPPORTED COMMAND: " + message + "\n")

                            if message == "LIGHTON":
                                GPIO.output(2, GPIO.HIGH)
                                print("Returning SUCCESS")
                                logfile.write("Returning SUCCESS\n")
                                SUCCESS = Packet(17, 2, "SUCCESS")
                                sock.sendall(SUCCESS.build())
                            elif message == "LIGHTOFF":
                                GPIO.output(2, GPIO.LOW)
                                print("Returning SUCCESS")
                                logfile.write("Returning SUCCESS\n")
                                SUCCESS = Packet(17, 2, "SUCCESS")
                                sock.sendall(SUCCESS.build())

                        else:
                            print("IGNORING UNKNOWN COMMAND: ", message)
                            logfile.write("IGNORING UNKNOWN COMMAND: " + message + "\n")
                    
                except socket.timeout:
                    sock.close()