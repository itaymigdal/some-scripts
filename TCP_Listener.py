import socket
import argparse


def listener(port, output_file_name):
    # create socket: AF_INET for IPV4, SOCK_STREAM for TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connsock:
        server_address = ('localhost', port)
        connsock.bind(server_address)
        connsock.settimeout(2)
        print("\n[+] Created socket on port {}.".format(port))
        # open log file for writing
        with open(output_file_name, "w+") as output_file:
            # listen for incoming connection
            connsock.listen(0)
            while True:
                try:
                    connection, client_address = connsock.accept()
                    incoming_string = "\n[*] Incoming connection from {}".format(client_address)
                    print(incoming_string)
                    output_file.write(incoming_string + "\n")
                    while True:
                        print(".")
                        data = connection.recv(1)
                        if data:
                            output_file.write(data.decode("utf-8"))
                        else:
                            stopped_string = "\n[*] Connection stopped from {}".format(client_address)
                            print(stopped_string)
                            output_file.write(stopped_string)
                            break
                except socket.timeout:
                    continue

def main():
    # parse the command line arguments
    parser = argparse.ArgumentParser(description="TCP Listener ", formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="-----------------------------------------------------------------")
    parser.add_argument("-port", metavar="<PORT>", type=int, help="The port to Listen \nDefault = 80", default=80)
    parser.add_argument("-output", metavar="<FILE PATH>", help=r"Output file (Default= c:\TCP_Listener.log)",
                        type=str, default=r'c:\TCP_Listener.log')
    args = parser.parse_args()
    # store variables
    port = args.port
    output_file_name = args.output
    listener(port, output_file_name)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Script interrupted by user.\n")
        exit(1)
