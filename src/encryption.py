import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256, Hash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Hashing password
# Salt and hashed password is 32 bytes long
def hash(password: str, salt: bytes=None):
    # Generating salt if none already
    if salt == None:
        salt = os.urandom(32)
    
    # Hashing password
    digest = Hash(SHA256())
    digest.update(salt)
    digest.update(password.encode("utf-8"))
    return digest.finalize(), salt
# Generating key
def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return kdf.derive(password.encode("utf-8"))

# Encrypting the data
def encrypt_data(data, key: bytes):
    iv = os.urandom(16)
    cipher = Cipher(algorithm=algorithms.AES256(key), mode=modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted = iv + encryptor.update(data) + encryptor.finalize()
    return encrypted

# Decrypting the data
def decrypt_data(encrypted_data: bytes, key: bytes):
    iv = encrypted_data[:16]
    cipher = Cipher(algorithm=algorithms.AES256(key), mode=modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    return decrypted
