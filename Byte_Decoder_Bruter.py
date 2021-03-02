import operator
import argparse


def hexdump(src, length=16, sep='.'):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
    lines = []
    for c in range(0, len(src), length):
        chars = src[c: c + length]
        hex_ = ' '.join(['{:02x}'.format(x) for x in chars])
        if len(hex_) > 24:
            hex_ = '{} {}'.format(hex_[:24], hex_[24:])
        printable = ''.join(['{}'.format((x <= 127 and FILTER[x]) or sep) for x in chars])
        lines.append('{0:08x}  {1:{2}s} |{3:{4}s}|'.format(c, hex_, length * 3, printable, length))
    return '\n'.join(lines)


def decoder(hex_content, key, op):
    ops = {"xor": operator.xor, "add": operator.add}
    if op not in ops:
        return None
    else:
        if type(hex_content) is str:
            hex_array = bytearray.fromhex(hex_content)
        else:
            hex_array = hex_content
        byte_array_result = []
        for byte in hex_array:
            byte_array_result.append(ops[op](byte, key) % 0xff)
        return hexdump(byte_array_result)


def print_operator(hex_content, key, operator, output_file):
    output = "\n\n"
    output += "#############################################################################\n"
    output += "############################### {} With {} ###############################".format(operator.upper(),
                                                                                                  "0x%x" % key)
    output += "\n#############################################################################\n\n"
    output += decoder(hex_content, key, operator)
    output += "\n"
    if output_file:
        with open(output_file, "a") as of:
            of.write(output)
    else:
        print(output)


def main():
    # Build Arguments
    parser = argparse.ArgumentParser(description="Single-Byte decoder (XOR, ADD)",
                                     epilog="#########################################################")
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("-HS", metavar="<HEX STRING>", help="Input as hex string")
    input_group.add_argument("-HF", metavar="<FILE NAME>", help="Input from hex file")
    input_group.add_argument("-CS", metavar="<STRING>", help="Input as content string")
    input_group.add_argument("-CF", metavar="<FILE NAME>", help="Input from file content")
    Arguments = parser.add_argument_group("Options")
    Arguments.add_argument("-HK", metavar="<HEX KEY>", help="Use only this hex byte key (e.g. B5)")
    Arguments.add_argument("-OP", help="Use only this operator", choices=["xor", "add"], required=False)
    Arguments.add_argument("-OF", metavar="<FILE NAME>", help="Output to file", required=False)
    args = parser.parse_args()
    # Store Key if supplied ,if no - Brute them all :)
    if args.HK:
        keys = bytearray.fromhex(args.HK)
    else:
        keys = bytearray(range(1, 256))
    # Store input
    if args.HS:
        hex_str_or_array = args.HS
    elif args.HF:
        try:
            with open(args.HF, "rt") as hf:
                hex_str_or_array = hf.read().strip()
        except FileNotFoundError:
            print("[-] ERROR: File {} not found".format(args.HF))
            return
    elif args.CS:
        hex_str_or_array = bytearray(args.CS, 'utf-8')
    elif args.CF:
        try:
            with open(args.CF, "rb") as cf:
                hex_str_or_array = bytearray(cf.read())
        except FileNotFoundError:
            print("[-] ERROR: File {} not found".format(args.CF))
            return
    else:
        print("[-] ERROR: No input supplied")
        return
    # Brute all hex keys (or one if supplied)
    for key in keys:
        # Store operator(s)
        operators = []
        if args.OP:
            operators.append(str(args.OP))
        else:
            operators = ["xor", "add"]
        # execute
        for operator in operators:
            print_operator(hex_str_or_array, key, operator, args.OF)


if __name__ == '__main__':
    main()
