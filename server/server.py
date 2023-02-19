from multipledispatch import dispatch
import socket


class Server:
    """

    """

    @dispatch()
    def __init__(self) -> None:
        self.__port: int = 0
        self.__log_location: str = ""

    @dispatch(str, int, str)
    def __init__(self, ip: str, port: int, log: str) -> None:
        self.__port: int = int(port)
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

        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.bind((HOST, self.__port))

        mysocket.listen()
        print("Listening")

        INCONN, INADDR = mysocket.accept()
        print("Incoming connection {}{} = ".format(INCONN, INADDR))

        with INCONN:
            while True:
                data = INCONN.recv(1024)
                print("Received data of length {}".format(len(data)))

                if not data:
                    print("Communication ended")
                    break

                print("Echoing back")
                INCONN.sendall(data)