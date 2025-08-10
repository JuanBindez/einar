# Einar

![PyPI - Downloads](https://img.shields.io/pypi/dm/einar)
![PyPI - License](https://img.shields.io/pypi/l/einar)
![GitHub Tag](https://img.shields.io/github/v/tag/JuanBindez/einar?include_prereleases)
<a href="https://pypi.org/project/einar/"><img src="https://img.shields.io/pypi/v/einar" /></a>

## Python3 library that implements AES-128, AES-192, AES-256 encryption in ECB and CBC modes.

### Install
```bash
pip install einar
```

### Quickstart

```python
from einar import AES

key = b''  # The key can be any size; it will be padded or truncated to the required length.

# AES-256 CBC example
iv = b'1234567890abcdef'  # Required for CBC mode, must be 16 bytes
cipher = AES(key, keyLen=256, mode="CBC", iv=iv)

message = b'Secret message to encrypt'
```

### Encrypt

```python
ciphertext = cipher.encrypt(message)
print(f"Ciphertext (hex): {ciphertext.hex()}")
```

### Decrypt

```python
original_text = cipher.decrypt(ciphertext)
print(f"Original text: {original_text.decode('utf-8')}")
```

### Modes

#### ECB (Electronic Codebook)

```python
cipher = AES(key, keyLen=128, mode="ECB")
ciphertext = cipher.encrypt(message)
original_text = cipher.decrypt(ciphertext)
```

#### CBC (Cipher Block Chaining)

```python
iv = b'1234567890abcdef'  # 16 bytes
cipher = AES(key, keyLen=256, mode="CBC", iv=iv)
ciphertext = cipher.encrypt(message)
original_text = cipher.decrypt(ciphertext)
```

### CLI

Einar includes a command-line interface for encryption and decryption:

```bash
einar -e "Secret message" -kl 256 -m CBC
```

### License

Distributed under [GPL v2 or later](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

### Author

Juan