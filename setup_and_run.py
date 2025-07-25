#!/usr/bin/env python3
"""
Setup and Run Script for Business Form Agent
This script will install dependencies and run the agent
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return False

def check_chrome():
    """Check if Chrome is installed"""
    print("🔍 Checking for Google Chrome...")
    
    # Common Chrome paths
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
        "/usr/bin/google-chrome",  # Linux
        "/usr/bin/chromium-browser",  # Linux Chromium
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",  # Windows
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",  # Windows 32-bit
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✅ Chrome found!")
            return True
    
    # Try to find Chrome in PATH
    try:
        subprocess.run(["google-chrome", "--version"], capture_output=True, check=True)
        print("✅ Chrome found in PATH!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    try:
        subprocess.run(["chrome", "--version"], capture_output=True, check=True)
        print("✅ Chrome found in PATH!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    print("❌ Google Chrome not found!")
    print("Please install Google Chrome from: https://www.google.com/chrome/")
    return False

def run_agent():
    """Run the business form agent"""
    print("🚀 Starting Business Form Agent...")
    
    try:
        subprocess.check_call([sys.executable, "business_form_agent.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Agent failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user")
        return True

def main():
    print("🎯 Business Form Agent Setup")
    print("=" * 40)
    
    # Step 1: Check Chrome
    if not check_chrome():
        print("\n⚠️  Please install Google Chrome and try again.")
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n⚠️  Dependency installation failed.")
        return False
    
    # Step 3: Run agent
    print("\n🎯 Running agent with Il Pastaio Beverly Hills...")
    success = run_agent()
    
    if success:
        print("\n✅ Setup and test completed!")
    else:
        print("\n❌ Setup or test failed!")
    
    return success

if __name__ == "__main__":
    main()