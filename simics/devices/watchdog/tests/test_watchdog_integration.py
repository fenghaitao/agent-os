#!/usr/bin/env python3
"""
Integration Test Suite for Simics Watchdog Device Model

This test suite validates the watchdog device integration with Simics
platform components and real-time behavior.

Integration Test Categories:
1. Platform Integration Tests
2. Real-time Timing Tests
3. Signal Interface Tests
4. Multi-device Interaction Tests
5. Performance Tests
6. Stress Tests
"""

import sys
import time
import threading
import unittest
from typing import Dict, List, Tuple

class MockPlatform:
    """Mock platform for integration testing"""
    
    def __init__(self, platform_type: str = "qsp"):
        self.platform_type = platform_type
        self.devices = {}
        self.interrupt_controller = MockInterruptController()
        self.reset_controller = MockResetController()
        self.memory_map = {}
        self.signals = {}
        
    def add_device(self, name: str, device, base_addr: int):
        """Add device to platform"""
        self.devices[name] = device
        self.memory_map[base_addr] = device
        
    def connect_signal(self, source: str, target: str):
        """Connect signal between devices"""
        self.signals[source] = target


class MockInterruptController:
    """Mock interrupt controller"""
    
    def __init__(self):
        self.irq_lines = {}
        self.interrupt_count = 0
        
    def assert_irq(self, line: int):
        """Assert interrupt line"""
        self.irq_lines[line] = True
        self.interrupt_count += 1
        
    def deassert_irq(self, line: int):
        """Deassert interrupt line"""
        self.irq_lines[line] = False
        
    def is_irq_asserted(self, line: int) -> bool:
        """Check if interrupt line is asserted"""
        return self.irq_lines.get(line, False)


class MockResetController:
    """Mock reset controller"""
    
    def __init__(self):
        self.reset_signals = {}
        self.reset_count = 0
        
    def assert_reset(self, source: str):
        """Assert reset signal"""
        self.reset_signals[source] = True
        self.reset_count += 1
        
    def deassert_reset(self, source: str):
        """Deassert reset signal"""
        self.reset_signals[source] = False
        
    def is_reset_asserted(self, source: str) -> bool:
        """Check if reset is asserted"""
        return self.reset_signals.get(source, False)


class TestWatchdogPlatformIntegration(unittest.TestCase):
    """Test watchdog integration with different platforms"""
    
    def setUp(self):
        from test_watchdog_unit import MockSimicsDevice
        self.qsp_platform = MockPlatform("qsp")
        self.spr_platform = MockPlatform("spr")
        self.gnr_platform = MockPlatform("gnr")
        
    def test_qsp_platform_integration(self):
        """Test QSP platform integration"""
        from test_watchdog_unit import MockSimicsDevice
        
        # Create watchdog for QSP platform
        watchdog = MockSimicsDevice()
        self.qsp_platform.add_device("watchdog", watchdog, 0x40010000)
        
        # Configure for QSP (embedded system)
        watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        watchdog.write_register('WDOGLOAD', 0x2FAF080)  # 30 seconds at 1 MHz
        watchdog.write_register('WDOGCONTROL', 0x0B)    # step_value=2 (250 MHz), INTEN=1, RESEN=1
        
        # Verify QSP-specific configuration
        self.assertTrue(watchdog.timer_enabled)
        control = watchdog.read_register('WDOGCONTROL')
        step_value = (control >> 2) & 0x7
        self.assertEqual(step_value, 2)  # 250 MHz for embedded
        
    def test_spr_platform_integration(self):
        """Test SPR server platform integration"""
        from test_watchdog_unit import MockSimicsDevice
        
        # Create watchdog for SPR platform
        watchdog = MockSimicsDevice()
        self.spr_platform.add_device("watchdog", watchdog, 0xFED40000)
        
        # Configure for SPR (server)
        watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        watchdog.write_register('WDOGLOAD', 0x5F5E100)   # 5 minutes at 1 MHz
        watchdog.write_register('WDOGCONTROL', 0x03)     # step_value=0 (1 GHz), INTEN=1, RESEN=1
        
        # Verify SPR-specific configuration
        self.assertTrue(watchdog.timer_enabled)
        control = watchdog.read_register('WDOGCONTROL')
        step_value = (control >> 2) & 0x7
        self.assertEqual(step_value, 0)  # 1 GHz for server
        
    def test_gnr_redundant_watchdog_integration(self):
        """Test GNR platform with redundant watchdogs"""
        from test_watchdog_unit import MockSimicsDevice
        
        # Create primary and backup watchdogs for GNR
        primary_wdt = MockSimicsDevice()
        backup_wdt = MockSimicsDevice()
        
        self.gnr_platform.add_device("watchdog_primary", primary_wdt, 0xFED50000)
        self.gnr_platform.add_device("watchdog_backup", backup_wdt, 0xFED51000)
        
        # Configure primary watchdog
        primary_wdt.write_register('WDOGLOCK', 0x1ACCE551)
        primary_wdt.write_register('WDOGLOAD', 0x1C9C380)  # 2 minutes
        primary_wdt.write_register('WDOGCONTROL', 0x03)
        
        # Configure backup watchdog
        backup_wdt.write_register('WDOGLOCK', 0x1ACCE551)
        backup_wdt.write_register('WDOGLOAD', 0x2FAF080)   # 5 minutes
        backup_wdt.write_register('WDOGCONTROL', 0x07)     # step_value=1, slower
        
        # Verify both watchdogs are running
        self.assertTrue(primary_wdt.timer_enabled)
        self.assertTrue(backup_wdt.timer_enabled)
        
        # Test failover scenario
        primary_wdt.write_register('WDOGCONTROL', 0x00)    # Disable primary
        self.assertFalse(primary_wdt.timer_enabled)
        self.assertTrue(backup_wdt.timer_enabled)          # Backup still running


