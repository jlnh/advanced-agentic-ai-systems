#!/usr/bin/env python3
"""Basic health check for setup verification"""

import sys
from pathlib import Path

def check_project_structure():
    """Verify project structure is correct"""
    required_dirs = [
        "src/agentic_ai",
        "notebooks",
        "tests",
        "scripts",
        "docker"
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)
    
    if missing:
        print("❌ Missing directories:")
        for d in missing:
            print(f"   - {d}")
        return False
    
    print("✅ Project structure is correct")
    return True

def check_environment():
    """Check environment file exists"""
    if not Path(".env").exists():
        print("❌ .env file not found")
        return False
    
    print("✅ Environment file exists")
    return True

def check_dependencies():
    """Check key dependencies are installed"""
    try:
        import langchain
        import fastapi
        import pydantic
        print("✅ Core dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Dependency issue: {e}")
        return False

def main():
    print("🔍 Phase 1 Health Check")
    print("=" * 30)
    
    checks = [
        check_project_structure(),
        check_environment(),
        check_dependencies()
    ]
    
    if all(checks):
        print("\n🎉 Phase 1 setup is healthy!")
        print("Ready to proceed to Phase 2")
    else:
        print("\n❌ Setup issues found")
        print("Please review and fix before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()
