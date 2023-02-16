import sys
import getopt
from server.server import Server


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:p:l:")
    except getopt.GetoptError:
        print("lightserver -p <PORT> -l <LOG FILE LOCATION>")
        sys.exit(2)

    sv = Server()

    for opt, args in opts:
        if opt == "-h":
            print("lightserver -p <PORT> -l <LOG FILE LOCATION>")
            sys.exit()
        elif opt == "-s":
            sv.ip = args
        elif opt == "-p":
            sv.port = args
        elif opt == "-l":
            sv.log = args

    print("IP is ", sv.ip)
    print("PORT is ", sv.port)
    print("LOG file is ", sv.log)


if __name__ == "__main__":
    main(sys.argv[1:])

