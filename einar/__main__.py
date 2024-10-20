# this is part of the einar project.
#
# Copyright ©  2024 Juan Bindez  <juanbindez780@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sqlite3
import hashlib
from cryptography.fernet import Fernet
from einar.exceptions import EinarError

class EinarManager:
    """A simple password manager that securely stores and retrieves passwords."""

    def __init__(self):
        """Initializes the EinarManager without a master password."""
        self.master_password_hash = None
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self._create_db()

    def set_master_password(self, master_password):
        """Sets the master password for the EinarManager.

        Args:
            master_password (str): The master password to be stored securely.

        Raises:
            EinarError: If the master password is already set.
        """
        if self.master_password_hash is not None:
            raise EinarError("Master password is already set. Please use a different method to change it.")
        
        self.master_password_hash = self._hash_password(master_password)

    def _hash_password(self, password):
        """Hashes the given password using SHA-256.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _create_db(self):
        """Creates an in-memory SQLite database for storing passwords."""
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE passwords
                          (id INTEGER PRIMARY KEY, service TEXT, username TEXT, password TEXT)''')

    def add_password(self, service, username, password):
        """Adds a new password entry for a specified service.

        Args:
            service (str): The name of the service for which the password is being stored.
            username (str): The username associated with the service.
            password (str): The password to be stored for the service.

        Raises:
            EinarError: If the master password has not been set.
        """
        if self.master_password_hash is None:
            raise EinarError("Master password must be set before adding passwords.")
        
        encrypted_password = self.fernet.encrypt(password.encode())
        self.c.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)", 
                       (service, username, encrypted_password))
        self.conn.commit()

    def check_master_password(self, master_password):
        """Checks if the provided master password matches the stored master password hash.

        Args:
            master_password (str): The master password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.

        Raises:
            EinarError: If the master password has not been set.
        """
        if self.master_password_hash is None:
            raise EinarError("Master password has not been set.")
        return self._hash_password(master_password) == self.master_password_hash

    def view_passwords(self, master_password):
        """Retrieves all stored passwords after verifying the master password.

        Args:
            master_password (str): The master password to access stored passwords.

        Returns:
            list: A list of dictionaries containing service, login, and decrypted password.

        Raises:
            EinarError: If the provided master password is incorrect.
        """
        if not self.check_master_password(master_password):
            raise EinarError("Incorrect master password!")

        self.c.execute("SELECT service, username, password FROM passwords")
        
        passwords = []
        for row in self.c.fetchall():
            service, username, encrypted_password = row
            decrypted_password = self.fernet.decrypt(encrypted_password).decode()
            passwords.append({
                "service": service,
                "login": username,
                "password": decrypted_password
            })
        
        return passwords

    def delete_password(self, service, master_password):
        """Deletes the password entry for a specified service after verifying the master password.

        Args:
            service (str): The name of the service whose password entry will be deleted.
            master_password (str): The master password to verify.

        Raises:
            EinarError: If the provided master password is incorrect.
        """
        if not self.check_master_password(master_password):
            raise EinarError("Incorrect master password!")

        self.c.execute("DELETE FROM passwords WHERE service = ?", (service,))
        self.conn.commit()

    def __del__(self):
        """Closes the database connection when the EinarManager instance is deleted."""
        self.conn.close()
