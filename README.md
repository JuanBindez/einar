# Einar

## Python3 Password Manager Library.

### Usage

Importing EinarManager in Your Script

You can create a Python script to use the EinarManager class. Below is an example of how to import and use it.

```python

from einar import EinarManager

# Create an instance of EinarManager
manager = EinarManager()

# Set the master password
manager.set_master_password('your_master_password')

# Add a password entry
manager.add_password('example_service', 'username', 'password123')

# View stored passwords
passwords = manager.view_passwords('your_master_password')
print(passwords)

# Delete a password entry
manager.delete_password('example_service', 'your_master_password')

```

### Command-Line Interface (CLI) Usage

You can use the following commands in the terminal to interact with Einar:

```bash

# Set Master Password
einar -s <your_master_password>

# Add Password
einar -a <service> <username> <password> <your_master_password>

# View Passwords
einar -v <your_master_password>

# Delete Password
einar -d <service> <your_master_password>

```
