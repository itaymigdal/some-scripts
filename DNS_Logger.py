from scapy.all import *
from datetime import datetime


def packet(pkt):
    # if had dns layer and is not a dns response
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if pkt.haslayer(DNS) and not (pkt[DNS].an or pkt[DNS].ns or pkt[DNS].ar):
        print(f"[{time}] [-> {pkt[IP].dst}] {pkt[DNS].qd.qname.decode()[:-1]}")


if __name__ == "__main__":
    try:
        sniff(prn=packet, filter="port 53")
    except KeyboardInterrupt:
        exit()