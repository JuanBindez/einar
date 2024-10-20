import argparse

from einar import EinarManager
from einar.exceptions import EinarError

def main():
    parser = argparse.ArgumentParser(description="Einar: Password Manager CLI")
    parser.add_argument('-s', '--set-master-password', type=str, help="Set the master password")
    parser.add_argument('-a', '--add-password', nargs=3, metavar=('service', 'username', 'password'),
                        help="Add a password for a specified service")
    parser.add_argument('-v', '--view-passwords', type=str, help="View all stored passwords")
    parser.add_argument('-d', '--delete-password', nargs=2, metavar=('service', 'master_password'),
                        help="Delete a password entry for a specified service using the master password")

    args = parser.parse_args()

    manager = EinarManager()

    if args.set_master_password:
        try:
            manager.set_master_password(args.set_master_password)
            print("Master password set successfully.")
        except EinarError as e:
            print(e)

    if args.add_password:
        service, username, password = args.add_password
        try:
            manager.add_password(service, username, password)
            print(f"Password for {service} added successfully.")
        except EinarError as e:
            print(e)

    if args.view_passwords:
        master_password = args.view_passwords
        try:
            passwords = manager.view_passwords(master_password)
            for entry in passwords:
                print(f"{entry['service']}:\n\tlogin = {entry['login']}\n\tpassword = {entry['password']}")
        except EinarError as e:
            print(e)

    if args.delete_password:
        service, master_password = args.delete_password
        try:
            manager.delete_password(service, master_password)
            print(f"Password for {service} deleted successfully.")
        except EinarError as e:
            print(e)

if __name__ == "__main__":
    main()
