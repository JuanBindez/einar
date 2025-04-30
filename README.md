# Einar

![PyPI - Downloads](https://img.shields.io/pypi/dm/einar)
![PyPI - License](https://img.shields.io/pypi/l/einar)
![GitHub Tag](https://img.shields.io/github/v/tag/JuanBindez/einar?include_prereleases)
<a href="https://pypi.org/project/pytubefix/"><img src="https://img.shields.io/pypi/v/einar" /></a>

## Python3 library that implements AES-128-ECB encryption.


### Install
    pip install einar

### Quickstart

```python
from einar import AES


key = b'' # The key must be exactly 16 bytes (128 bits)

cipher = AES(key)

message = b'Secret message to encrypt'

```

### Encrypt

```python
ciphertext = cipher.encrypt_ecb(message)
print(f"Ciphertext (bytes): {ciphertext}")

```

### Decrypt

```python
original_text = cipher.decrypt_ecb(ciphertext)
print(f"Original text: {original_text.decode('utf-8')}")

```