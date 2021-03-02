from shodan import Shodan, APIError
import argparse
import colorama

# initiate Shodan
def init():
    # set API key
    api_key = "PUT YOUR SHODAN API LEY HERE"
    # define and init global API object
    global api
    api = Shodan(api_key)


# prints API error
def print_error(e):
    print(colorama.Fore.RED + '\nError: {}\n'.format(e))


# print scan credits and query credits
def print_credits():
    try:
        info = api.info()
        print("\n[*] scan credits: {} \n[*] query credits: {}\n".format(info['scan_credits'], info['query_credits']))
    except APIError as e:
        print_error(e)


# prints my external IP
def print_my_ip():
    try:
        result = api.tools.myip()
        print("\n[+] my ip: {}\n".format(result))
    except APIError as e:
        print_error(e)


# prints a list of IP's matches the query - consumes 1 query credit if: 1.qurey contains filter. 2.accessing results past the 1st page.
def query_ips(search_query):
    try:
        # create list for ip's
        ips = []
        # Search Shodan
        results = api.search(search_query)
        # print total IP's found
        print('\n[*] IP\'s found: {}\n'.format(results['total']))
        # appent IP's to the list
        for result in results['matches']:
            ips.append(result['ip_str'])
        # Print IP's
        for ip in ips:
            print("[+]", ip)
        print("")
    except APIError as e:
        print_error(e)


# prints all services that have been found on the given host IP.
def query_host(ip):
    try:
        # Lookup the host
        host = api.host(ip)
        # Print general info
        print("""
        
           #########################################
                IP: {}
                Organization: {}
                Operating System: {}
           #########################################
                
                
        """.format(host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))
        # Print all banners
        for item in host['data']:
            print("[+] Port: {}".format(item['port']))
            print("[+] Banner: ")
            for line in item['data'].splitlines():
                print("\t\t", line)
            print("")
    except APIError as e:
        print_error(e)


def main():
    # init colorama for print in color
    colorama.init(autoreset=True)
    # build argument parser
    parser = argparse.ArgumentParser(description="Shodan API functions",
                                     epilog="----------------------------------------------------------------------------")
    main_group = parser.add_mutually_exclusive_group()
    main_group.add_argument("-pc", help="prints scan and query credits", action="store_true")
    main_group.add_argument("-pi", help="prints my external IP", action="store_true")
    main_group.add_argument("-query", metavar="<QUERY>", help="prints a list of IP's matches the query", type=str)
    main_group.add_argument("-host", metavar="<IP>", help="prints all services that have been found on the given host",
                            type=str)
    args = parser.parse_args()
    # initiate shodan API
    init()
    if args.pc:
        print_credits()
    if args.pi:
        print_my_ip()
    if args.query:
        query_ips(args.query)
    if args.host:
        query_host(args.host)


if __name__ == '__main__':
    main()