class TestWatchdogSignalInterface(unittest.TestCase):
    """Test signal interface integration"""
    
    def setUp(self):
        from test_watchdog_unit import MockSimicsDevice
        self.platform = MockPlatform()
        self.watchdog = MockSimicsDevice()
        self.platform.add_device("watchdog", self.watchdog, 0x40000000)
        
    def test_interrupt_signal_routing(self):
        """Test interrupt signal routing to interrupt controller"""
        # Connect watchdog interrupt to controller
        self.platform.connect_signal("watchdog.wdogint", "interrupt_controller.irq[32]")
        
        # Configure and trigger interrupt
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        self.watchdog.write_register('WDOGLOAD', 0x1000)
        self.watchdog.write_register('WDOGCONTROL', 0x1)
        
        # Simulate timeout to generate interrupt
        self.watchdog.simulate_timeout()
        
        # Verify interrupt signal is active
        self.assertTrue(self.watchdog.get_signal('wdogint'))
        
        # Clear interrupt and verify signal is deasserted
        self.watchdog.write_register('WDOGINTCLR', 0x1)
        self.assertFalse(self.watchdog.get_signal('wdogint'))
        
    def test_reset_signal_routing(self):
        """Test reset signal routing to reset controller"""
        # Connect watchdog reset to controller
        self.platform.connect_signal("watchdog.wdogreset", "reset_controller.watchdog_reset")
        
        # Configure for reset escalation
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        self.watchdog.write_register('WDOGLOAD', 0x1000)
        self.watchdog.write_register('WDOGCONTROL', 0x3)  # Enable interrupt and reset
        
        # First timeout - interrupt only
        self.watchdog.simulate_timeout()
        self.assertTrue(self.watchdog.get_signal('wdogint'))
        self.assertFalse(self.watchdog.get_signal('wdogreset'))
        
        # Second timeout - reset escalation
        self.watchdog.simulate_timeout()
        self.assertTrue(self.watchdog.get_signal('wdogreset'))
        
    def test_integration_test_mode_signals(self):
        """Test direct signal control in integration test mode"""
        # Enable test mode
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        self.watchdog.write_register('WDOGITCR', 0x1)
        
        # Test direct interrupt control
        self.watchdog.write_register('WDOGITOP', 0x2)  # Assert interrupt
        self.assertTrue(self.watchdog.get_signal('wdogint'))
        
        # Test direct reset control
        self.watchdog.write_register('WDOGITOP', 0x1)  # Assert reset
        self.assertTrue(self.watchdog.get_signal('wdogreset'))
        
        # Test simultaneous control
        self.watchdog.write_register('WDOGITOP', 0x3)  # Assert both
        self.assertTrue(self.watchdog.get_signal('wdogint'))
        self.assertTrue(self.watchdog.get_signal('wdogreset'))


