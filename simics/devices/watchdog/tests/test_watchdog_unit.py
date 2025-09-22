#!/usr/bin/env python3
"""
Comprehensive Unit Test Suite for Simics Watchdog Device Model

This test suite provides comprehensive validation of the watchdog device
functionality including register access, timer operations, interrupt handling,
security mechanisms, and platform integration.

Test Categories:
1. Register Access Tests
2. Timer Functionality Tests  
3. Interrupt System Tests
4. Security Mechanism Tests
5. Integration Test Mode Tests
6. Platform Integration Tests
7. Error Condition Tests
"""

import sys
import time
import unittest
from typing import Dict, Any, Optional

# Mock Simics framework for testing
class MockSimicsDevice:
    """Mock device for unit testing"""
    
    def __init__(self):
        self.registers = {
            'WDOGLOAD': 0xFFFFFFFF,
            'WDOGVALUE': 0xFFFFFFFF,
            'WDOGCONTROL': 0x00000000,
            'WDOGINTCLR': 0x00000000,
            'WDOGRIS': 0x00000000,
            'WDOGMIS': 0x00000000,
            'WDOGLOCK': 0x00000000,
            'WDOGITCR': 0x00000000,
            'WDOGITOP': 0x00000000,
            'PeripheralID0': 0x05,
            'PeripheralID1': 0xB8,
            'PeripheralID2': 0x1B,
            'PeripheralID3': 0x04,
            'PrimeCellID0': 0x0D,
            'PrimeCellID1': 0xF0,
            'PrimeCellID2': 0x05,
            'PrimeCellID3': 0xB1
        }
        self.device_locked = True
        self.timer_enabled = False
        self.interrupt_pending = False
        self.reset_pending = False
        self.test_mode = False
        self.counter_value = 0xFFFFFFFF
        self.load_value = 0xFFFFFFFF
        self.signals = {'wdogint': False, 'wdogreset': False}
        
    def read_register(self, reg_name: str) -> int:
        """Read register value"""
        if reg_name == 'WDOGVALUE':
            return self.counter_value
        elif reg_name == 'WDOGRIS':
            return 1 if self.interrupt_pending else 0
        elif reg_name == 'WDOGMIS':
            inten = self.registers['WDOGCONTROL'] & 0x1
            return 1 if (self.interrupt_pending and inten) else 0
        elif reg_name == 'WDOGLOCK':
            return 0x00000001 if self.device_locked else 0x00000000
        return self.registers.get(reg_name, 0)
    
    def write_register(self, reg_name: str, value: int) -> bool:
        """Write register value"""
        # Check write access for most registers
        if reg_name not in ['WDOGLOCK'] and self.device_locked:
            return False
            
        if reg_name == 'WDOGLOAD':
            self.load_value = value
            self.registers[reg_name] = value
            if not self.timer_enabled:
                self.counter_value = value
        elif reg_name == 'WDOGCONTROL':
            old_inten = self.registers[reg_name] & 0x1
            # Mask to only allow valid bits (4:0)
            value = value & 0x1F
            self.registers[reg_name] = value
            new_inten = value & 0x1
            
            # Handle timer enable/disable
            if old_inten == 0 and new_inten == 1:
                self.timer_enabled = True
                self.counter_value = self.load_value
            elif old_inten == 1 and new_inten == 0:
                self.timer_enabled = False
        elif reg_name == 'WDOGINTCLR':
            if self.interrupt_pending:
                self.interrupt_pending = False
                self.counter_value = self.load_value
                self.signals['wdogint'] = False
        elif reg_name == 'WDOGLOCK':
            self.registers[reg_name] = value
            if value == 0x1ACCE551:
                self.device_locked = False
            else:
                self.device_locked = True
        elif reg_name == 'WDOGITCR':
            if not self.device_locked:
                self.test_mode = (value & 0x1) != 0
                self.registers[reg_name] = value
        elif reg_name == 'WDOGITOP':
            if not self.device_locked and self.test_mode:
                test_int = (value & 0x2) != 0
                test_reset = (value & 0x1) != 0
                self.signals['wdogint'] = test_int
                self.signals['wdogreset'] = test_reset
        else:
            # Read-only registers
            if reg_name in ['WDOGVALUE', 'WDOGRIS', 'WDOGMIS', 
                           'PeripheralID0', 'PeripheralID1', 'PeripheralID2', 'PeripheralID3',
                           'PrimeCellID0', 'PrimeCellID1', 'PrimeCellID2', 'PrimeCellID3']:
                return False
            self.registers[reg_name] = value
        
        return True
    
    def simulate_timeout(self):
        """Simulate timer timeout for testing"""
        if self.timer_enabled:
            if not self.interrupt_pending:
                # First timeout - generate interrupt
                self.interrupt_pending = True
                self.signals['wdogint'] = True
                self.counter_value = self.load_value
            else:
                # Second timeout - generate reset if enabled
                resen = (self.registers['WDOGCONTROL'] >> 1) & 0x1
                if resen:
                    self.reset_pending = True
                    self.signals['wdogreset'] = True
                self.timer_enabled = False
    
    def get_signal(self, signal_name: str) -> bool:
        """Get signal state"""
        return self.signals.get(signal_name, False)


