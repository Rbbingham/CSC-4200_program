from multipledispatch import dispatch


class Server:
    """

    """

    @dispatch()
    def __init__(self) -> None:
        self.__ip: str = ""
        self.__port: int = 0
        self.__log_location: str = ""

    @dispatch(str, int, str)
    def __init__(self, ip: str, port: int, log: str):
        self.__ip: str = ip
        self.__port: int = int(port)
        self.__log_location: str = log

    @property
    def ip(self) -> str:
        return self.__ip

    @property
    def port(self) -> int:
        return self.__port

    @property
    def log(self) -> str:
        return self.__log_location

    @ip.setter
    def ip(self, ip: str) -> None:
        self.__ip = ip

    @port.setter
    def port(self, port: int) -> None:
        self.__port = port

    @log.setter
    def log(self, log: str) -> None:
        self.__log_location = log

