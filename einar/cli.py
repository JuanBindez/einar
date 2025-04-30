#!/usr/bin/env python3
import sys
import getpass
import argparse
from einar import AES

def encrypt_message(key, plaintext):
    """Encrypts a message using AES-128 ECB."""
    cipher = AES(key)
    padded_msg = cipher._pad(plaintext.encode('utf-8'))
    ciphertext = cipher.encrypt_ecb(padded_msg)
    return ciphertext.hex()

def decrypt_message(key, ciphertext_hex):
    """Decrypts a message using AES-128 ECB."""
    cipher = AES(key)
    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted = cipher.decrypt_ecb(ciphertext)
    return decrypted.decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description="AES-128 Encryption/Decryption CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", help="Text to encrypt", type=str)
    group.add_argument("-d", "--decrypt", help="Hex ciphertext to decrypt", type=str)
    args = parser.parse_args()

    key = getpass.getpass("Enter 16-byte key: ").encode('utf-8')
    if len(key) != 16:
        print("Error: Key must be 16 bytes (128 bits)!")
        sys.exit(1)

    if args.encrypt:
        ciphertext = encrypt_message(key, args.encrypt)
        print(f"\nCiphertext (hex): {ciphertext}")
    elif args.decrypt:
        try:
            plaintext = decrypt_message(key, args.decrypt)
            print(f"\nDecrypted message: {plaintext}")
        except ValueError:
            print("Error: Invalid hex ciphertext!")
            sys.exit(1)

if __name__ == "__main__":
    main()