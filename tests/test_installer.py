#!/usr/bin/env python3
"""
Test script for Agent OS Python installer.

This script tests the basic functionality of the Agent OS installer
without requiring actual network access.
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add the agent_os package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_os.installer import AgentOsInstaller
from agent_os.cli import cli


def test_installer_initialization():
    """Test installer initialization."""
    print("Testing installer initialization...")
    
    installer = AgentOsInstaller()
    assert installer.base_url == "https://raw.githubusercontent.com/fenghaitao/agent-os/main"
    assert not any(installer.platforms.values())
    
    installer.set_platforms(claude_code=True, cursor=True)
    assert installer.platforms['claude_code'] == True
    assert installer.platforms['cursor'] == True
    assert installer.platforms['github_copilot'] == False
    
    print("✓ Installer initialization test passed")


def test_installer_flags():
    """Test installer flag setting."""
    print("Testing installer flag setting...")
    
    installer = AgentOsInstaller()
    installer.set_overwrite_flags(instructions=True, standards=True)
    
    assert installer.overwrite_instructions == True
    assert installer.overwrite_standards == True
    assert installer.overwrite_config == False
    
    print("✓ Installer flag setting test passed")


def test_cli_help():
    """Test CLI help functionality."""
    print("Testing CLI help...")
    
    # This would normally be tested with subprocess, but for now we'll just
    # test that the CLI module can be imported and the cli function exists
    assert callable(cli)
    
    print("✓ CLI help test passed")


def test_package_structure():
    """Test that the package structure is correct."""
    print("Testing package structure...")
    
    package_dir = Path(__file__).parent / "agent_os"
    
    # Check required files exist
    required_files = [
        "__init__.py",
        "installer.py", 
        "cli.py"
    ]
    
    for file in required_files:
        assert (package_dir / file).exists(), f"Missing required file: {file}"
    
    print("✓ Package structure test passed")


def test_setup_files():
    """Test that setup files are present."""
    print("Testing setup files...")
    
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        "pyproject.toml",
        "MANIFEST.in"
    ]
    
    for file in required_files:
        assert (base_dir / file).exists(), f"Missing required file: {file}"
    
    print("✓ Setup files test passed")


def main():
    """Run all tests."""
    print("Running Agent OS installer tests...\n")
    
    try:
        test_package_structure()
        test_setup_files()
        test_installer_initialization()
        test_installer_flags()
        test_cli_help()
        
        print("\n🎉 All tests passed!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
