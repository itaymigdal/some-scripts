from gooey import Gooey
from googlesearch import search
import argparse


# Gooey Decorator
@Gooey(program_name="Google Dorks Explorer",
       program_description="GUI Program for google dorking without open the browser :)",
       default_size=(1000, 800), terminal_font_size=12, show_exit_warning=False, show_success_modal=False,
       show_failure_modal=False, show_stop_warning=False, clear_before_run=True, disable_stop_button=True)
def main():
    # Define arguments
    parser = argparse.ArgumentParser()
    operators_parser = parser.add_argument_group("Optional Operators")
    operators_parser.add_argument("-inurl", help="OR logic, comma-separated (no space)")
    operators_parser.add_argument("-and-inurl", help="AND logic, comma-separated (no space)")
    operators_parser.add_argument("-not-inurl", help="AND logic, comma-separated (no space)")
    operators_parser.add_argument("-intext", help="OR logic, each phrase in quotations, comma-separated (no space)")
    operators_parser.add_argument("-and-intext", help="AND logic, each phrase in quotations, comma-separated (no space)")
    operators_parser.add_argument("-not-intext", help="AND logic, each phrase in quotations, comma-separated (no space)")
    operators_parser.add_argument("-intitle", help="OR logic, each phrase in quotations, comma-separated (no space)")
    operators_parser.add_argument("-not-intitle", help="AND logic, each phrase in quotations, comma-separated (no space)")
    operators_parser.add_argument("-filetype", help="OR logic, comma-separated (no space)")
    operators_parser.add_argument("-not-filetype", help="AND logic, comma-separated (no space)")
    operators_parser.add_argument("-site", help="OR logic, comma-separated (no space)")
    operators_parser.add_argument("-not-site", help="AND logic, comma-separated (no space)")
    operators_parser.add_argument("-query", help="Add terms manually or full query")
    # parse arguments and make them dict
    args = vars(parser.parse_args())
    # OR Operators
    or_operators = ["inurl", "intext", "filetype", "intitle", "site"]
    # Google query string
    query_string = ""
    # Parse operators and append to query string
    for arg in args:
        if args[arg] is not None:
            if arg in or_operators:
                for _ in args[arg].split(","):
                    query_string += "{}:{} | ".format(arg, _)
                query_string = query_string[:-2]
            else:
                for _ in args[arg].split(","):
                    query_string += "{}:{} ".format(arg, _)

    # Adjust query
    query_string = query_string.replace("not_", "-").replace("query:", "").replace("and_", "")[:-1]
    # Print query
    print('[*] Googling [{}] ...\n'.format(query_string))
    # Google search
    results = search(query_string, num_results=100)
    # Print results
    if len(results) == 0:
        print("[-] Sorry, no results :(")
        return
    else:
        i = 1
        for result in results:
            print("[{}]".format(i), result)
            i += 1


main()
