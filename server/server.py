import socket
from packet.packet import Packet
import RPi.GPIO as GPIO


class Server:
    """

    """

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
        HOST = "127.0.0.1"
        PIN = -99

        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.bind((HOST, self.__port))

        mysocket.listen()

        while True:
            INCONN, INADDR = mysocket.accept()

            with INCONN:
                print("Received connection from (IP, PORT): {}".format(INADDR))
                while True:
                    data = INCONN.recv(1024)

                    if not data:
                        break

                    try:
                        PIN, command = Packet.unpack('!ii', data)
                    except:
                        print("Bad input")
                        pass

            if PIN != -99:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(PIN, GPIO.OUT)

                if command == "LIGHTON":
                    GPIO.output(PIN, GPIO.HIGH)
                elif command == "LIGHTOFF":
                    GPIO.output(PIN, GPIO.LOW)
