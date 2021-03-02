import operator
import argparse


def encoder(hex_content, key, op, output_file):
    ops = {"xor": operator.xor, "add": operator.add}
    if type(hex_content) is str:
        hex_array = bytearray.fromhex(hex_content)
    else:
        hex_array = hex_content
    byte_array_result = []
    for byte in hex_array:
        byte_array_result.append(ops[op](byte, key) % 0xff)
    with open(output_file, "wb") as of:
        of.write(bytearray(byte_array_result))


def main():
    # Build Arguments
    parser = argparse.ArgumentParser(description="Hex key Encoder (XOR, ADD)",
                                     epilog="##################################################################")
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("-HS", metavar="<HEX STRING>", help="Input as hex string")
    input_group.add_argument("-HF", metavar="<FILE NAME>", help="Input from hex file")
    input_group.add_argument("-CS", metavar="<STRING>", help="Input as content string")
    input_group.add_argument("-CF", metavar="<FILE NAME>", help="Input from file content")
    Arguments = parser.add_argument_group("arguments")
    Arguments.add_argument("OP", help="Use this operator", choices=["xor", "add"])
    Arguments.add_argument("HK", metavar="<HEX KEY>", help="Encode with this single-byte hex key (e.g. 5b)")
    Arguments.add_argument("OF", metavar="<FILE NAME>", help="Output to file")
    args = parser.parse_args()
    # Store Key
    key = bytearray.fromhex(args.HK)[0]
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

    # execute
    encoder(hex_str_or_array, key, args.OP, args.OF)


if __name__ == '__main__':
    main()
