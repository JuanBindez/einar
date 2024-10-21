# Einar

## Python3 Password Manager Library.

![PyPI - Downloads](https://img.shields.io/pypi/dm/einar)
![PyPI - License](https://img.shields.io/pypi/l/einar)
![GitHub Tag](https://img.shields.io/github/v/tag/JuanBindez/einar?include_prereleases)
<a href="https://pypi.org/project/pytubefix/"><img src="https://img.shields.io/pypi/v/einar" /></a>

### Usage

Importing EinarManager in Your Script

You can create a Python script to use the EinarManager class. Below is an example of how to import and use it.

```python

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


```

### Command-Line Interface (CLI) Usage

You can use the following commands in the terminal to interact with Einar:

```bash

# Set Master Password
einar -s <your_master_password>

# Add Password
einar -a <service> <username> <password>

# View Passwords
einar -v

# Delete Password
einar -d <service>

```
