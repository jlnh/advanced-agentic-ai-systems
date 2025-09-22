# scripts/setup_project.py
#!/usr/bin/env python3
"""One-click project setup script"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

def run_command(command, description, exit_on_error=True):
    """Run shell command with error handling"""
    print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        if exit_on_error:
            sys.exit(1)
        return None

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    requirements = {
        "python3": "Python 3.11+",
        "pip": "Python package manager",
        "git": "Version control",
        "docker": "Containerization (optional)"
    }
    
    missing = []
    for cmd, desc in requirements.items():
        if shutil.which(cmd) is None:
            missing.append(f"{cmd} ({desc})")
    
    if missing:
        print("❌ Missing requirements:")
        for item in missing:
            print(f"   - {item}")
        print("\nPlease install missing tools and try again.")
        sys.exit(1)
    
    print("✅ All prerequisites satisfied")

def setup_environment():
    """Set up Python virtual environment and dependencies"""
    
    # Create virtual environment
    if not Path("venv").exists():
        run_command("python -m venv venv", "Creating virtual environment")
    
    # Activate and install dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix-like
        pip_cmd = "venv/bin/pip"
    
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    run_command(f"{pip_cmd} install -e '.[dev]'", "Installing project dependencies")

def setup_environment_file():
    """Create .env file from template"""
    env_file = Path(".env")
    template_file = Path(".env.template")
    
    if not env_file.exists() and template_file.exists():
        shutil.copy(template_file, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your API keys:")
        print("   - OPENAI_API_KEY")
        print("   - LANGCHAIN_API_KEY (optional)")
    else:
        print("ℹ️  .env file already exists")

def create_workspace():
    """Create workspace directory for file operations"""
    workspace = Path("workspace")
    workspace.mkdir(exist_ok=True)
    print("✅ Created workspace directory")

def print_next_steps():
    """Print what to do next"""
    print("\n" + "=" * 60)
    print("🎉 PHASE 1 SETUP COMPLETE!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your API keys")
    print("2. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("3. Proceed to Phase 2: Core Foundation Development")
    print("4. Or jump ahead to Phase 3: Notebook Creation")

def main():
    """Main setup function"""
    print("🚀 Advanced Agentic AI Systems - Phase 1: Initialization")
    print("=" * 60)
    
    check_prerequisites()
    setup_environment()
    setup_environment_file()
    create_workspace()
    print_next_steps()

if __name__ == "__main__":
    main()