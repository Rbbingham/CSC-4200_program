import sys
import getopt
from client.client import Client


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:p:l:")
    except getopt.GetoptError:
        print("lightclient -s <SERVER IP> -p <PORT> -l <LOG FILE LOCATION>")
        sys.exit(2)

    con = Client()

    for opt, args in opts:
        if opt == "-h":
            print("lightclient -s <SERVER IP> -p <PORT> -l <LOG FILE LOCATION>")
            sys.exit()
        elif opt == "-s":
            con.ip = args
        elif opt == "-p":
            con.port = args
        elif opt == "-l":
            con.log = args

    con.conserver()


if __name__ == "__main__":
    main(sys.argv[1:])

