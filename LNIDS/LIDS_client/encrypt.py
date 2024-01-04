#!/usr/bin/env python3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding




class Encrypt:


    class Pad:
    
        def pad_data(plaintext):
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext)
            padded_data += padder.finalize()
            return padded_data



    def encrypt_aes_128(key, plaintext):
        plaintext = bytes(plaintext, 'utf-8')
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()
        padded_plaintext = Pad.pad_data(plaintext)
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return ciphertext
