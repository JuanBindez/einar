from einar import AES

# A chave deve ter exatamente 16 bytes (128 bits)
chave = b''  # 16 caracteres

# Inicialize o objeto AES
cipher = AES(chave)

mensagem = b'Mensagem secreta para criptografar'

# Criptografar
texto_cifrado = cipher.encrypt_ecb(mensagem)
print(f"Texto cifrado (bytes): {texto_cifrado}")

# Descriptografar
texto_original = cipher.decrypt_ecb(texto_cifrado)
print(f"Texto original: {texto_original.decode('utf-8')}")