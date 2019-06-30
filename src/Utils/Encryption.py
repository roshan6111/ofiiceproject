import ast
import json
from base64 import b64decode, b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

backend = default_backend()
key = 'B8DDAA85EF098452123B787412CCEA04740C7256EC8FDBA1'[:32]
iv = '9EB1F717F81C163466E04BB4BF74E7D8'[:16]


def encryptor(data):
    data = str(data)
    padder = padding.PKCS7(128).padder()
    message_encrypt = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor_cipher = cipher.encryptor()
    ct = encryptor_cipher.update(message_encrypt) + encryptor_cipher.finalize()
    ct_out = b64encode(ct)
    return ct_out


def decryptor(data):
    unpadder = padding.PKCS7(128).unpadder()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor_cipher = cipher.decryptor()
    ct = b64decode(data)
    plain = decryptor_cipher.update(ct) + decryptor_cipher.finalize()
    plain = unpadder.update(plain) + unpadder.finalize()
    plain = json.dumps(plain)
    plain = json.loads(plain)
    plain = ast.literal_eval(plain)
    plain = ast.literal_eval(json.dumps(plain))
    return plain
