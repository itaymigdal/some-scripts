import argparse
import ipaddress
from scapy.all import *
from scapy.layers.inet import IP, TCP
from random import randint
from concurrent.futures import ThreadPoolExecutor
import requests


def try_put(ip):
    try:
        url = "http://{}/index.txt".format(ip)
        response = requests.put(url)
        if response.status_code in [201, 204]:
            print("\n[+] PUT SUCCESS! URL: {}\n".format(url))
            return
    except Exception:
        return


def check_options(ip, verbose):
    try:
        response = requests.options('http://{}'.format(ip))
        if 'PUT' in response.headers['Allow']:
            if verbose:
                print("[*] PUT in OPTIONS response from [{}:80].".format(ip, response.headers['Allow']))
            try_put(ip)
        return
    except Exception:
        return


def scan_port_thread(port, count, verbose):
    syn = 0x02
    syn_ack = 0x12
    # While we need more results
    while True:
        # generate new IP
        ip = str(random.randint(1, 255)) + "." + str(random.randint(0, 255)) + "." + str(
            random.randint(0, 255)) + "." + str(random.randint(0, 255))
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
            check_options(ip, verbose)


def main():
    # parse the command line arguments
    parser = argparse.ArgumentParser(description="Discover HTTP servers with PUT method enabled",
                                     epilog="****************************************************************")
    parser.add_argument("-count", metavar="<INT>", type=int, help="How many servers to retrieve (Default= 1)",
                        default=1)
    parser.add_argument("-threads", metavar="<INT>", type=int, help="Number of Threads (Default= 50)", default=50)
    parser.add_argument("-v", action="store_true", help="Print When PUT found in OPTIONS response")
    args = parser.parse_args()
    # store variables
    threads = args.threads
    port = 80
    count = args.count
    verbose = args.v
    print("\n[*] HTTP_PUT_Discover is starting with {} threads...\n".format(threads))
    # Execute Threads
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(scan_port_thread, port, count, verbose)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)
