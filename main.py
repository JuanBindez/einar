from einar import EinarManager
from einar.exceptions import EinarError

def main():
    master_password = input("Enter the master password: ")

    try:
        manager = EinarManager(master_password)
        print("Access granted!")

        service = input("Enter the service name: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        
        manager.add_password(service, username, password)
        print("Password added successfully!")

        passwords = manager.view_passwords()
        print(passwords)

    except EinarError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
