import argparse
import getpass

from einar.__main__ import EinarManager
from einar.exceptions import EinarError
from einar.version import __version__

def main():
    parser = argparse.ArgumentParser(description="Einar Password Manager")
    
    parser.add_argument("-s", "--set-password", action="store_true", help="Set the master password (first use)")
    parser.add_argument("-a", "--add", nargs=3, metavar=('SERVICE', 'USERNAME', 'PASSWORD'), help="Add a new password")
    parser.add_argument("-v", "--view", action="store_true", help="View all stored passwords")
    parser.add_argument("-d", "--delete", metavar='SERVICE', help="Delete a password for a specific service")
    parser.add_argument("-V", "--version", action="store_true", help="Show the version of Einar")

    args = parser.parse_args()

    try:
        if args.set_password:
            master_password = getpass.getpass(prompt="Create the master password: ")
            confirm_password = getpass.getpass(prompt="Confirm the master password: ")
            if master_password != confirm_password:
                print("Passwords do not match. Please try again.")
                return

            manager = EinarManager(master_password)
            print("Master password successfully set!")

        else:
            master_password = getpass.getpass(prompt="Enter the master password: ")

            manager = EinarManager(master_password)
            print("Access granted!")

            if args.add:
                service, username, password = args.add
                manager.add_password(service, username, password)
                print(f"Password for service '{service}' has been successfully added!")

            elif args.view:
                passwords = manager.view_passwords()
                if passwords:
                    print("Stored passwords:")
                    for entry in passwords:
                        print(f"Service: {entry['service']}, Username: {entry['login']}, Password: {entry['password']}")
                else:
                    print("No passwords stored.")

            elif args.delete:
                service = args.delete
                manager.delete_password(service)
                print(f"Password for service '{service}' has been successfully deleted!")

            elif args.version:
                print(f"Einar version: {__version__}")

            else:
                print("No valid command was provided. Use --help to see the available options.")
    
    except EinarError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()