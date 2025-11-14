#!/usr/bin/env python3
"""
Starlight launcher script for Windows.
Poll removable drives for Starlight drive and run the runtime script.
"""
import os
import time
import subprocess
import string

USB_NAME = "Starlight"
ENTRY_REL = "runtime/common/starlight_main.py"

def find_usb_root():
    # Check all drive letters for Starlight drive
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        manifest_path = os.path.join(drive, USB_NAME, "manifest.json")
        if os.path.exists(manifest_path):
            return os.path.join(drive, USB_NAME)
    return None

def main():
    print("Starlight Windows launcher watching for USB...")
    while True:
        root = find_usb_root()
        if root:
            print(f"Starlight drive found at {root}")
            subprocess.Popen(["python", os.path.join(root, ENTRY_REL), root])
            break
        time.sleep(5)

if __name__ == "__main__":
    main()
