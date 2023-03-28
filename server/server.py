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
        webpage = Packet.get_webpage(webpage=self.__webpage)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', self.__port))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2, GPIO.OUT)

        with open(self.__log_location, "w") as logfile, open("recv_file", "wb") as w:
            while True:
                data, address = sock.recvfrom(512)
                print("Received connection from (IP, PORT): ", address)
                logfile.write("Received connection from (IP, PORT): " + "".join(map(str, address)) + "\n")
                w.write(address)
                
                send_data = Packet(sequence_number=1, ack_number=1, ack='Y', syn='Y', fin='N', data=data)
                sock.sendto(send_data, address)

                while True:
                    
                    
        sock.close()