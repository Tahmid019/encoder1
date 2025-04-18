import os
import subprocess

def install_requirements():
    print("🔍 Checking and installing dependencies from requirements.txt...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    print("✅ All dependencies installed.")

if __name__ == "__main__":
    install_requirements()
