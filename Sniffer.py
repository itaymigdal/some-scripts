import argparse
import ipaddress
from sys import argv
from scapy.all import *
from scapy.layers.inet import TCP, UDP, ICMP, IP


script_banner = """


|\ |   _   _|_       _    _  |       (~   _   .   |`   |`   _    _                         
| \|  (/_   |   VV  (_)  |   |<      _)  | |  |  ~|~  ~|~  (/_  |                          
                                                                                           
                                                                                        
"""


def print_end():
    # print statistics at the end
    print()
    print("##############################################################\n")
    print("########################  STATISTICS  ########################\n")
    print("##############################################################\n")
    # sort dict
    sorted_connectios = {conn: count for conn, count in reversed(sorted(connections.items(), key=lambda item: item[1]))}
    for conn in sorted_connectios:
        # store variables
        src = conn.split(":")[0]
        dst = conn.split(":")[1]
        prt = conn.split(":")[2]
        # conection string to print
        conn_str = "[*] {} : {} --> {}".format(prt, src, dst)
        # print connection string and count as table
        print(conn_str.ljust(50), "Count = ", sorted_connectios[conn], "\n")
    print("##############################################################\n")


def print_stats(source_ip, destination_ip, protocol_pkt):
    # generate unique key for each connection (src + dst + prt)
    unique_key = source_ip + ":" + destination_ip + ":" + protocol_pkt
    if unique_key in connections:
        # if already sniffed - count + 1
        connections[unique_key] += 1
    else:
        # new packet- add to dictionary
        connections.update({unique_key: 1})
    # print each packet
    print("[+]", protocol_pkt, ":", source_ip, " --> ", destination_ip)


def packet(pkt):
    try:
        # store fields and decide wich protocol
        source_ip = pkt.getlayer(IP).src
        destination_ip = pkt.getlayer(IP).dst
        # check if need to exclude packet
        if exclude == "in" and ipaddress.ip_address(destination_ip).is_private:
            return
        elif exclude == "out" and ipaddress.ip_address(source_ip).is_private:
            return
        else:
            if pkt.haslayer(TCP):
                protocol_pkt = "TCP"
            elif pkt.haslayer(UDP):
                protocol_pkt = "UDP"
            elif pkt.haslayer(ICMP):
                protocol_pkt = "ICMP"
            else:
                protocol_pkt = "OTHER"
            # call function to print packet and get stats
            print_stats(source_ip, destination_ip, protocol_pkt)
    except:
        # on error skip
        return


def start_sniff():
    if protocol == "":
        # sniff all
        print("\n[*] Start sniffing... (exclude: {})".format(exclude), "\n")
    else:
        # sniff with filter
        print("\n[*] Start sniffing {} packets... (exclude: {})".format(protocol.upper() ,exclude), "\n")
    # sniff function
    sniff(filter=protocol, prn=packet)


def main():
    # global connections dictionaty, and arguments statements
    global connections, protocol, exclude
    connections = {}
    # building arguments parser
    parser = argparse.ArgumentParser(description="sniff network traffic and finally print statistics",
                                     epilog="----------------------------------------------------------------------------")
    parser.add_argument("-protocol", help="filter packets by this protocol ",
                        required=False, default="", metavar="<tcp/udp/icmp>", choices=["tcp", "udp", "icmp"])
    parser.add_argument("-exclude", help="exclude incoming or outgoing connections", required=False, metavar="<in/out>", choices=["in", "out"])
    args = parser.parse_args()
    # store variables
    protocol = args.protocol
    exclude = args.exclude
    try:
        # start sneef
        start_sniff()
    except KeyboardInterrupt:
        pass
    finally:
        # at CTRL^C print statistics
        print_end()


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv:
        print(script_banner)
    main()