class TestWatchdogTimingAccuracy(unittest.TestCase):
    """Test timing accuracy and real-time behavior"""
    
    def setUp(self):
        from test_watchdog_unit import MockSimicsDevice
        self.watchdog = MockSimicsDevice()
        
    def test_step_value_timing_accuracy(self):
        """Test timing accuracy with different step values"""
        test_cases = [
            (0, 1),      # 1 GHz
            (1, 2),      # 500 MHz  
            (2, 4),      # 250 MHz
            (3, 8),      # 125 MHz
            (4, 16),     # 62.5 MHz
        ]
        
        for step_value, expected_divisor in test_cases:
            with self.subTest(step_value=step_value):
                # Configure watchdog with specific step value
                self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
                control_val = (step_value << 2) | 0x1
                self.watchdog.write_register('WDOGCONTROL', control_val)
                
                # Verify step value is set correctly
                control = self.watchdog.read_register('WDOGCONTROL')
                actual_step = (control >> 2) & 0x7
                self.assertEqual(actual_step, step_value)
                
    def test_counter_accuracy(self):
        """Test counter value accuracy"""
        # Set known load value
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        self.watchdog.write_register('WDOGLOAD', 0x10000)
        
        # Enable timer
        self.watchdog.write_register('WDOGCONTROL', 0x1)
        
        # Verify counter starts at load value
        self.assertEqual(self.watchdog.read_register('WDOGVALUE'), 0x10000)
        
        # Verify load value is preserved
        self.assertEqual(self.watchdog.read_register('WDOGLOAD'), 0x10000)


class TestWatchdogMultiDeviceInteraction(unittest.TestCase):
    """Test interactions between multiple watchdog devices"""
    
    def setUp(self):
        from test_watchdog_unit import MockSimicsDevice
        self.platform = MockPlatform("gnr")
        self.primary_wdt = MockSimicsDevice()
        self.backup_wdt = MockSimicsDevice()
        
        self.platform.add_device("primary", self.primary_wdt, 0xFED50000)
        self.platform.add_device("backup", self.backup_wdt, 0xFED51000)
        
    def test_redundant_watchdog_operation(self):
        """Test redundant watchdog operation"""
        # Configure both watchdogs
        for wdt in [self.primary_wdt, self.backup_wdt]:
            wdt.write_register('WDOGLOCK', 0x1ACCE551)
            wdt.write_register('WDOGLOAD', 0x10000)
            wdt.write_register('WDOGCONTROL', 0x3)
            
        # Both should be running
        self.assertTrue(self.primary_wdt.timer_enabled)
        self.assertTrue(self.backup_wdt.timer_enabled)
        
        # Simulate primary timeout
        self.primary_wdt.simulate_timeout()
        self.assertTrue(self.primary_wdt.interrupt_pending)
        self.assertTrue(self.backup_wdt.timer_enabled)  # Backup still running
        
    def test_watchdog_isolation(self):
        """Test that watchdogs operate independently"""
        # Configure different timeouts
        self.primary_wdt.write_register('WDOGLOCK', 0x1ACCE551)
        self.primary_wdt.write_register('WDOGLOAD', 0x1000)
        self.primary_wdt.write_register('WDOGCONTROL', 0x1)
        
        self.backup_wdt.write_register('WDOGLOCK', 0x1ACCE551)
        self.backup_wdt.write_register('WDOGLOAD', 0x2000)
        self.backup_wdt.write_register('WDOGCONTROL', 0x1)
        
        # Trigger timeout on primary only
        self.primary_wdt.simulate_timeout()
        
        # Primary should have interrupt, backup should not
        self.assertTrue(self.primary_wdt.interrupt_pending)
        self.assertFalse(self.backup_wdt.interrupt_pending)
        
        # Clear primary interrupt
        self.primary_wdt.write_register('WDOGINTCLR', 0x1)
        self.assertFalse(self.primary_wdt.interrupt_pending)
        self.assertFalse(self.backup_wdt.interrupt_pending)  # Backup unaffected


