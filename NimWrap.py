import argparse
from os import getenv, path, remove
from subprocess import run


def validate_nim():
    print("[i] Validating nim...")
    paths = getenv("path").split(";")
    for p in paths:
        if "\\nim-" in p and not "mingw" in p:
            nim_path = p
    nim_bin = nim_path + "\\nim.exe"
    if not path.isfile(nim_bin):
        print("[-] ERROR: Could not find nim binary")
        exit()
    return nim_path


def wrap_exe(command, out_file, is_strenc, keep_source):

    # import strenc if exists
    if is_strenc:
        import_strenc = "import strenc"
    else:
        import_strenc = ""

    nim_content = ""
    nim_content += "import winim/lean\n" 
    nim_content += f"{import_strenc}\n\n"
    nim_content += f'WinExec(r"' + command + '", 0)\n'

    nim_file = "temp.nim"

    compile_nim = f"nim c -d:release -o:{out_file} {nim_file}"

    print(f"[i] Writing nim source code to {nim_file}...")
    with open(nim_file, "wt") as f:
        f.write(nim_content)

    print(f"[i] Compiling to exe... [{compile_nim}]")
    ret = run(compile_nim, capture_output=True)
    if ret.returncode == 1:
        print("[-] ERROR: Could not compile")
        exit()
    else:
        print("[+] Compiled Successfully")

    if not keep_source:
        print(f"[i] Removing {nim_file}...")
        remove(nim_file)


def wrap_dll(command, out_file, is_strenc, keep_source):

    # import strenc if exists
    if is_strenc:
        import_strenc = "import strenc"
    else:
        import_strenc = ""

    nim_content = ""
    nim_content += "import winim/lean\n" 
    nim_content += f"{import_strenc}\n\n"
    nim_content += "proc NimMain() {.cdecl, importc.}\n\n"
    nim_content += "proc DllMain(hinstDLL: HINSTANCE, fdwReason: DWORD, lpvReserved: LPVOID) : BOOL {.stdcall, exportc, dynlib.} =\n\n"
    nim_content += "    NimMain()\n\n"
    nim_content += "    if fdwReason == DLL_PROCESS_ATTACH:\n"
    nim_content += f'        WinExec(r"' + command + '", 0)\n'
    nim_content += "    return true\n"

    nim_file = "temp.nim"

    compile_nim = f"nim c -d:release --app:lib --nomain -o:{out_file} {nim_file}"

    print(f"[i] Writing nim source code to {nim_file}...")
    with open(nim_file, "wt") as f:
        f.write(nim_content)

    print(f"[i] Compiling to dll... [{compile_nim}]")
    ret = run(compile_nim, capture_output=True)
    if ret.returncode == 1:
        print("[-] ERROR: Could not compile")
        exit()
    else:
        print("[+] Compiled Successfully")
    
    if not keep_source:
        print(f"[i] Removing {nim_file}...")
        remove(nim_file)


def main():

    # Build Arguments
    parser = argparse.ArgumentParser(description="Wrap a windows shell command with compiled binary using nim")
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("-s", metavar="<command>", help="Input as shell command")
    input_group.add_argument("-i", metavar="<file name>", help="Input from file contains shell command")
    Arguments = parser.add_argument_group("Options")
    Arguments.add_argument("-o", metavar="<file name>", help="Output file name")
    Arguments.add_argument("-t", choices=["exe", "dll"], help="PE type", default="exe")
    Arguments.add_argument("-e", action="store_true", help="Encrypt shell command using nim-strenc (need to be installed)")
    Arguments.add_argument("-k", action="store_true", help="Keep nim source file")
    args = parser.parse_args()

    # get command
    if args.i:
        try:
            with open(args.i, "rt") as f:
                command = f.read().strip()
        except FileNotFoundError:
            print("[-] ERROR: File {} not found".format(args.i))
            return
    elif args.s:
        command = args.s
    else:
        print("[-] ERROR: No shell command supplied")
        exit()

    # set output file
    if not args.o:
        out_file = "out." + args.t
    else:
        out_file = args.o
        if args.t == "dll" and not out_file.endswith("dll"):
            out_file += ".dll"
        if out_file.endswith("dll"):
            args.t = "dll"

    print("[i] Starting...")

    # validate nim and check libraries
    nim_path = validate_nim()
    
    if args.t == "exe":
        wrap_exe(command, out_file, args.e, args.k)
    elif args.t == "dll":
        wrap_dll(command, out_file, args.e, args.k)

    print(f"[#] Output file: {path.abspath(out_file)}")

if __name__ == '__main__':
    main()
