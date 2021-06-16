import subprocess
import os


def get_services():
    command = "WMIC.exe service get pathname"
    services_list = []
    command_output = subprocess.check_output(command, shell=True, universal_newlines=True)
    for service in command_output.split("\n"):
        # remove title and empty values
        if service != '' and not service.startswith('PathName'):
            services_list.append(service.strip())
    return services_list


def check_unquoted(services):
    unqouted_services = []
    for service in services:
        binary_path = service.split(".exe")[0]
        if not binary_path.startswith('"') and " " in binary_path:
            unqouted_services.append(service)
    return unqouted_services


def print_unquoted_service(unqouted_service):
    print("[!] Unquoted service Found!")
    print(f"\t--> {unqouted_service}")
    print("\tPotential paths to implant bad binary:")
    binary_path_parts = unqouted_service.split(".exe")[0].split(" ")[:-1]
    binary_paths = [binary_path_parts[0]]
    for i in (0, len(binary_path_parts) - 1):
        binary_paths.append(binary_paths[-1] + binary_path_parts[i])
    # append .exe for each path
    binary_paths = [(i + ".exe") for i in binary_paths]
    for binary_path in binary_paths:
        if os.access(os.path.dirname(binary_path), os.W_OK):
            print(f"\t\t{binary_path} <-- Have write access ;-)")
        else:
            print(f"\t\t{binary_path} <-- Don't Have write access :-(")


def main():
    services = get_services()
    unqouted_services = check_unquoted(services)
    if not unqouted_services:
        print("[-] No unqouted services found :-(")
    for unqouted_service in unqouted_services:
        print_unquoted_service(unqouted_service)


main()
