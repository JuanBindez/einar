#!/usr/bin/env python3
import sys
import os
import getpass
import argparse
import binascii
from einar import AES

def encrypt_message(key, plaintext, key_len, mode, iv=None):
    """Encrypts a message using the AES class."""
    try:
        cipher = AES(key, keyLen=key_len, mode=mode, iv=iv)
        ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
        return ciphertext.hex()
    except ValueError as e:
        print(f"Error initializing cipher: {e}", file=sys.stderr)
        sys.exit(1)

def decrypt_message(key, ciphertext_hex, key_len, mode, iv=None):
    """Decrypts a message using the AES class."""
    try:
        cipher = AES(key, keyLen=key_len, mode=mode, iv=iv)
        ciphertext = bytes.fromhex(ciphertext_hex)
        decrypted = cipher.decrypt(ciphertext)
        return decrypted.decode('utf-8')
    except (ValueError, binascii.Error) as e:
        print(f"Error during decryption: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

# --- Main CLI Function ---

def main():
    parser = argparse.ArgumentParser(description="AES Encryption/Decryption CLI")
    
    # Arguments for operation (encrypt or decrypt)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", help="Text to encrypt", type=str)
    group.add_argument("-d", "--decrypt", help="Hexadecimal ciphertext to decrypt", type=str)
    
    # Arguments for AES configuration
    parser.add_argument("-kl", "--keylen", default=128, type=int, choices=[128, 192, 256],
                        help="Key length in bits (128, 192, or 256). Default: 128")
    parser.add_argument("-m", "--mode", default="ECB", type=str, choices=["ECB", "CBC"],
                        help="AES operation mode (ECB or CBC). Default: ECB")
    
    args = parser.parse_args()

    # Set key length in bytes
    key_len_bytes = args.keylen // 8
    
    # Prompt user for the key
    try:
        key = getpass.getpass(f"Enter the key (any size, will be adjusted to {key_len_bytes} bytes): ").encode('utf-8')
    except Exception as e:
        print(f"Error reading key: {e}", file=sys.stderr)
        sys.exit(1)
    
    # CBC mode logic (IV)
    iv = None
    if args.mode == "CBC" and args.encrypt:
        iv = os.urandom(16)
        print(f"Generated IV (hex): {iv.hex()}")

    # Perform the operation according to the provided argument
    if args.encrypt:
        ciphertext = encrypt_message(key, args.encrypt, args.keylen, args.mode, iv)
        if args.mode == "CBC":
            print(f"Ciphertext (hex): {iv.hex()}:{ciphertext}")
        else:
            print(f"Ciphertext (hex): {ciphertext}")
    elif args.decrypt:
        if args.mode == "CBC":
            try:
                iv_hex, ciphertext_hex = args.decrypt.split(':', 1)
                iv = bytes.fromhex(iv_hex)
                if len(iv) != 16:
                    print("Error: The provided IV must be 16 bytes!", file=sys.stderr)
                    sys.exit(1)
            except (ValueError, binascii.Error):
                print("Error: For CBC mode, the ciphertext must be in the format 'IV_in_hex:ciphertext_in_hex'.", file=sys.stderr)
                sys.exit(1)
            plaintext = decrypt_message(key, ciphertext_hex, args.keylen, args.mode, iv)
            print(f"Decrypted message: {plaintext}")
        else:
            plaintext = decrypt_message(key, args.decrypt, args.keylen, args.mode)
            print(f"Decrypted message: {plaintext}")

if __name__ == "__main__":
    main()