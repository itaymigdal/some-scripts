from os import path
from sys import argv
from psutil import pid_exists
from ctypes import *


def main():

    # Validation
    if len(argv) != 3 or not path.isfile(argv[1]) or not pid_exists(int(argv[2])):
        print(f"\nUsage: py {argv[0]} <dll path> <pid>\n")
        exit(1)

    # Arguments
    dll_path = argv[1].replace("\\", "\\\\").encode()
    pid = argv[2]

    # Memory constants
    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = (0x00F0000 | 0x00100000 | 0xFFF)
    VIRTUAL_MEM = (0x1000 | 0x2000)

    # Get handle to the injected process
    h_process = windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))
    if not h_process:
        print(f"[-] Error: Could not open process {pid}")
        exit(1)

    # Allocate space for DLL path
    allocated_address = windll.kernel32.VirtualAllocEx(h_process, 0, len(dll_path), VIRTUAL_MEM, PAGE_READWRITE)
    if not allocated_address:
        print(f"[-] Error: Could not allocate memory in {pid}")
        exit(1)

    # Write DLL path to allocated space
    result = windll.kernel32.WriteProcessMemory(h_process, allocated_address, dll_path, len(dll_path), byref(c_int(0)))
    if not result or result == 0:
        print(f"[-] Error: Could not write memory to {pid}")
        exit(1)

    # Resolve LoadLibraryA address (for injected process)
    h_kernel32 = windll.kernel32.GetModuleHandleA("kernel32.dll".encode())
    h_loadlibrary = windll.kernel32.GetProcAddress(h_kernel32, "LoadLibraryA".encode())

    # Create remote thread by loading the dll using load LoadLibraryA
    result = windll.kernel32.CreateRemoteThread(h_process, None, 0, h_loadlibrary, allocated_address, 0, c_ulong(0))
    if not result:
        print(f"[-] Error: Could not start remote thread in {pid}")
        exit(1)

    # Print Success
    dll_path = path.abspath(dll_path.decode().replace("\\\\", "\\"))
    print(f"[+] {dll_path} Injected to {pid} :)")


main()
