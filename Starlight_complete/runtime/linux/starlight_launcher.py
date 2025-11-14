#!/usr/bin/env python3
"""
Starlight launcher script for Linux.
Poll mount points for Starlight drive and run the runtime script.
"""
import os
import time
import subprocess

USB_NAME = "Starlight"
ENTRY_REL = "runtime/common/starlight_main.py"

# potential mount points to search
MOUNT_BASES = ["/media", "/run/media"]

def find_usb_root():
    for base in MOUNT_BASES:
        if os.path.exists(base):
            for user in os.listdir(base):
                user_path = os.path.join(base, user, USB_NAME)
                manifest_path = os.path.join(user_path, "manifest.json")
                if os.path.exists(manifest_path):
                    return user_path
    return None

def main():
    print("Starlight Linux launcher watching for USB...")
    while True:
        root = find_usb_root()
        if root:
            print(f"Starlight drive found at {root}")
            subprocess.Popen(["python3", os.path.join(root, ENTRY_REL), root])
            break
        time.sleep(5)

if __name__ == "__main__":
    main()
