import argparse
from scapy.all import *
from scapy.layers.inet import IP, UDP, ICMP
from random import randint
from sys import argv
from time import sleep

script_banner = """

  

   __  ______  ____     _____                                 
  / / / / __ \/ __ \   / ___/_________ _____  ____  ___  _____
 / / / / / / / /_/ /   \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
/ /_/ / /_/ / ____/   ___/ / /__/ /_/ / / / / / / /  __/ /    
\____/_____/_/       /____/\___/\__,_/_/ /_/_/ /_/\___/_/     
                                                              


"""


common_ports = """
            53,67,68,69,123,135,137,138,139,161,162,445,500,514,520,631,1434,1900,4500,49152
"""


def scan_port(target, port, verbose):
    srcport = randint(1, 1024)
    response = sr1(IP(dst=target) / UDP(sport=srcport, dport=port), verbose=0, timeout=0.5)
    if response is None:
        if verbose:
            print("[+] [{}:{}] is open / filtered.".format(target, port))
        return "O"
    if ICMP in response:
        if verbose:
            print("[+] [{}:{}] is Closed.".format(target, port))
        return "C"


def main():
    # parse the command line arguments
    parser = argparse.ArgumentParser(description="UDP scanner ", formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="----------------------------------------------------------------------")
    parser.add_argument("-address", metavar="<ADDRESS>", type=str, required=True,
                        help="The target address <ip> / <hostname> / <domain>")
    parser.add_argument("-ports", metavar="<PORTS>", type=str, help="The ports to scan\n<*> - top 20 common UDP ports", required=True)
    parser.add_argument("-t", metavar="<SECONDS>", help="Timeout between each request", type=float, default=0)
    parser.add_argument("-v", action="store_true", help="verbose")
    args = parser.parse_args()
    # store variables
    target = args.address
    ports = args.ports
    verbose = args.v
    timeout = args.t
    if ports == "*":
        ports = common_ports
    # split ports
    ports = ports.split(',')
    closed_ports = list()
    open_ports = list()
    print("\n[*] UDP Scanner starting...\n")
    for port in ports:
        sleep(timeout)
        res = scan_port(target, int(port), verbose)
        if res == "C":
            closed_ports.append(int(port))
        elif res == "O":
            open_ports.append(int(port))
    print("\n*************************************************\n")
    print("[*] Ports status for [{}]:\n".format(target))
    print("[+] Open / Filtered ports:  {}\n".format(open_ports))
    print("[+] Closed ports: {}".format(closed_ports))
    print("\n*************************************************\n")


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv or len(argv) == 1:
        print(script_banner)
    try:
        # start script
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)
