#!/usr/bin/env python3
"""
Test Runner for Simics Watchdog Device Model

This script runs all tests (unit and integration) for the watchdog device model
and generates comprehensive test reports.
"""

import os
import sys
import unittest
import time
from datetime import datetime

# Add tests directory to path
test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, test_dir)

def run_all_tests():
    """Run both unit and integration tests"""
    print("=" * 80)
    print("SIMICS WATCHDOG DEVICE MODEL - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Test execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    # Run unit tests
    print("UNIT TESTS")
    print("-" * 40)
    try:
        from test_watchdog_unit import run_all_tests as run_unit_tests
        unit_success = run_unit_tests()
        # Note: In a real implementation, we'd capture the test results
        # For now, we'll assume success if no exceptions were thrown
        print("Unit tests completed successfully" if unit_success else "Unit tests failed")
    except Exception as e:
        print(f"Error running unit tests: {e}")
        unit_success = False
    
    print("\n" + "=" * 40)
    
    # Run integration tests
    print("INTEGRATION TESTS")
    print("-" * 40)
    try:
        from test_watchdog_integration import run_integration_tests
        integration_success = run_integration_tests()
        print("Integration tests completed successfully" if integration_success else "Integration tests failed")
    except Exception as e:
        print(f"Error running integration tests: {e}")
        integration_success = False
    
    # Generate summary report
    print("\n" + "=" * 80)
    print("TEST EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Unit Tests: {'PASSED' if unit_success else 'FAILED'}")
    print(f"Integration Tests: {'PASSED' if integration_success else 'FAILED'}")
    print(f"Overall Status: {'PASSED' if (unit_success and integration_success) else 'FAILED'}")
    print(f"Test execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return unit_success and integration_success

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)