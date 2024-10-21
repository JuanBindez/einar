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
import einar.exceptions as exception

class EinarManager:
    """A simple password manager that securely stores and retrieves passwords."""

    def __init__(self, master_password):
        """Initializes the EinarManager with the provided master password."""
        self._create_db()

        # Retrieve or generate the encryption key
        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)

        # Flag to check if the password has been validated
        self.password_validated = False

        # Check if master password already exists
        self.master_password_hash = self._get_master_password_hash()
        if self.master_password_hash is None:
            # First time: save the master password
            self.master_password_hash = self._hash_password(master_password)
            self._save_master_password_hash(self.master_password_hash)
            self.password_validated = True
        else:
            # Verify if the provided password matches the saved one
            if self.check_master_password(master_password):
                self.password_validated = True
            else:
                raise exception.EinarError("Incorrect master password!")
            
    def _get_or_create_key(self):
        """Retrieves the encryption key from the database or generates a new one if not found."""
        self.c.execute("SELECT key FROM encryption_key WHERE id = 1")
        result = self.c.fetchone()
        if result:
            return result[0]
        else:
            new_key = Fernet.generate_key()
            self.c.execute("INSERT INTO encryption_key (id, key) VALUES (1, ?)", (new_key,))
            self.conn.commit()
            return new_key

    def _hash_password(self, password):
        """
        Hashes the given password using SHA-256.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _create_db(self):
        """Creates or connects to the SQLite database for storing passwords, master password, and encryption key."""
        self.conn = sqlite3.connect('passwords.db')  # Persist the data to disk
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS passwords
                          (id INTEGER PRIMARY KEY, service TEXT, username TEXT, password TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS master_password
                          (id INTEGER PRIMARY KEY, password_hash TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS encryption_key
                          (id INTEGER PRIMARY KEY, key TEXT)''')
        self.conn.commit()

    def _get_master_password_hash(self):
        """
        Retrieves the master password hash from the database.

        Returns:
            str or None: The stored master password hash or None if not set.
        """
        self.c.execute("SELECT password_hash FROM master_password WHERE id = 1")
        result = self.c.fetchone()
        return result[0] if result else None

    def _save_master_password_hash(self, password_hash):
        """
        Saves the master password hash to the database.

        Args:
            password_hash (str): The hashed master password to save.
        """
        self.c.execute("INSERT INTO master_password (id, password_hash) VALUES (1, ?)", (password_hash,))
        self.conn.commit()

    def check_master_password(self, master_password):
        """
        Checks if the provided master password matches the stored master password hash.

        Args:
            master_password (str): The master password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self._hash_password(master_password) == self.master_password_hash

    def _require_valid_password(self):
        """
        Internal method to ensure the master password has been validated before proceeding.
        
        Raises:
            EinarError: If the master password is not validated.
        """
        if not self.password_validated:
            raise exception.EinarError("Master password not validated. Access denied.")

    def add_password(self, service, username, password):
        """
        Adds a new password entry for a specified service, requires valid master password.

        Args:
            service (str): The service name (e.g., Gmail).
            username (str): The username associated with the service.
            password (str): The password to store.

        Raises:
            EinarError: If the master password is not validated.
        """
        self._require_valid_password()
        encrypted_password = self.fernet.encrypt(password.encode())
        self.c.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)", 
                       (service, username, encrypted_password))
        self.conn.commit()

    def view_passwords(self):
        """
        Retrieves all stored passwords, requires valid master password.

        Returns:
            list of dict: A list of dictionaries containing the service, username, and decrypted password.

        Raises:
            EinarError: If the master password is not validated.
        """
        self._require_valid_password()
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

    def delete_password(self, service):
        """
        Deletes the password entry for a specified service, requires valid master password.

        Args:
            service (str): The service name for which the password should be deleted.

        Raises:
            EinarError: If the master password is not validated.
        """
        self._require_valid_password()
        self.c.execute("DELETE FROM passwords WHERE service = ?", (service,))
        self.conn.commit()

    def __del__(self):
        """
        Closes the database connection when the EinarManager instance is deleted.
        """
        self.conn.close()