class TestWatchdogRegisterAccess(unittest.TestCase):
    """Test register access functionality"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
    
    def test_register_reset_values(self):
        """Test all registers have correct reset values"""
        self.assertEqual(self.device.read_register('WDOGLOAD'), 0xFFFFFFFF)
        self.assertEqual(self.device.read_register('WDOGVALUE'), 0xFFFFFFFF)
        self.assertEqual(self.device.read_register('WDOGCONTROL'), 0x00000000)
        self.assertEqual(self.device.read_register('WDOGRIS'), 0x00000000)
        self.assertEqual(self.device.read_register('WDOGMIS'), 0x00000000)
        self.assertEqual(self.device.read_register('WDOGLOCK'), 0x00000001)  # Locked
        
    def test_peripheral_id_registers(self):
        """Test Peripheral ID registers are read-only with correct values"""
        self.assertEqual(self.device.read_register('PeripheralID0'), 0x05)
        self.assertEqual(self.device.read_register('PeripheralID1'), 0xB8)
        self.assertEqual(self.device.read_register('PeripheralID2'), 0x1B)
        self.assertEqual(self.device.read_register('PeripheralID3'), 0x04)
        
        # Verify read-only nature
        self.assertFalse(self.device.write_register('PeripheralID0', 0x12345678))
        self.assertEqual(self.device.read_register('PeripheralID0'), 0x05)
    
    def test_primecell_id_registers(self):
        """Test PrimeCell ID registers are read-only with correct values"""
        self.assertEqual(self.device.read_register('PrimeCellID0'), 0x0D)
        self.assertEqual(self.device.read_register('PrimeCellID1'), 0xF0)
        self.assertEqual(self.device.read_register('PrimeCellID2'), 0x05)
        self.assertEqual(self.device.read_register('PrimeCellID3'), 0xB1)
        
        # Verify read-only nature
        self.assertFalse(self.device.write_register('PrimeCellID0', 0x12345678))
        self.assertEqual(self.device.read_register('PrimeCellID0'), 0x0D)


class TestWatchdogSecurity(unittest.TestCase):
    """Test security lock mechanism"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
    
    def test_initial_locked_state(self):
        """Test device starts in locked state"""
        self.assertTrue(self.device.device_locked)
        self.assertEqual(self.device.read_register('WDOGLOCK'), 0x00000001)
    
    def test_unlock_sequence(self):
        """Test correct unlock sequence"""
        # Unlock with magic value
        self.assertTrue(self.device.write_register('WDOGLOCK', 0x1ACCE551))
        self.assertFalse(self.device.device_locked)
        self.assertEqual(self.device.read_register('WDOGLOCK'), 0x00000000)
    
    def test_lock_sequence(self):
        """Test locking device"""
        # First unlock
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
        self.assertFalse(self.device.device_locked)
        
        # Lock with any other value
        self.device.write_register('WDOGLOCK', 0x12345678)
        self.assertTrue(self.device.device_locked)
        self.assertEqual(self.device.read_register('WDOGLOCK'), 0x00000001)
    
    def test_write_protection_when_locked(self):
        """Test write protection when device is locked"""
        # Ensure device is locked
        self.assertTrue(self.device.device_locked)
        
        # Attempt to write protected registers
        self.assertFalse(self.device.write_register('WDOGLOAD', 0x12345678))
        self.assertFalse(self.device.write_register('WDOGCONTROL', 0x00000003))
        
        # Verify values haven't changed
        self.assertEqual(self.device.read_register('WDOGLOAD'), 0xFFFFFFFF)
        self.assertEqual(self.device.read_register('WDOGCONTROL'), 0x00000000)
    
    def test_write_access_when_unlocked(self):
        """Test write access when device is unlocked"""
        # Unlock device
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
        
        # Write to protected registers
        self.assertTrue(self.device.write_register('WDOGLOAD', 0x12345678))
        self.assertTrue(self.device.write_register('WDOGCONTROL', 0x00000003))
        
        # Verify values have changed
        self.assertEqual(self.device.read_register('WDOGLOAD'), 0x12345678)
        self.assertEqual(self.device.read_register('WDOGCONTROL'), 0x00000003)


