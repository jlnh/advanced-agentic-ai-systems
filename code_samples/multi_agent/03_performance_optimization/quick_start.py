#!/usr/bin/env python3
"""
Quick start script for the Multi-Agent Performance Optimization System.
This script automatically handles setup and runs the demo.
"""

import sys
import subprocess
import os

def check_and_install_dependencies():
    """Check if python-dotenv is installed, install if not"""
    try:
        import dotenv
        print("✅ Dependencies already installed")
        return True
    except ImportError:
        print("📦 Installing required dependency: python-dotenv")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("💡 Please run: pip install python-dotenv")
            return False

def main():
    """Main quick start function"""
    print("🚀 Multi-Agent Performance Optimization - Quick Start")
    print("=" * 55)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return

    print(f"✅ Python {sys.version.split()[0]} detected")

    # Install dependencies if needed
    if not check_and_install_dependencies():
        return

    # Run the demo
    print("\n🎯 Running the simple demo...")
    print("-" * 30)

    try:
        import simple_demo
        print("\n✅ Demo completed successfully!")
        print("\n💡 What's next?")
        print("  • Try: python test_basic.py")
        print("  • For production: Set up API keys in .env")
        print("  • Full examples: python example_usage.py")
        print("  • Read the README.md for detailed instructions")

    except Exception as e:
        print(f"❌ Error running demo: {str(e)}")
        print("\n🔧 Try running manually:")
        print("  python simple_demo.py")

if __name__ == "__main__":
    main()