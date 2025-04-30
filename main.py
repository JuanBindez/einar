from einar import AES


key = b'' # The key must be exactly 16 bytes (128 bits)

cipher = AES(key)

message = b'Secret message to encrypt'

# Encrypt
ciphertext = cipher.encrypt_ecb(message)
print(f"Ciphertext (bytes): {ciphertext}")

# Decrypt
original_text = cipher.decrypt_ecb(ciphertext)
print(f"Original text: {original_text.decode('utf-8')}")