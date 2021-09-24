from math import log
from sys import argv
from os import path
try:
	import pefile
	use_pe_parsing = True
except ModuleNotFoundError:
	print("[*] Module 'pefile' isn't installed. calculating simple entropy.")
	use_pe_parsing = False


def print_help():
	print("\n[-] Usage: {} <file>\n".format(argv[0]))
	exit(1)


def calc_shannon_entropy(byte_array):

	byte_array_length = len(byte_array)
	if byte_array_length == 0:
		return 0
	byte_counts = []  # list of counters for each byte [0-255] in byte array
	entropy = 0.0     

	# for each byte in [0-255] calculate apperances count
	for b in range(256):
		byte_counter = 0
		for byte in byte_array:
			if byte == b:
				byte_counter += 1
		byte_counts.append(float(byte_counter) / byte_array_length)

	# calculate shannon entropy
	for byte_count in byte_counts:
		if byte_count > 0:
			entropy -= byte_count * log(byte_count, 2)
	
	return entropy


def pe_parsing(pe_file):

	# getting total pe length for proportion calculation
	total_pe_length = 0
	for section in pe_file.sections:
		total_pe_length += len(section.get_data())

	# calculate entropy for each section
	print("===================================")
	print("  SECTION  |  ENTROPY  | PROPORTION")
	print("===================================")

	for section in pe_file.sections:
		byte_array = list(section.get_data())
		entropy = calc_shannon_entropy(byte_array)
		propotrion_percent = len(byte_array) * 100 / total_pe_length
		print("[+]", section.Name.decode().ljust(10), "{:.3f}".format(entropy).ljust(10), "{:.3f}%".format(propotrion_percent))
	print("===================================")


def basic_parsing(file):
	with open(file, 'rb') as f:
		byte_array = list(f.read())
		entropy = calc_shannon_entropy(byte_array)
		print("=====================")
		print("[+] Entropy:   {:.3f}".format(entropy))
		print("=====================")


def main():

	global use_pe_parsing

	if len(argv) != 2 or not (path.isfile(argv[1])):
		print_help()

	if use_pe_parsing:
		try:
			pe_file =  pefile.PE(argv[1])
			print("[*] File is portable executable. calculating entropy for each section.")

		except pefile.PEFormatError:
			print("[*] File isn't portable executable. calculating simple entropy.")
			use_pe_parsing = False

	if use_pe_parsing:
		pe_parsing(pe_file)
	else:
		basic_parsing(argv[1])


main()