class TestWatchdogTimerFunctionality(unittest.TestCase):
    """Test timer functionality"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
        # Unlock device for testing
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
    
    def test_timer_enable_disable(self):
        """Test timer enable and disable"""
        # Set load value
        self.device.write_register('WDOGLOAD', 0x1000)
        
        # Enable timer (INTEN=1)
        self.device.write_register('WDOGCONTROL', 0x1)
        self.assertTrue(self.device.timer_enabled)
        self.assertEqual(self.device.counter_value, 0x1000)
        
        # Disable timer (INTEN=0)
        self.device.write_register('WDOGCONTROL', 0x0)
        self.assertFalse(self.device.timer_enabled)
    
    def test_load_value_update(self):
        """Test load value updates counter when timer disabled"""
        # Set initial load value
        self.device.write_register('WDOGLOAD', 0x1000)
        self.assertEqual(self.device.counter_value, 0x1000)
        
        # Change load value while timer disabled
        self.device.write_register('WDOGLOAD', 0x2000)
        self.assertEqual(self.device.counter_value, 0x2000)
        self.assertEqual(self.device.load_value, 0x2000)
    
    def test_counter_reload_on_timer_enable(self):
        """Test counter reloads when timer is enabled"""
        # Set load value
        self.device.write_register('WDOGLOAD', 0x5000)
        
        # Manually change counter value
        self.device.counter_value = 0x1000
        
        # Enable timer - should reload counter
        self.device.write_register('WDOGCONTROL', 0x1)
        self.assertEqual(self.device.counter_value, 0x5000)


class TestWatchdogInterruptSystem(unittest.TestCase):
    """Test interrupt generation and handling"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
        # Unlock device for testing
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
    
    def test_first_timeout_interrupt_generation(self):
        """Test interrupt generation on first timeout"""
        # Configure timer
        self.device.write_register('WDOGLOAD', 0x1000)
        self.device.write_register('WDOGCONTROL', 0x1)  # INTEN=1
        
        # Simulate timeout
        self.device.simulate_timeout()
        
        # Check interrupt status
        self.assertTrue(self.device.interrupt_pending)
        self.assertEqual(self.device.read_register('WDOGRIS'), 1)
        self.assertEqual(self.device.read_register('WDOGMIS'), 1)
        self.assertTrue(self.device.get_signal('wdogint'))
    
    def test_interrupt_masking(self):
        """Test interrupt masking with INTEN bit"""
        # Generate interrupt
        self.device.interrupt_pending = True
        
        # With INTEN=0, masked interrupt should be 0
        self.device.write_register('WDOGCONTROL', 0x0)
        self.assertEqual(self.device.read_register('WDOGRIS'), 1)  # Raw interrupt still set
        self.assertEqual(self.device.read_register('WDOGMIS'), 0)  # Masked interrupt clear
        
        # With INTEN=1, masked interrupt should be 1
        self.device.write_register('WDOGCONTROL', 0x1)
        self.assertEqual(self.device.read_register('WDOGMIS'), 1)  # Masked interrupt set
    
    def test_interrupt_clear(self):
        """Test interrupt clearing"""
        # Set up interrupt condition
        self.device.write_register('WDOGLOAD', 0x2000)
        self.device.write_register('WDOGCONTROL', 0x1)
        self.device.simulate_timeout()
        
        # Verify interrupt is pending
        self.assertTrue(self.device.interrupt_pending)
        self.assertEqual(self.device.read_register('WDOGRIS'), 1)
        
        # Clear interrupt
        self.device.write_register('WDOGINTCLR', 0x1)
        
        # Verify interrupt is cleared and counter reloaded
        self.assertFalse(self.device.interrupt_pending)
        self.assertEqual(self.device.read_register('WDOGRIS'), 0)
        self.assertEqual(self.device.counter_value, 0x2000)
        self.assertFalse(self.device.get_signal('wdogint'))


