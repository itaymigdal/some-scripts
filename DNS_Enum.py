import argparse
import os
from sys import argv
from dns import *

script_banner = """

______ _   _  _____   _____                      
|  _  \ \ | |/  ___| |  ___|                     
| | | |  \| |\ `--.  | |__ _ __  _   _ _ __ ___  
| | | | . ` | `--. \ |  __| '_ \| | | | '_ ` _ \ 
| |/ /| |\  |/\__/ / | |__| | | | |_| | | | | | |
|___/ \_| \_/\____/  \____/_| |_|\__,_|_| |_| |_|                                              

"""


def dns_bruter(domain, sd_file_path):
    print("[*] Trying Subdomain Enumaration...")
    with open(sd_file_path, "rt") as sd_path:
        print("")
        for line in sd_path:
            subdomain = line.strip() + "." + domain
            try:
                answer = resolver.query(subdomain, "A")[0]
                print("[+] Found subdomain: [{} | {}]".format(answer, subdomain))
            except:
                continue
        print("")


def dns_zt(domain):
    print("[*] Trying Zone-Tranfer Attack...")
    try:
        ns_servers = resolver.query(domain, "NS")
    except:
        print("[-] WRONG INPUT: This is not a valid super domain.")
        exit(1)
    for ns_server in ns_servers:
        ns_server = str(ns_server)[:-1]
        try:
            zone_transfer = zone.from_xfr(query.xfr(ns_server, domain))
            names = zone_transfer.nodes.keys()
            print("[+] Zone-Tranfer Attack succeeded!\n")
            for n in names:
                print(zone_transfer[n].to_text(n))
            print("")
            return True
        except:
            continue
    print("[-] Zone-Tranfer Attack Failed.")
    return False


def validations(args):
    if args.SD is None and args.OZT is True:
        print("[-] WRONG INPUT: Ommit zone-Transfer and no File to enumarate with.")
        exit(1)
    if args.SD and not os.path.isfile(args.SD):
        print("[-] WRONG INPUT: Invalid file.")
        exit(1)


def main():
    # arguments
    parser = argparse.ArgumentParser(description="Subdomains Enumaration and Zone Transfer Check")
    parser.add_argument("-D", metavar="<DOMAIN>", help="Domain to Brute-Force", required=True, type=str)
    parser.add_argument("-SD", metavar="<FILE>", help="SubDomains file to Brute with", type=str, required=False,
                        default=None)
    parser.add_argument("-OZT", action="store_true", help="Ommit Zone-Transfer")
    # parse arguments
    args = parser.parse_args()
    # validate arguments
    validations(args)
    # variable for zone transfer success, if True - then no need to brute force sub domains
    zt_success = False
    # if not ommit it, call dns zone transfer function
    if args.OZT is False:
        zt_success = dns_zt(args.D)
    # if zone transfer failed and a subdomains file supplied
    if args.SD and not zt_success:
        dns_bruter(args.D, args.SD)


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv or len(argv) == 1:
        print(script_banner)
    try:
        # start script
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)
