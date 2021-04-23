from sys import argv
import argparse
import random
import string
import base64
import re

banner = """
   ___                           _          _ _     ___ _      __                     _             
  / _ \_____      _____ _ __ ___| |__   ___| | |   /___\ |__  / _|_   _ ___  ___ __ _| |_ ___  _ __ 
 / /_)/ _ \ \ /\ / / _ \ '__/ __| '_ \ / _ \ | |  //  // '_ \| |_| | | / __|/ __/ _` | __/ _ \| '__|
/ ___/ (_) \ V  V /  __/ |  \__ \ | | |  __/ | | / \_//| |_) |  _| |_| \__ \ (_| (_| | || (_) | |   
\/    \___/ \_/\_/ \___|_|  |___/_| |_|\___|_|_| \___/ |_.__/|_|  \__,_|___/\___\__,_|\__\___/|_|   
                                                                                                    
"""


##### helpful functions #####

def get_random_string():
    length = random.randint(3, 15)
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_random_comment():
    comment = ""
    length = random.randint(3, 15)
    for _ in range(length):
        comment += get_random_string() + " "
    comment = " <#" + comment + "#> "
    return comment


def add_function_parentheses(input_data):
    # where functions declared without () --> some obfuscation techniques fails.
    function_without_parentheses_pattern = re.compile(r"function [\w-]+\s*\{")
    functions_without_parentheses = re.findall(function_without_parentheses_pattern, input_data)
    output_data = input_data
    for function_without_parentheses in functions_without_parentheses:
        # remove last "{"
        temp = function_without_parentheses[:-1]
        # if last character is a newline - remove it too
        if temp[-1] == "\n":
            temp = temp[:-1]
        replaced_pattern = temp + "(){"
        output_data = input_data.replace(function_without_parentheses, replaced_pattern)
    return output_data


##### obfuscation functions #####

def remove_comments(input_data):
    print("[i] Removing comments...")
    output_data = ""
    in_multiple_line_comment = False
    in_one_line_comment = False
    for i in range(0, len(input_data)):
        if input_data[i] == "<" and input_data[i + 1] == "#":
            in_multiple_line_comment = True
        elif input_data[i - 2] == "#" and input_data[i - 1] == ">":
            in_multiple_line_comment = False
        elif input_data[i] == "#" and not in_multiple_line_comment:
            in_one_line_comment = True
        elif input_data[i] == "\n" and in_one_line_comment:
            in_one_line_comment = False
        else:
            pass
        if not in_one_line_comment and not in_multiple_line_comment:
            output_data += input_data[i]
            i += 1
    return output_data


def remove_whitespaces(input_data):
    print("[i] Removing whitespaces...")
    output_data = input_data
    # replaces any whitespaces characters with \n to \n
    pattern = re.compile(r"\s+\n\s+")
    output_data = re.sub(pattern, "\n", output_data)
    # remove tabs and multiple whitespaces
    pattern = re.compile(r"[ \t]+")
    output_data = re.sub(pattern, " ", output_data)
    # replace "[ \n" --> "["
    pattern = re.compile(r"\s*\[\n+")
    output_data = re.sub(pattern, " [", output_data)
    # replace "] \n" --> "]"
    pattern = re.compile(r"\s*\]\n+")
    output_data = re.sub(pattern, " ]", output_data)
    # replace "{ \n" --> "{"
    pattern = re.compile(r"\s*\{\n+")
    output_data = re.sub(pattern, " {", output_data)
    # replace "} \n" --> "}"
    pattern = re.compile(r"\s*\}\n+")
    output_data = re.sub(pattern, " }", output_data)
    # replace "( \n" --> "("
    pattern = re.compile(r"\s*\(\n+")
    output_data = re.sub(pattern, " (", output_data)
    output_data = re.sub(pattern, " )\n", output_data)
    # ") \n" cannot become ")" in some cases so will be ")\n"
    pattern = re.compile(r"\s*\)\n+")
    output_data = re.sub(pattern, " )\n", output_data)

    return output_data


def rename_variables(input_data):
    print("[i] Renaming variables...")
    output_data = input_data
    powershell_variables = ["$args", "$ConfirmPreference", "$ConsoleFileName", "$currentProcess", "$DebugPreference",
                            "$Error", "$ErrorActionPreference", "$ErrorView", "$ExecutionContext", "$false",
                            "$FormatEnumerationLimit", "$HOME", "$Host", "$InformationPreference", "$input",
                            "$MaximumAliasCount", "$MaximumDriveCount", "$MaximumErrorCount", "$MaximumFunctionCount",
                            "$MaximumHistoryCount", "$MaximumVariableCount", "$MyInvocation", "$NestedPromptLevel",
                            "$null", "$OutputEncoding", "$PID", "$PROFILE", "$ProgressPreference", "$PSBoundParameters",
                            "$PSCommandPath", "$PSCulture", "$PSDefaultParameterValues", "$PSEdition", "$PSEmailServer",
                            "$PSHOME", "$PSScriptRoot", "$PSSessionApplicationName", "$PSSessionConfigurationName",
                            "$PSSessionOption", "$PSUICulture", "$PSVersionTable", "$PWD", "$ShellId", "$StackTrace",
                            "$true", "$VerbosePreference", "$WarningPreference", "$WhatIfPreference"]
    variable_pattern = re.compile(r"\$\w+")
    all_variables = re.findall(variable_pattern, input_data)
    variables = list(set(all_variables) - set(powershell_variables))
    for var in variables:
        new_var = "$" + get_random_string()
        output_data = output_data.replace(var, new_var)
    return output_data