class TestWatchdogResetEscalation(unittest.TestCase):
    """Test reset escalation functionality"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
        # Unlock device for testing
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
    
    def test_reset_on_second_timeout(self):
        """Test reset generation on second timeout"""
        # Configure timer with reset enabled
        self.device.write_register('WDOGLOAD', 0x1000)
        self.device.write_register('WDOGCONTROL', 0x3)  # INTEN=1, RESEN=1
        
        # First timeout - should generate interrupt
        self.device.simulate_timeout()
        self.assertTrue(self.device.interrupt_pending)
        self.assertFalse(self.device.reset_pending)
        
        # Second timeout - should generate reset
        self.device.simulate_timeout()
        self.assertTrue(self.device.reset_pending)
        self.assertTrue(self.device.get_signal('wdogreset'))
        self.assertFalse(self.device.timer_enabled)  # Timer should stop
    
    def test_no_reset_when_resen_disabled(self):
        """Test no reset when RESEN is disabled"""
        # Configure timer with reset disabled
        self.device.write_register('WDOGLOAD', 0x1000)
        self.device.write_register('WDOGCONTROL', 0x1)  # INTEN=1, RESEN=0
        
        # First timeout
        self.device.simulate_timeout()
        self.assertTrue(self.device.interrupt_pending)
        
        # Second timeout - should not generate reset
        self.device.simulate_timeout()
        self.assertFalse(self.device.reset_pending)
        self.assertFalse(self.device.get_signal('wdogreset'))


class TestWatchdogIntegrationTestMode(unittest.TestCase):
    """Test integration test mode functionality"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
        # Unlock device for testing
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
    
    def test_test_mode_enable_disable(self):
        """Test integration test mode enable/disable"""
        # Enable test mode
        self.device.write_register('WDOGITCR', 0x1)
        self.assertTrue(self.device.test_mode)
        self.assertEqual(self.device.read_register('WDOGITCR'), 0x1)
        
        # Disable test mode
        self.device.write_register('WDOGITCR', 0x0)
        self.assertFalse(self.device.test_mode)
        self.assertEqual(self.device.read_register('WDOGITCR'), 0x0)
    
    def test_direct_signal_control(self):
        """Test direct signal control in test mode"""
        # Enable test mode
        self.device.write_register('WDOGITCR', 0x1)
        
        # Test interrupt signal control
        self.device.write_register('WDOGITOP', 0x2)  # test_wdogint=1
        self.assertTrue(self.device.get_signal('wdogint'))
        
        # Test reset signal control
        self.device.write_register('WDOGITOP', 0x1)  # test_wdogres=1
        self.assertTrue(self.device.get_signal('wdogreset'))
        
        # Test both signals
        self.device.write_register('WDOGITOP', 0x3)  # Both signals
        self.assertTrue(self.device.get_signal('wdogint'))
        self.assertTrue(self.device.get_signal('wdogreset'))
    
    def test_test_mode_protection(self):
        """Test test mode is protected when device locked"""
        # Lock device
        self.device.write_register('WDOGLOCK', 0x12345678)
        
        # Attempt to enable test mode
        self.assertFalse(self.device.write_register('WDOGITCR', 0x1))
        self.assertFalse(self.device.test_mode)


