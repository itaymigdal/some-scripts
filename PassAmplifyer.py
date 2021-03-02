import os
import argparse
from sys import argv

banner = """



  _____                                                      _                                    _   _    __                        
 |  __ \                                                    | |       /\                         | | (_)  / _|                       
 | |__) |   __ _   ___   ___  __      __   ___    _ __    __| |      /  \     _ __ ___    _ __   | |  _  | |_   _   _    ___   _ __  
 |  ___/   / _` | / __| / __| \ \ /\ / /  / _ \  | '__|  / _` |     / /\ \   | '_ ` _ \  | '_ \  | | | | |  _| | | | |  / _ \ | '__| 
 | |      | (_| | \__ \ \__ \  \ V  V /  | (_) | | |    | (_| |    / ____ \  | | | | | | | |_) | | | | | | |   | |_| | |  __/ | |    
 |_|       \__,_| |___/ |___/   \_/\_/    \___/  |_|     \__,_|   /_/    \_\ |_| |_| |_| | .__/  |_| |_| |_|    \__, |  \___| |_|    
  _                     _____   _                       __  __   _               _       | | _                   __/ |               
 | |              _    |_   _| | |                     |  \/  | (_)             | |      |_|| |                 |___/                
 | |__    _   _  (_)     | |   | |_    __ _   _   _    | \  / |  _    __ _    __| |   __ _  | |                                      
 | '_ \  | | | |         | |   | __|  / _` | | | | |   | |\/| | | |  / _` |  / _` |  / _` | | |                                      
 | |_) | | |_| |  _     _| |_  | |_  | (_| | | |_| |   | |  | | | | | (_| | | (_| | | (_| | | |                                      
 |_.__/   \__, | (_)   |_____|  \__|  \__,_|  \__, |   |_|  |_| |_|  \__, |  \__,_|  \__,_| |_|                                      
           __/ |                               __/ |                  __/ |                                                          
          |___/                               |___/                  |___/                                                           




"""


def validate_input_create_files(input_file_path, output_name, verbose):
    if verbose:
        print("[*] validating input...")
    try:
        # resolve directory path
        dir_path = r'{}'.format(os.path.dirname(os.path.realpath(input_file_path)))
        # if supplied non-txt file raise exception
        if not input_file_path.endswith('.txt'):
            raise
    except:
        # couldn't resolve path or file is not txt, print and exit
        print("[-] Wrong input file!\n")
        exit(0)
    # if not output name has'nt supplied - choose default
    if not output_name:
        output_name = "PassAmp_out.txt"
    else:
        # if output name isn't txt - make it txt
        if not output_name.endswith('.txt'):
            output_name = "{}.txt".format(output_name)
    # create full output file path
    output_file_path = r'{}\{}'.format(dir_path, output_name)
    if verbose:
        print("[*] creating output file: {}...".format(output_file_path))
    try:
        # create output file for write
        output_file = open(output_file_path, "w+")
    except:
        print("[-] Error creating output file: {}".format(output_file_path))
        exit(0)
    try:
        # open input file for read
        input_file = open(input_file_path, "r")
    except:
        print("[-] Error opening input file: {}".format(input_file_path))
        exit(0)
    # return input & output files
    return input_file, output_file


def copy_as_is(input_file, output_file, verbose):
    if verbose:
        print("[*] copying words as is from input to output...")
    try:
        # go to start of file
        input_file.seek(0)
        # iterate over words in input file
        for line_space in input_file.readlines():
            # remove spaces frim line
            line = line_space.strip()
            output_file.write("{}\n".format(line))
    except:
        print("[-] Error at copy_as_is function")
    return


def combine_words(output_file, verbose):
    if verbose:
        print("[*] generating passwords by combined words...")
    try:
        # dictionary to help save the words
        words = []
        # go to start of file
        output_file.seek(0)
        # iterate over words in input file
        for line_space in output_file.readlines():
            # remove spaces from line
            line = line_space.strip()
            # store in ditionary
            words.append(line)
        # go to start of file
        output_file.seek(0)
        for line_space in output_file.readlines():
            # remove spaces from line
            line = line_space.strip()
            # for each word in dictionary
            for word in words:
                # add the combination to output file
                output_file.write("{}{}\n".format(line, word))
    except:
        print("[-] Error at combine_words function")
    return


def capitalize(output_file, verbose):
    if verbose:
        print("[*] generating passwords by capitalize words...")
    try:
        # go to start of file
        output_file.seek(0)
        # iterate over words in input file
        for line_space in output_file.readlines():
            # remove spaces from line
            line = line_space.capitalize().strip()
            output_file.write("{}\n".format(line))
    except:
        print("[-] Error at capitalize function")
    return


def add_obvious(output_file, verbose):
    if verbose:
        print("[*] generating passwords by adding obvious numbers to words...")
    obvious_numbers = ["0", "1", "12", "123", "1234", "12345", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@",
                       "#", "$", "^", "*"]
    try:
        # go to start of file
        output_file.seek(0)
        # iterate over words in input file
        for line_space in output_file.readlines():
            # remove spaces from line
            line_before = line_space.strip()
            for number in obvious_numbers:
                line = "{}{}".format(line_before, number)
                output_file.write("{}\n".format(line))
    except:
        print("[-] Error at add_obvious function")
    return


