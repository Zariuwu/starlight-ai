#!/usr/bin/env python3
"""
Starlight launcher script for macOS.
This script polls for the Starlight drive and launches the runtime when detected.
"""
import os
import time
import subprocess

VOLUME_PATH = "/Volumes"
USB_NAME = "Starlight"
ENTRY_REL = "runtime/common/starlight_main.py"


def find_usb_root():
    path = os.path.join(VOLUME_PATH, USB_NAME)
    manifest_path = os.path.join(path, "manifest.json")
    return path if os.path.exists(manifest_path) else None

def main():
    print("Starlight macOS launcher watching for USB...")
    while True:
        root = find_usb_root()
        if root:
            print(f"Starlight drive found at {root}")
            # Launch the runtime script
            subprocess.Popen(["python3", os.path.join(root, ENTRY_REL), root])
            break
        time.sleep(5)

if __name__ == "__main__":
    main()
