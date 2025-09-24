"""
Security Utilities - Security best practices for tool integration
"""

import os
import stat
from typing import List

def safe_file_operation(filename: str) -> str:
    """Validate filename for security"""
    # Prevent directory traversal attacks
    if ".." in filename or filename.startswith("/"):
        raise ValueError("Invalid filename - directory traversal detected")

    # Restrict file types
    allowed_extensions = [".txt", ".md", ".json", ".csv"]
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise ValueError("File type not allowed")

    return filename

def setup_secure_workspace(workspace_path: str = "./agent_workspace") -> str:
    """Create a secure workspace directory with proper permissions"""
    os.makedirs(workspace_path, exist_ok=True)

    # Set appropriate permissions (Unix/Linux)
    try:
        os.chmod(workspace_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
    except:
        pass  # Windows doesn't support chmod

    return workspace_path

def validate_tool_input(input_data: str, max_length: int = 10000) -> bool:
    """Validate tool input for basic security checks"""
    if len(input_data) > max_length:
        raise ValueError(f"Input too long: {len(input_data)} > {max_length}")

    # Check for potentially dangerous patterns
    dangerous_patterns = ["rm -rf", "del /", "__import__", "exec(", "eval("]
    for pattern in dangerous_patterns:
        if pattern in input_data.lower():
            raise ValueError(f"Potentially dangerous pattern detected: {pattern}")

    return True