def replace_letters(output_file, verbose):
    if verbose:
        print("[*] generating passwords by replacing letters to signs and numbers...")
    signs_dict = {"a": "@", "s": "5", "e": "3", "o": "0", "i": "!"}
    try:
        # go to start of file
        output_file.seek(0)
        # iterate over words in input file
        for line_space in output_file.readlines():
            # remove spaces from line
            line = line_space.strip()
            line_all_switch = line
            # dict of each word to avoid duplicates
            dict_word = [line]
            # for each char in dictionary
            for s in signs_dict:
                # if the word contains the char
                if s in line:
                    # replace each dictionary char individually
                    line_to_add = line.replace(s, signs_dict[s])
                    # create line with all switched
                    line_all_switch = line_all_switch.replace(s, signs_dict[s])
                    # if created a new word
                    if line_to_add not in dict_word:
                        # add word to output file
                        output_file.write("{}\n".format(line_to_add))
                        # update dict_word
                        dict_word.append(line_to_add)
            # if line_all_switch is new
            if line_all_switch not in signs_dict:
                # add word to output file
                output_file.write("{}\n".format(line_all_switch))
    except:
        print("[-] Error at raplece_letters function")
    return


def add_dates(output_file, verbose, dates):
    if verbose:
        print("[*] generating passwords by adding dates to words...")
    # build list from given dates
    dates_list = dates.split(",")
    try:
        for date in dates_list:
            date_arr = date.split(".")
            day = date_arr[0]
            month = date_arr[1]
            year = date_arr[2]
            year2 = year[2:]
    except:
        print("[-] Error in dates argument\n")
        # return failed
        return False
    # go to start of file
    output_file.seek(0)
    # iterate over words in input file
    for line_space in output_file.readlines():
        # remove spaces from line
        line = line_space.strip()
        #  if word ends with a letter
        if line[len(line) - 1].isalpha():
            output_file.write("{}{}{}{}\n".format(line, day, month, year))
            output_file.write("{}{}{}{}\n".format(line, day, month, year2))
            output_file.write("{}{}\n".format(line, year))
            output_file.write("{}{}\n".format(line, year2))
            output_file.write("{}{}{}\n".format(line, day, month))
    # return success
    return True


def filter_max(output_file, max_length, verbose):
    if verbose:
        print("[*] filtering passwords by maximum length...")
    # list for saving all words after filter
    words_list = []
    # go to start of file
    output_file.seek(0)
    # iterate over words in input file
    for line_space in output_file.readlines():
        # remove spaces from line
        line = line_space.strip()
        if len(line) <= max_length:
            words_list.append(line)
    # delete file content
    output_file.truncate(0)
    # go to start of file
    output_file.seek(0)
    # append all filtered words back to file
    for word in words_list:
        output_file.write("{}\n".format(word))


def calculate(input_file, output_file, verbose):
    if verbose:
        print("[*] calculating lines in files...\n")
    # inialize lines count variables
    input_lines = 0
    output_lines = 0
    # go to start of files
    input_file.seek(0)
    output_file.seek(0)
    for line in input_file.readlines():
        input_lines += 1
    for line in output_file.readlines():
        output_lines += 1
    return input_lines, output_lines


def main():
    # Building arguments
    parser = argparse.ArgumentParser(description="Password dictionary amplifyer",
                                     epilog="-------------------------------------------------------------------------------")
    main_group = parser.add_argument_group("Argumnets")
    main_group.add_argument("-I", metavar="<FILE PATH>", help="Input password dictionary file (.txt)", type=str,
                            required=True)
    main_group.add_argument("-O", metavar="<FILE NAME>", help="Output file name (deafult: PassAmp_out.txt)", type=str)
    main_group.add_argument("-V", action="store_true", help="Verbose mode", required=False)
    amplify_options_group = parser.add_argument_group("Amplify options")
    amplify_options_group.add_argument("-m", action="store_true", help="Amplify by combined words")
    amplify_options_group.add_argument("-c", action="store_true", help="Amplify by capitalized words")
    amplify_options_group.add_argument("-o", action="store_true",
                                       help="Amplify by adding obvious numbers and signs to words")
    amplify_options_group.add_argument("-s", action="store_true",
                                       help="Amplify by replacing letters with signs (like: i -> !)")
    amplify_options_group.add_argument("-d", metavar="<DAY.MONTH.YEAR>", type=str,
                                       help="Amplify by adding dates to words (comma-seperated) ")
    amplify_options_group.add_argument("-x", metavar="<INT>", type=int, help="Maximum word length (default: none)")
    args = parser.parse_args()
    # store variables
    input_file_path = args.I
    output_name = args.O
    verbose = args.V
    capital = args.c
    obvious_num = args.o
    signs = args.s
    combined = args.m
    dates = args.d
    max_length = args.x
    # print when start
    print("\n[*] PassAmplifyer starting...\n")
    # try send to relevant functions
    try:
        # get input & output files from function
        input_file, output_file = validate_input_create_files(input_file_path, output_name, verbose)
        # anyway, call copy_as_is function
        copy_as_is(input_file, output_file, verbose)
        # if -c supplied, call capitalize function
        if capital:
            capitalize(output_file, verbose)
        # if -m supplied, call combine_words
        if combined:
            combine_words(output_file, verbose)
        # if -o supplied, call add_obvious_numbers function
        if obvious_num:
            add_obvious(output_file, verbose)
        # if -s supplied, call replace_to_signs function
        if signs:
            replace_letters(output_file, verbose)
        # if -d supplied, call add_dates function
        if dates:
            res = add_dates(output_file, verbose, dates)
            # if add_dates failed - return
            if res is False:
                return
        # if -x supplied, call filter_max function
        if max_length:
            filter_max(output_file, max_length, verbose)

        # get data from calculate function before closing files
        input_lines, output_lines = calculate(input_file, output_file, verbose)
        # print data of files
        print("[+] input file: {} lines  --->  output file: {} lines\n".format(input_lines, output_lines))
    finally:
        if verbose:
            print("[*] closing input & output files...\n")
        # close files
        input_file.close()
        output_file.close()
        print("[*] PassAmplifyer completed.\n")


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv or len(argv) == 1:
        print(banner)
    main()
