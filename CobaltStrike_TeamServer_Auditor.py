import hashlib
import argparse
import requests
import socket
import ssl
import dns.resolver
from sys import argv


script_banner = """
   _____      _           _ _      _____ _        _ _           _____                                              _ _ _             
  / ____|    | |         | | |    / ____| |      (_) |         / ____|                              /\            | (_) |            
 | |     ___ | |__   __ _| | |_  | (___ | |_ _ __ _| | _____  | (___   ___ _ ____   _____ _ __     /  \  _   _  __| |_| |_ ___  _ __ 
 | |    / _ \| '_ \ / _` | | __|  \___ \| __| '__| | |/ / _ \  \___ \ / _ \ '__\ \ / / _ \ '__|   / /\ \| | | |/ _` | | __/ _ \| '__|
 | |___| (_) | |_) | (_| | | |_   ____) | |_| |  | |   <  __/  ____) |  __/ |   \ V /  __/ |     / ____ \ |_| | (_| | | || (_) | |   
  \_____\___/|_.__/ \__,_|_|\__| |_____/ \__|_|  |_|_|\_\___| |_____/ \___|_|    \_/ \___|_|    /_/    \_\__,_|\__,_|_|\__\___/|_|   
                                                                                                                                                                                                                                                                                                                                                                                                                                                       
"""


def check_dns_response(ip):
    port = 53
    test_hostname = "cnn.com"
    excepted_answer = "0.0.0.0"

    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        answer = resolver.query(test_hostname, "A")[0].to_text()
    except Exception:
        print(f"[-] Could not query host [{ip}:{port}]")
        return

    if answer == excepted_answer:
        print(f"[+] Retrieved default DNS answer from [{ip}:{port}]!")
        return
    else:
        print(f"[-] No default DNS answer from [{ip}:{port}]")


def check_ssl_certificate(ip):

    port = 443
    default_sha256_fingerprints = ["87f2085c32b6a2cc709b365f55873e207a9caa10bffecf2fd16d3cf9d94d390c"]

    try:
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        ssl_socket = ssl.wrap_socket(sock)
        ssl_socket.connect((ip, port))
        der_cert_bin = ssl_socket.getpeercert(True)
        pem_cert = ssl.DER_cert_to_PEM_cert(ssl_socket.getpeercert(True))
        sha256_fingerprint = hashlib.sha256(der_cert_bin).hexdigest()
        ssl_socket.close()
    except Exception:
        print(f"[-] Could not retrieve SSL certificate from [{ip}:{port}]")
        return
    for default_sha256_fingerprint in default_sha256_fingerprints:
        if sha256_fingerprint == default_sha256_fingerprint:
            print(f"[+] Found default SSL certificate at [{ip}:{port}]!")
        else: 
            print(f"[-] No default SSL certificate at [{ip}:{port}] ")


def check_http_response(ip, port):
    if port == 80:
        protocol = "http"
    elif port == 443:
        protocol = "https"
    try:
        response = requests.get(f"{protocol}://{ip}:{port}/", verify=False)
        if response.status_code == 404 and response.headers["Content-Type"] == "text/plain":
            print(f"[+] Found Cobalt Strike default {protocol} response at [{ip}:{port}]!")
        else:
            print(f"[-] No default {protocol} response at [{ip}:{port}]")        
            return
    except Exception:
        print(f"[-] Could not retrieve {protocol} response at [{ip}:{port}]")
        return



def check_teamserver(ip):
    teamserver_port = 50050
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, teamserver_port))
        print(f"[+] Found Cobalt Strike default teamserver port at [{ip}:{teamserver_port}]!")
        return
    except (ConnectionRefusedError, TimeoutError, socket.timeout):
        print(f"[-] No default teamserver port running at [{ip}:{teamserver_port}]")
        return 


def scan_target(target):
    print(f"-------======= Scanning [{target}] =======-------")
    try:
        ip = socket.gethostbyname(target)
    except:
        print(f"[X] Could not Resolve host {target}\n")
        return
    check_teamserver(ip)
    check_ssl_certificate(ip)
    check_http_response(ip, 443)
    check_http_response(ip, 80)
    check_dns_response(ip)


def main():
    # Build Arguments
    parser = argparse.ArgumentParser(description="Cobalt Strike Server Audit Tool")
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("-f", metavar="<path>", help="file containing targets (ipv4/fqdn) to audit")
    input_group.add_argument("-t", metavar="<target>", help="single target (ipv4/fqdn) to audit")
    args = parser.parse_args()
    # parse targets
    if args.f:
        with open(args.f) as input_file_h:
            targets = input_file_h.readlines()
    else:
        targets = [args.t]
    
    for target in targets:
        scan_target(target.strip())       


if __name__ == "__main__":
    print(script_banner)
    try:
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.\n")
        exit(0)
