import argparse
import pefile
import os


def get_paths(root_dir, recursive=True, only_dll_ext=True):
    paths = []

    if recursive:
        for root, dirs, files in os.walk(root_dir):
            [paths.append(os.path.join(root, f)) for f in files]
    else:
        [paths.append(os.path.join(root_dir, f)) for f in os.listdir(root_dir) if
         os.path.isfile(os.path.join(root_dir, f))]

    if only_dll_ext:
        return [path for path in paths if os.path.splitext(path)[1].lower() == ".dll"]
    else:
        return paths


def parse_dlls(file_paths, output_file):
    for f in file_paths:
        try:
            dll = pefile.PE(f)
            for export in dll.DIRECTORY_ENTRY_EXPORT.symbols:
                out_line = f + " -> " + export.name.decode()
                print(out_line)
                if output_file:
                    with open(output_file, "a+") as file_h:
                        file_h.write(out_line + "\n")

        except (pefile.PEFormatError, AttributeError):
            pass


def main():
    parser = argparse.ArgumentParser(description="Dump DLLs exports")
    parser.add_argument("-d", "--directory", metavar="<dirname>", help="directory to start from", required=True)
    parser.add_argument("-o", "--output", metavar="<filename>", help="output file name", default=None)
    parser.add_argument("-r", "--recursive", action="store_true", help="hunt recursively", default=False)
    parser.add_argument("-e", "--only-dll-ext", action="store_true", help="don't try to parse other extensions",
                        default=False)
    args = parser.parse_args()

    file_paths = get_paths(args.directory, recursive=args.recursive, only_dll_ext=args.only_dll_ext)
    parse_dlls(file_paths, args.output)


try:
    main()
except KeyboardInterrupt:
    pass
