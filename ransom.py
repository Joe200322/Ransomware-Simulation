import os
from Crypto.Cipher import AES
import base64

def generateKey():
    key = os.urandom(16)
    return key

def generateIv():
    iv = os.urandom(16)
    return iv

def encrypt(plaintxt,key,iv):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    padded_plaintxt = plaintxt + (16 - len(plaintxt)%16)*' ' 
    ciphertxt = cipher.encrypt(padded_plaintxt.encode())
    return base64.b64encode(iv+ciphertxt).decode()

def decrypt(ciphertxt,key):
    raw_data = base64.b64decode(ciphertxt)
    iv = raw_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(raw_data[16:]).decode().strip()
    return decrypted_text


