import hashlib
import json
import os
import streamlit as st

def generate_hashes():
    """Generates hashes for core files to prevent tampering."""
    core_files = ["Homepage.py", "utils.py", "threshold_squats.py", "threshold_curl.py"]
    hashes = {}
    
    for file in core_files:
        if os.path.exists(file):
            with open(file, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                hashes[file] = file_hash
                
    with open("security_hashes.json", "w") as f:
        json.dump(hashes, f, indent=4)
    print("Hashes generated successfully!")

def verify_integrity():
    """Verifies that core files have not been modified."""
    if not os.path.exists("security_hashes.json"):
        # Initial run: generate hashes
        generate_hashes()
        return True

    with open("security_hashes.json", "r") as f:
        stored_hashes = json.load(f)

    for file, stored_hash in stored_hashes.items():
        if os.path.exists(file):
            with open(file, "rb") as f:
                current_hash = hashlib.sha256(f.read()).hexdigest()
                if current_hash != stored_hash:
                    st.error(f"🚨 SECURITY ALERT: Integrity check failed for {file}. The application has been tampered with. Please run 'python security.py --update' to legitimize your changes.")
                    st.stop()
        else:
            st.error(f"🚨 SECURITY ALERT: Core file {file} is missing.")
            st.stop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        generate_hashes()
