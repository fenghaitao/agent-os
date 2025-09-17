#!/usr/bin/env python3
"""
Basic test script for Agent OS Python installer.

This script tests basic functionality without requiring external dependencies.
"""

import sys
from pathlib import Path


def test_package_structure():
    """Test that the package structure is correct."""
    print("Testing package structure...")
    
    package_dir = Path(__file__).parent.parent / "src"
    
    # Check required files exist
    required_files = [
        "__init__.py",
        "installer.py", 
        "cli.py"
    ]
    
    for file in required_files:
        if not (package_dir / file).exists():
            print(f"❌ Missing required file: {file}")
            return False
        print(f"✓ Found {file}")
    
    print("✓ Package structure test passed")
    return True


def test_setup_files():
    """Test that setup files are present."""
    print("Testing setup files...")
    
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        "pyproject.toml",
        "MANIFEST.in"
    ]
    
    for file in required_files:
        if not (base_dir / file).exists():
            print(f"❌ Missing required file: {file}")
            return False
        print(f"✓ Found {file}")
    
    print("✓ Setup files test passed")
    return True


def test_file_contents():
    """Test that key files have expected content."""
    print("Testing file contents...")
    
    # Test pyproject.toml has required content
    pyproject_toml = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_toml.exists():
        content = pyproject_toml.read_text()
        if "agent-os" in content and "src.cli:main" in content:
            print("✓ pyproject.toml has expected content")
        else:
            print("❌ pyproject.toml missing expected content")
            return False
    
    # Test pyproject.toml has dependencies
    pyproject_toml = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_toml.exists():
        content = pyproject_toml.read_text()
        if "requests" in content and "click" in content and "rich" in content:
            print("✓ pyproject.toml has expected dependencies")
        else:
            print("❌ pyproject.toml missing expected dependencies")
            return False
    
    print("✓ File contents test passed")
    return True


def test_import_structure():
    """Test that the package can be imported (without dependencies)."""
    print("Testing import structure...")
    
    try:
        # Test that __init__.py can be read
        init_file = Path(__file__).parent.parent / "src" / "__init__.py"
        content = init_file.read_text()
        
        if "AgentOsInstaller" in content and "cli_main" in content:
            print("✓ __init__.py has expected exports")
        else:
            print("❌ __init__.py missing expected exports")
            return False
        
        # Test that installer.py has expected classes
        installer_file = Path(__file__).parent.parent / "src" / "installer.py"
        content = installer_file.read_text()
        
        if "class AgentOsInstaller" in content and "def install" in content:
            print("✓ installer.py has expected structure")
        else:
            print("❌ installer.py missing expected structure")
            return False
        
        # Test that cli.py has expected functions
        cli_file = Path(__file__).parent.parent / "src" / "cli.py"
        content = cli_file.read_text()
        
        if "def cli" in content and "def main" in content:
            print("✓ cli.py has expected structure")
        else:
            print("❌ cli.py missing expected structure")
            return False
        
        print("✓ Import structure test passed")
        return True
        
    except Exception as e:
        print(f"❌ Import structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Running Agent OS basic tests...\n")
    
    tests = [
        test_package_structure,
        test_setup_files,
        test_file_contents,
        test_import_structure,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}\n")
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
