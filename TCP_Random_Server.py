import argparse
import requests
import ipaddress
from sys import argv
from scapy.all import *
from scapy.layers.inet import IP, TCP
from random import randint
from concurrent.futures import ThreadPoolExecutor
from tabulate import tabulate


script_banner = """


  ________________     ____                  __                   _____                          
 /_  __/ ____/ __ \   / __ \____ _____  ____/ /___  ____ ___     / ___/___  ______   _____  _____
  / / / /   / /_/ /  / /_/ / __ `/ __ \/ __  / __ \/ __ `__ \    \__ \/ _ \/ ___/ | / / _ \/ ___/
 / / / /___/ ____/  / _, _/ /_/ / / / / /_/ / /_/ / / / / / /   ___/ /  __/ /   | |/ /  __/ /    
/_/  \____/_/      /_/ |_|\__,_/_/ /_/\__,_/\____/_/ /_/ /_/   /____/\___/_/    |___/\___/_/     
                                                                                                 

"""


# Global results to restore [IP, PORT]
results = []
results_geo = []


def scan_port_thread(ports, count, verbose):
    # Declare global results
    global results
    syn = 0x02
    syn_ack = 0x12
    rst_ack = 0x14
    # While we need more results
    while len(results) <= count:
        # generate new IP
        ip = str(random.randint(1, 255)) + "." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255))
        if not ipaddress.IPv4Address(ip).is_global:
            continue
        # Randomize source port
        srcport = randint(1, 1024)
        # choose random port from ports
        port = int(ports[randint(0, (len(ports) - 1))])
        # send and receive
        response = sr1(IP(dst=ip) / TCP(sport=srcport, dport=port, flags=syn), timeout=1.5, verbose=0)
        # check port status and print if verbose
        if (response is None or not response.haslayer(TCP)) and len(results) < count:
            if verbose:
                print("[-] [{}:{}] is filtered or host is down.".format(ip, port))
            continue
        response_flags = response.getlayer(TCP).flags
        if response_flags == syn_ack and len(results) < count:
            results.append((ip, port))
            print("[+] [{}:{}] is open (flags = SYN + ACK).".format(ip, port))
        else:
            if response_flags == rst_ack and len(results) < count:
                if verbose:
                    print("[-] [{}:{}] is closed (flags= RST + ACK).".format(ip, port))



def add_geo(verbose):
    for result in results:
        try:
            if verbose:
                print("[*] Getting geolocation for {}.".format(result[0]))
            base_url = "http://ip-api.com/json/"
            response = requests.get(base_url + result[0])
            response = response.json()
            location = "{}, {}, {}".format(response["country"], response["regionName"], response["city"])
            results_geo.append((result[0], result[1], location))
        except Exception:
            print("[-] Error: could not retrieve or parse geolocation response for {}.".format(result[0]))
            results_geo.append((result[0], result[1], "-"))
            continue


def main():
    # Declare global results
    global results
    # parse the command line arguments
    parser = argparse.ArgumentParser(description="Scan the network for random servers",
                                     epilog="****************************************************************")
    parser.add_argument("-ports", metavar="<PORT>", type=str, help="Open ports to search (comma-seperated)",
                        required=True)
    parser.add_argument("-count", metavar="<INT>", type=int, help="How many results to retrieve (Default= 1)",
                        default=1)
    parser.add_argument("-threads", metavar="<INT>", type=int, help="Number of Threads (Default= 50)", default=50)
    parser.add_argument("-output", metavar="<FILE PATH>", type=str, help="Store addresses in file", default=None)
    parser.add_argument("-geo", action="store_true", help="Add geo-location to results", required=False)
    parser.add_argument("-v", action="store_true", help="Verbose")
    args = parser.parse_args()
    # store variables
    threads = args.threads
    ports = args.ports.split(",")
    count = args.count
    geo = args.geo
    verbose = args.v
    output_path = args.output
    if output_path:
        output_path = r'{}'.format(os.path.realpath(output_path))
    print("\n[*] TCP_Random_Server is starting with {} threads...\n".format(threads))
    # Execute Threads
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(scan_port_thread, ports, count, verbose)
    # write output to file
    if output_path:
        if verbose:
            print("[*] Writing output to {}".format(output_path))
        with open(output_path, "w") as output:
            output.write("# TCP_Random_Server report (ports: {}).\n\n".format(args.ports))
            for result in results:
                output.write("{}\n".format(result[0]))
    # if geo supplied, add geolocation to results
    if geo:
        add_geo(verbose)
        # print results (with geo)
        print("\n***************************************************************************\n")
        print(tabulate(results_geo, headers=["IP", "PORT", "LOCATION"], tablefmt="psql", showindex=True))
        print("\n***************************************************************************\n")
    else:
        # print results
        print("\n*********************************\n")
        print(tabulate(results, headers=["IP", "PORT"], tablefmt="psql", showindex=True))
        print("\n*********************************\n")


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv or len(argv) == 1:
        print(script_banner)
    try:
        # start script
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)