class TestWatchdogErrorConditions(unittest.TestCase):
    """Test error conditions and edge cases"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
    
    def test_read_only_register_writes(self):
        """Test writes to read-only registers are ignored"""
        # Unlock device first
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
        
        # Attempt to write read-only registers
        original_value = self.device.read_register('WDOGVALUE')
        self.assertFalse(self.device.write_register('WDOGVALUE', 0x12345678))
        self.assertEqual(self.device.read_register('WDOGVALUE'), original_value)
        
        # Test status registers
        self.assertFalse(self.device.write_register('WDOGRIS', 0x1))
        self.assertFalse(self.device.write_register('WDOGMIS', 0x1))
    
    def test_reserved_bit_handling(self):
        """Test reserved bits are handled correctly"""
        # Unlock device
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
        
        # Write to WDOGCONTROL with reserved bits set
        self.device.write_register('WDOGCONTROL', 0xFFFFFFFF)
        
        # Verify only valid bits are set (bits 4:0)
        control_value = self.device.read_register('WDOGCONTROL')
        self.assertEqual(control_value & 0xFFFFFFE0, 0)  # Reserved bits should be 0


class TestWatchdogPlatformIntegration(unittest.TestCase):
    """Test platform-specific integration features"""
    
    def setUp(self):
        self.device = MockSimicsDevice()
    
    def test_step_value_configuration(self):
        """Test different step values for clock division"""
        # Unlock device
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
        
        # Test different step values
        step_values = [0, 1, 2, 3, 4]
        expected_divisors = [1, 2, 4, 8, 16]
        
        for step_val, expected_div in zip(step_values, expected_divisors):
            control_val = (step_val << 2) | 0x1  # Set step_value and INTEN
            self.device.write_register('WDOGCONTROL', control_val)
            
            # Verify step value is stored correctly
            read_control = self.device.read_register('WDOGCONTROL')
            actual_step = (read_control >> 2) & 0x7
            self.assertEqual(actual_step, step_val)
    
    def test_signal_interface(self):
        """Test signal interface functionality"""
        # Test initial signal states
        self.assertFalse(self.device.get_signal('wdogint'))
        self.assertFalse(self.device.get_signal('wdogreset'))
        
        # Test signal activation through normal operation
        self.device.write_register('WDOGLOCK', 0x1ACCE551)
        self.device.write_register('WDOGCONTROL', 0x3)  # Enable both int and reset
        
        # Simulate timeouts
        self.device.simulate_timeout()  # First timeout
        self.assertTrue(self.device.get_signal('wdogint'))
        
        self.device.simulate_timeout()  # Second timeout
        self.assertTrue(self.device.get_signal('wdogreset'))


def create_test_suite():
    """Create comprehensive test suite"""
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestWatchdogRegisterAccess,
        TestWatchdogSecurity,
        TestWatchdogTimerFunctionality,
        TestWatchdogInterruptSystem,
        TestWatchdogResetEscalation,
        TestWatchdogIntegrationTestMode,
        TestWatchdogErrorConditions,
        TestWatchdogPlatformIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_all_tests():
    """Run complete test suite"""
    print("Simics Watchdog Device Model - Comprehensive Unit Tests")
    print("=" * 60)
    
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
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
    # Run tests
    success = run_all_tests()
    sys.exit(0 if success else 1)