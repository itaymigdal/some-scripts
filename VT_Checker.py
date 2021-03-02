import os
import hashlib
import vt
import traceback
from sys import argv
from tabulate import tabulate

vt_api_key = "PUT YOUR VT API KEY HERE"


def print_stats(file, vt_answer):
    stats = vt_answer.last_analysis_stats
    info_table = [
        ("File name", file),
        ("Size", vt_answer.size),
        ("MD5", vt_answer.md5),
        ("SHA1", vt_answer.sha1),
        ("SHA256", vt_answer.sha256),
        ("Malicious", stats['malicious']),
        ("Undetected", stats['undetected'])
    ]
    print("\n#################################################################################")
    print(tabulate(info_table, tablefmt="grid"))
    print("#################################################################################")


def print_help():
    print("\nUsage: py {} <path>\n".format(argv[0]))


def get_file_hash(file):
    sha256 = hashlib.sha256()
    with open(file, 'rb') as file_:
        buffer = file_.read()
    sha256.update(buffer)
    return sha256.hexdigest()


def parse_and_print(vt_answer):
    vt_table = []
    for engine in vt_answer:
        vt_table.append((engine, vt_answer[engine]['result']))
    print("")
    print(tabulate(vt_table, headers=["ENGINE", "RESULT"], tablefmt="grid"))
    print("")


def main():
    if len(argv) != 2 or not os.path.isfile(argv[1]):
        print_help()
        return
    vt_client = vt.Client(vt_api_key)
    file_hash = get_file_hash(argv[1])
    try:
        vt_answer = vt_client.get_object("/files/{}".format(file_hash))
    except vt.APIError:
        print("[-] ERROR: Could not Found Item on VT.")
        exit(0)
    finally:
        vt_client.close()
    print_stats(os.path.basename(argv[1]), vt_answer)
    parse_and_print(vt_answer.last_analysis_results)
    vt_client.close()


main()
