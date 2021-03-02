from scapy.all import *
from scapy.layers.l2 import Ether, ARP
from tabulate import tabulate
from sys import argv
import argparse
import ipaddress
import socket


banner = """
                       

           _____  _____    _   _      _                      _       _____                                 
     /\   |  __ \|  __ \  | \ | |    | |                    | |     / ____|                                
    /  \  | |__) | |__) | |  \| | ___| |___      _____  _ __| | __ | (___   ___ __ _ _ __  _ __   ___ _ __ 
   / /\ \ |  _  /|  ___/  | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ /  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
  / ____ \| | \ \| |      | |\  |  __/ |_ \ V  V / (_) | |  |   <   ____) | (_| (_| | | | | | | |  __/ |   
 /_/    \_\_|  \_\_|      |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\ |_____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                               
"""


# function for getting (MAC, IP) of default NIC for scapy (only windows)
def get_default_interface():
    # get MAC of default NIC
    my_default_mac = Ether().src
    # getting all NIC's
    interfaces = get_windows_if_list()
    # get IP of my_default_mac
    for i in interfaces:
        if i['mac'] == my_default_mac:
            for ip in i['ips']:
                if 'IPv4Address' in str(type(ipaddress.ip_address(ip))):
                    my_default_ip = ip
    return my_default_mac, my_default_ip


# ARP scanning for subnet/address
def check_subnet(subnet):
    answers, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet), timeout=2, verbose=0)
    return answers


def main():
    # Building arguments
    parser = argparse.ArgumentParser(description="Network ARP Scanner", epilog="----------------------------------------------------")
    parser.add_argument("-s", metavar="<SUBNET>", help="Subnet to scan (Default: 10.0.0.0/24)", default="10.0.0.0/24")
    args = parser.parse_args()
    subnet = args.s
    # list of ARP answers
    answers_list = []
    # get (mac, ip, hostname) of default NIC
    my_mac, my_ip = get_default_interface()
    my_hostname = socket.gethostname()
    # add (mac, ip, hostname) of default NIC answers_list
    answers_list.append((my_mac, my_ip, my_hostname))
    # get answers of subnet
    answers = check_subnet(subnet)
    for answer in answers:
        ip = answer[1].psrc
        mac = answer[1].hwsrc
        try:
            # try to resolve hostname
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = None
        # add (mac, ip, hostname) to answers_list
        answers_list.append((mac, ip, hostname))
    # print using tabulate module
    print(tabulate(answers_list, headers=["MAC", "IP", "Hostname"], tablefmt="psql", showindex=True))
    print("\n")


if __name__ == "__main__":
    print(banner)
    try:
        # start script
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)
