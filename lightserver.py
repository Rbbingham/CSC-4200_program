import sys
import getopt
from server.server import Server


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hp:l:")
    except getopt.GetoptError:
        print("lightserver -p <PORT> -l <LOG FILE LOCATION>")
        sys.exit(2)

    con = Server()

    for opt, args in opts:
        if opt == "-h":
            print("lightserver -p <PORT> -l <LOG FILE LOCATION>")
            sys.exit()
        elif opt == "-p":
            con.port = args
        elif opt == "-l":
            con.log = args

    con.createserver()


if __name__ == "__main__":
    main(sys.argv[1:])