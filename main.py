from einar import AES
from einar.helpers import key_len 

KEY = b'key12345'
KEY_CBC = b'key12345678901234567890'  # 24 bytes for 192 bits

text = b'cryptography test'

aes128 = AES(KEY, keyLen=128, mode="ECB")
cipher128 = aes128.encrypt_ecb(text)
deciphered128 = aes128.decrypt_ecb(cipher128)
print(f"128-bit mode - decrypted from {cipher128} to:", deciphered128)


aes192 = AES(KEY, mode="ECB", keyLen=192)
cipher192 = aes192.encrypt_ecb(text)
deciphered192 = aes192.decrypt_ecb(cipher192)
print(f"192-bit mode - decrypted from {cipher192} to:", deciphered192)


aes256 = AES(KEY_CBC, keyLen=256, mode="CBC", iv=b'1234567890123456')
cipher256 = aes256.encrypt_ecb(text)
deciphered256 = aes256.decrypt_ecb(cipher256)
print(f"CBC mode - 256 bits - decrypted from {cipher256} to:", deciphered256)