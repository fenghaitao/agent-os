#!/usr/bin/env python3
"""
Test runner for Agent OS

This script runs all tests in the tests/ directory.
"""

import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all tests."""
    print("Running Agent OS tests...\n")
    
    # Get the tests directory
    tests_dir = Path(__file__).parent / "tests"
    
    # Run basic tests
    print("=" * 50)
    print("Running basic tests...")
    print("=" * 50)
    
    result = subprocess.run([
        sys.executable, "test_basic.py"
    ], cwd=tests_dir)
    
    if result.returncode != 0:
        print("❌ Basic tests failed!")
        return 1
    
    print("\n✅ All tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(run_tests())
