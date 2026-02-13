"""
config.py
Central configuration file for the ransomware simulation project.
All paths, names, and simulation parameters are defined here to keep the code clean
and easy to modify without touching the logic files.
"""

import os

# === IMPORTANT SAFETY === 
# These values MUST point to a isolated test folder inside a VM/snapshot!
# Never use real user folders (Documents, Desktop, Downloads, etc.)
# TARGET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "testfolder"))
TARGET_DIR = 'E:\\Script\\testfolder\\'

# You can also hard-code an absolute path for clarity (recommended in VM):
# TARGET_DIR = "C:/VMs/Lab/victim_test_folder"           # Windows example
# TARGET_DIR = "/home/lab/victim_test"                   # Linux example

# File marking & extensions
ENCRYPTED_EXTENSION = ".locked"
RANSOM_NOTE_FILENAME = "READ_THIS_NOW.txt"

# Crypto settings
KEY_LENGTH_BYTES = 32                       # For AES-256

# Simulation behavior flags
DRY_RUN_ENCRYPTION = False                  # If True → only prints what WOULD be encrypted
CREATE_USER = True                          # Toggle user creation (requires admin/root on some OS)
SHOW_KEY_IN_CONSOLE = True                  # For forensics demo – normally False in real attacks

# Ransom note content
RANSOM_NOTE_CONTENT = """\
=== THIS IS A CONTROLLED EDUCATIONAL SIMULATION ===

This folder has been encrypted as part of a cybersecurity training exercise.
No real harm has been done and no payment is required or possible.

What happened:
- Files were encrypted using AES (via Fernet)
- A dummy user account was created
- This note was dropped

How to recover (for demonstration):
1. Find the encryption key (in this simulation: visible in console / memory forensics)
2. Run the recover.py script with the key
3. Use cleanup.py to remove the dummy user

Instructor/Student note: This is NOT real ransomware.
Purpose: Learn encryption, forensics, recovery, and defense.

Simulation project by:
"""

# Derived / computed paths (don't edit these directly)
RANSOM_NOTE_PATH = os.path.join(TARGET_DIR, RANSOM_NOTE_FILENAME)


def validate_config():
    """Basic sanity checks – call this at startup"""
    if not os.path.isabs(TARGET_DIR):
        raise ValueError("TARGET_DIR must be an absolute path!")
    
    if "Documents" in TARGET_DIR or "Desktop" in TARGET_DIR or "Downloads" in TARGET_DIR:
        raise ValueError(
            "DANGER: TARGET_DIR appears to point to a real user folder!\n"
            "Change it to a dedicated test folder inside a virtual machine."
        )
    
    if not os.path.isdir(TARGET_DIR):
        print(f"Note: TARGET_DIR does not exist yet → will be created when needed.")
    
    print(f"Simulation target folder: {TARGET_DIR}")
    print(f"Dry-run mode: {DRY_RUN_ENCRYPTION}")
