import argparse
import ipaddress
from scapy.all import *
from scapy.layers.inet import IP, TCP
from random import randint
from concurrent.futures import ThreadPoolExecutor
import ftplib


script_banner = """


    ________________     ____  _                               
   / ____/_  __/ __ \   / __ \(_)_____________ _   _____  _____
  / /_    / / / /_/ /  / / / / / ___/ ___/ __ \ | / / _ \/ ___/
 / __/   / / / ____/  / /_/ / (__  ) /__/ /_/ / |/ /  __/ /    
/_/     /_/ /_/      /_____/_/____/\___/\____/|___/\___/_/     
                                                               

"""


servers_found = 0


def check_anonymous_server(ip, port):
    global servers_found
    ftp = ftplib.FTP()
    try:
        ftp.connect(ip, port=port, timeout=2)
        ftp.login("Anonymous", "password")
        files = ftp.nlst()
        if len(files) >= 1 and files != [".", ".."]:
            servers_found += 1
            print("\n\t[+] Found open FTP server (anonymous login) at [{}:{}] !".format(ip, port))
            print("\t[+] Files list: {}\n".format(files))
            ftp.quit()
        return
    except Exception:
        return


def scan_port_thread(port, count, verbose):
    # Declare global servers_found and vars
    global servers_found
    syn = 0x02
    syn_ack = 0x12
    # While we need more results
    while servers_found < count:
        # generate new IP
        ip = str(random.randint(1, 255)) + "." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255))
        if not ipaddress.IPv4Address(ip).is_global:
            continue
        # Randomize source port
        srcport = randint(1, 1024)
        # send and receive
        response = sr1(IP(dst=ip) / TCP(sport=srcport, dport=port, flags=syn), timeout=2, verbose=0)
        # if response is not valid
        if response is None or not response.haslayer(TCP):
            continue
        # get TCP flags
        response_flags = response.getlayer(TCP).flags
        # if port is open
        if response_flags == syn_ack:
            if verbose:
                print("[*] [{}:{}] is open. checking if an Anonymous FTP server...".format(ip, port))
            check_anonymous_server(ip, port)


def main():
    # Declare global servers_found
    global servers_found
    # parse the command line arguments
    parser = argparse.ArgumentParser(description="Discover open FTP servers (Anonymous login)",
                                     epilog="****************************************************************")
    parser.add_argument("-count", metavar="<INT>", type=int, help="How many servers to retrieve (Default= 1)", default=1)
    parser.add_argument("-threads", metavar="<INT>", type=int, help="Number of Threads (Default= 50)", default=50)
    parser.add_argument("-v", help="Print when open port found", action="store_true")
    args = parser.parse_args()
    # store variables
    threads = args.threads
    port = 21
    count = args.count
    verbose = args.v
    print("[*] FTP_Discover is starting with {} threads...\n".format(threads))
    # Execute Threads
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(scan_port_thread, port, count, verbose)


if __name__ == "__main__":
    print(script_banner)
    try:
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)