# scripts/verify_phase2.py
#!/usr/bin/env python3
"""Verification script for Phase 2 completion"""

import sys
from pathlib import Path

def check_file_structure():
    """Verify all required files exist"""
    required_files = [
        "src/agentic_ai/core/agents/base.py",
        "src/agentic_ai/core/agents/react_agent.py", 
        "src/agentic_ai/core/agents/specialized.py",
        "src/agentic_ai/core/tools/registry.py",
        "src/agentic_ai/core/memory/short_term.py",
        "src/agentic_ai/core/memory/long_term.py",
        "src/agentic_ai/core/memory/semantic_cache.py",
        "src/agentic_ai/core/orchestration/supervisor.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All core component files present")
    return True

def check_imports():
    """Verify imports work correctly"""
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        
        # Test core imports
        from agentic_ai.core.agents.base import BaseAgent
        from agentic_ai.core.agents.specialized import ResearchAgent, AnalystAgent, WriterAgent
        from agentic_ai.core.tools.registry import tool_registry
        from agentic_ai.core.orchestration.supervisor import SupervisorAgent
        
        print("✅ All imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def check_tool_registry():
    """Verify tool registry works"""
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        from agentic_ai.core.tools.registry import tool_registry
        
        tools = tool_registry.list_tools()
        expected_tools = ["web_search", "python_repl", "write_file", "read_file"]
        
        missing_tools = [tool for tool in expected_tools if tool not in tools]
        
        if missing_tools:
            print(f"❌ Missing tools: {missing_tools}")
            return False
        
        print(f"✅ Tool registry working ({len(tools)} tools available)")
        return True
        
    except Exception as e:
        print(f"❌ Tool registry error: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🔍 Phase 2 Verification")
    print("=" * 30)
    
    checks = [
        check_file_structure(),
        check_imports(),
        check_tool_registry()
    ]
    
    if all(checks):
        print("\n🎉 Phase 2 completed successfully!")
        print("Ready for Phase 3: Notebook Creation")
    else:
        print("\n❌ Phase 2 incomplete")
        print("Please fix issues before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()