def rename_functions(input_data):
    print("[i] Renaming functions...")
    function_names = []
    # get function names
    for _ in input_data.split("function ")[1:]:
        function_names.append(_.split("(")[0].strip())
    output_data = input_data
    for function_name in function_names:
        new_function_name = get_random_string()
        # output_data = output_data.replace(function_name, new_function_name)
        function_name_pattern = re.compile(r"\b{}\b".format(function_name))
        output_data = re.sub(function_name_pattern, new_function_name, output_data)
    return output_data


def mix_letters(input_data):
    print("[i] Mixing upper and lower letters...")
    output_data = ""
    for i in range(0, len(input_data)):
        if input_data[i] in string.ascii_letters and input_data[i - 1] != "`":
            bool_upper = random.randint(0, 1)
            if bool_upper == 1:
                output_data += input_data[i].upper()
            else:
                output_data += input_data[i].lower()
        else:
            output_data += input_data[i]
    return output_data


def add_comments(input_data):
    print("[i] Adding garbage comments...")
    output_data = ""
    for char in input_data:
        if char == "\n":
            output_data += get_random_comment() + "\n" + get_random_comment()
        else:
            output_data += char
    return output_data


def base64_reverse_and_iex(input_data):
    print("[i] Encoding to Base64, reversing, and invoking expression...")
    base64_input_data = base64.b64encode(input_data.encode(encoding='UTF-16LE')).decode()
    reverse_base64_input_data = base64_input_data[::-1]
    output_data = "${0}='{1}';& ([char]105+[char]69+[char]120)([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(${0}[-1..-${0}.Length] -join '')))".format(
        get_random_string(), reverse_base64_input_data)
    return output_data


def make_cmd_oneliner_encoded_command(input_data):
    print("[i] Making CMD oneliner...")
    base64_powershell = base64.b64encode(input_data.encode(encoding='UTF-16LE')).decode()
    cmd_oneliner = "pOwErShElL -eX bYpAsS -nOp -w hIdDeN -eN {}".format(base64_powershell)
    return cmd_oneliner


##### main #####

def main():
    # Building arguments
    parser = argparse.ArgumentParser(description="Obfuscator for Powershell scripts",
                                     epilog="------------------------------------------------------------------------------")
    io_group = parser.add_argument_group("input & output")
    io_group.add_argument("-I", metavar="<FILE PATH>", help="Input ps1 file", type=str, required=True)
    io_group.add_argument("-O", metavar="<FILE PATH>", help="Output file (optional)", type=str, required=False)
    obfuscation_group = parser.add_argument_group("obfuscation techniques")
    obfuscation_group.add_argument("-rc", help="Remove comments", action="store_true")
    obfuscation_group.add_argument("-rw", help="Remove whitespaces", action="store_true")
    obfuscation_group.add_argument("-rv", help="Rename variables", action="store_true")
    obfuscation_group.add_argument("-rf", help="Rename functions", action="store_true")
    obfuscation_group.add_argument("-ml", help="Mix letters (upper & lower)", action="store_true")
    obfuscation_group.add_argument("-ac", help="Add garbage comments", action="store_true")
    obfuscation_group.add_argument("-er", help="Encode (base64), reverse and invoke-expression", action="store_true")
    obfuscation_group.add_argument("-A", help="Invoke all obfuscation methods", action="store_true")
    more_options_group = parser.add_argument_group("more options")
    more_options_group.add_argument("-co", help="Make CMD oneliner to invoke powershell encoded command in hidden window",
                                    action="store_true")
    args = parser.parse_args()

    # read input file
    try:
        with open(args.I, "rt", encoding='utf-8-sig') as input_file:
            data = input_file.read()
    except UnicodeDecodeError:
        print("\n[-] Cannot read binary files.\n")
        exit(1)

    # add parentheses to functions declarations where they do not have, some obfuscation functions need this
    data = add_function_parentheses(data)

    # send to obfuscation functions
    if args.A:
        args.rc = args.rw = args.rv = args.rf = args.ml = args.ac = args.er = True
    if args.rc:
        data = remove_comments(data)
    if args.rw:
        data = remove_whitespaces(data)
    if args.rv:
        data = rename_variables(data)
    if args.rf:
        data = rename_functions(data)
    if args.ml:
        data = mix_letters(data)
    if args.ac:
        data = add_comments(data)
    if args.er:
        data = base64_reverse_and_iex(data)
    if args.co:
        data = make_cmd_oneliner_encoded_command(data)

    # output
    if args.O:
        with open(args.O, "wt") as output_file:
            output_file.write(data)
            print("[+] Output written to {}".format(args.O))
    else:
        print("\n[+] Output: \n")
        print(data)
        print("")


if __name__ == "__main__":
    if "-h" in argv or "--help" in argv or len(argv) == 1:
        print(banner)
    main()
