import requests
import argparse
import os
import time
from sys import argv

script_banner = """


         _____  _____  ___                              
  /\  /\/__   \/__   \/ _ \   ___ _ __  _   _ _ __ ___  
 / /_/ /  / /\/  / /\/ /_)/  / _ \ '_ \| | | | '_ ` _ \ 
/ __  /  / /    / / / ___/  |  __/ | | | |_| | | | | | |
\/ /_/   \/     \/  \/       \___|_| |_|\__,_|_| |_| |_|
                                                        



"""


def check(url, line):
    request = "{}/{}".format(url, line)
    response = requests.get(request)
    if response.status_code == 404:
        return 404, None
    size = len(response.content)
    status_code = response.status_code
    return status_code, size



def enum(url, file, timeout):
    print("\n[*] HTTP_Enum starting...\n")
    with open(file) as extentions:
        # count lines in file
        total = len(extentions.readlines())
        # how many lines have been tried
        count = 0
        # go back to line 0
        extentions.seek(0)
        # read each line
        for lineW in extentions:
            # remove spaces
            line = lineW.strip()
            # call check
            status_code, size = check(url, line)
            # + 1 line
            count = count + 1
            # extention found
            if status_code != 404:
                print("[+] [{}] [Size:{}]".format(status_code, size).ljust(24), "{}/{}                                   \n".format(url, line))
                continue
            else:
                # no match
                print("[*] [{}%] TESTING --> /{}                            ".format(int(100 * (count / total)), line), end="\r\r\r")
                # sleep timeout
                time.sleep(timeout)
                continue
    # end of file
    print("[*] HTTP_Enum finished.                                                                                       \n")
    return


def main():
    # Building arguments
    parser = argparse.ArgumentParser(description="HTTP enumaretion / forced browse",
                                     epilog="--------------------------------------------------------------------")
    main_group = parser.add_argument_group("arguments")
    main_group.add_argument("-url", metavar="<URL>", help="Base URL", required=True)
    main_group.add_argument("-F", metavar="<EXTENTIONS FILE>", help="Extentions file to use ")
    main_group.add_argument("-T", metavar="<SECONDS>", type=float, help="Timeout between each request (default: none)",
                            default=0)
    args = parser.parse_args()
    # store variables
    url = args.url
    file = args.F
    timeout = args.T
    # validate URL
    if requests.get(url).status_code != 200:
        print("\n[-] Invalid url\n")
        return
    # validate file
    if not os.path.isfile(file):
        print(file)
        print("\n[-] Invalid file\n")
        return
    # call Enum function
    enum(url, file, timeout)


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv or len(argv) == 1:
        print(script_banner)
    try:
        # start script
        main()
    except KeyboardInterrupt:
        print("[*] script interrupted by user.                                            \n")
        exit(0)