class TestWatchdogPerformance(unittest.TestCase):
    """Test watchdog performance characteristics"""
    
    def setUp(self):
        from test_watchdog_unit import MockSimicsDevice
        self.watchdog = MockSimicsDevice()
        
    def test_register_access_performance(self):
        """Test register access performance"""
        # Unlock device
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        
        # Measure time for register operations
        start_time = time.time()
        
        # Perform many register operations
        for i in range(1000):
            self.watchdog.write_register('WDOGLOAD', i)
            value = self.watchdog.read_register('WDOGLOAD')
            self.assertEqual(value, i)
            
        end_time = time.time()
        operation_time = end_time - start_time
        
        # Verify reasonable performance (should complete quickly)
        self.assertLess(operation_time, 1.0)  # Should complete in under 1 second
        
    def test_rapid_timer_operations(self):
        """Test rapid timer enable/disable operations"""
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        self.watchdog.write_register('WDOGLOAD', 0x1000)
        
        # Rapidly enable and disable timer
        for i in range(100):
            self.watchdog.write_register('WDOGCONTROL', 0x1)  # Enable
            self.assertTrue(self.watchdog.timer_enabled)
            
            self.watchdog.write_register('WDOGCONTROL', 0x0)  # Disable
            self.assertFalse(self.watchdog.timer_enabled)


class TestWatchdogStressConditions(unittest.TestCase):
    """Test watchdog under stress conditions"""
    
    def setUp(self):
        from test_watchdog_unit import MockSimicsDevice
        self.watchdog = MockSimicsDevice()
        
    def test_rapid_interrupt_generation(self):
        """Test rapid interrupt generation and clearing"""
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        self.watchdog.write_register('WDOGLOAD', 0x100)
        self.watchdog.write_register('WDOGCONTROL', 0x1)
        
        # Generate and clear interrupts rapidly
        for i in range(50):
            # Simulate timeout
            self.watchdog.simulate_timeout()
            self.assertTrue(self.watchdog.interrupt_pending)
            
            # Clear interrupt
            self.watchdog.write_register('WDOGINTCLR', 0x1)
            self.assertFalse(self.watchdog.interrupt_pending)
            
    def test_lock_unlock_stress(self):
        """Test rapid lock/unlock operations"""
        for i in range(100):
            # Lock device
            self.watchdog.write_register('WDOGLOCK', 0x12345678)
            self.assertTrue(self.watchdog.device_locked)
            
            # Unlock device
            self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
            self.assertFalse(self.watchdog.device_locked)
            
    def test_boundary_conditions(self):
        """Test boundary conditions"""
        self.watchdog.write_register('WDOGLOCK', 0x1ACCE551)
        
        # Test maximum load value
        self.watchdog.write_register('WDOGLOAD', 0xFFFFFFFF)
        self.assertEqual(self.watchdog.read_register('WDOGLOAD'), 0xFFFFFFFF)
        
        # Test minimum load value
        self.watchdog.write_register('WDOGLOAD', 0x0)
        self.assertEqual(self.watchdog.read_register('WDOGLOAD'), 0x0)
        
        # Test maximum step value
        self.watchdog.write_register('WDOGCONTROL', 0x1D)  # step_value=7, max value
        control = self.watchdog.read_register('WDOGCONTROL')
        step_value = (control >> 2) & 0x7
        self.assertEqual(step_value, 7)


def create_integration_test_suite():
    """Create comprehensive integration test suite"""
    suite = unittest.TestSuite()
    
    # Add all integration test classes
    test_classes = [
        TestWatchdogPlatformIntegration,
        TestWatchdogSignalInterface,
        TestWatchdogTimingAccuracy,
        TestWatchdogMultiDeviceInteraction,
        TestWatchdogPerformance,
        TestWatchdogStressConditions
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_integration_tests():
    """Run complete integration test suite"""
    print("Simics Watchdog Device Model - Integration Tests")
    print("=" * 60)
    
    suite = create_integration_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Integration Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run integration tests
    success = run_integration_tests()
    sys.exit(0 if success else 1)