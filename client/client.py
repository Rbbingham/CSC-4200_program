from multipledispatch import dispatch


class Client:
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
