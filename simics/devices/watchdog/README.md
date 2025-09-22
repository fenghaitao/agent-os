# Simics Watchdog Device Model

A comprehensive ARM SP805-compatible watchdog timer device model for Simics virtual platforms, featuring configurable timeouts, progressive escalation, and multi-platform support.

## Features

- **32-bit Down Counter**: Configurable countdown timer with reload capability
- **Clock Frequency Division**: Support for frequencies from 1 GHz to 62.5 MHz  
- **Progressive Escalation**: Interrupt → Reset escalation on timeout
- **Security Lock**: Hardware write protection mechanism
- **Integration Testing**: Direct signal control for validation
- **Multi-platform Support**: QSP, SPR, GNR platform configurations
- **DML 1.4 Implementation**: Modern Simics device modeling

## Quick Start

### Building the Device

```bash
cd simics/devices/watchdog
make all
```

### Basic Usage

```simics
# Load the watchdog module
load-module watchdog-device

# Create a watchdog instance
new-watchdog-device name = system.watchdog

# Configure for 30-second timeout
system.watchdog.regs.WDOGLOCK = 0x1ACCE551   # Unlock
system.watchdog.regs.WDOGLOAD = 0x1C9C380    # 30 seconds at 1 MHz
system.watchdog.regs.WDOGCONTROL = 0x3       # Enable interrupt and reset
```

### Platform Integration

#### QSP (Embedded)
```simics
run-command-file "platforms/qsp-integration.simics"
```

#### SPR (Server)
```simics
run-command-file "platforms/spr-integration.simics"
```

#### GNR (Next-Gen with Redundancy)
```simics
run-command-file "platforms/gnr-integration.simics"
```

## Register Map

| Offset | Register | Access | Description |
|--------|----------|--------|-------------|
| 0x000 | WDOGLOAD | R/W | Timer reload value |
| 0x004 | WDOGVALUE | RO | Current counter value |
| 0x008 | WDOGCONTROL | R/W | Control register |
| 0x00C | WDOGINTCLR | WO | Interrupt clear |
| 0x010 | WDOGRIS | RO | Raw interrupt status |
| 0x014 | WDOGMIS | RO | Masked interrupt status |
| 0xC00 | WDOGLOCK | R/W | Write access lock |
| 0xF00 | WDOGITCR | R/W | Integration test control |
| 0xF04 | WDOGITOP | WO | Integration test output |

## Clock Configuration

| step_value | Frequency | Use Case |
|------------|-----------|----------|
| 0 | 1 GHz | High-precision servers |
| 1 | 500 MHz | Standard servers |
| 2 | 250 MHz | Embedded systems |
| 3 | 125 MHz | Low-power applications |
| 4 | 62.5 MHz | Very low power |

## Signal Interface

- **wdogint**: Interrupt output signal
- **wdogreset**: Reset output signal

## Testing

### Run Unit Tests
```bash
cd tests
python test_watchdog_unit.py
```

### Run Integration Tests  
```bash
python test_watchdog_integration.py
```

### Run All Tests
```bash
python run_tests.py
```

## Documentation

- [Implementation Guide](docs/implementation-guide.md) - Comprehensive implementation and usage guide
- [Device Specification](../../.agent-os/specs/2025-09-22-simics-device-watchdog/spec.md) - Detailed device specification

## Project Structure

```
watchdog/
├── watchdog.dml              # Main DML implementation
├── Makefile                  # Build configuration
├── README.md                 # This file
├── platforms/                # Platform integration files
│   ├── qsp-integration.simics
│   ├── spr-integration.simics
│   └── gnr-integration.simics
├── tests/                    # Test suite
│   ├── test_watchdog_unit.py
│   ├── test_watchdog_integration.py
│   └── run_tests.py
└── docs/                     # Documentation
    └── implementation-guide.md
```

## Requirements

- Simics 6.0 or later
- DML 1.4 compiler
- Python 3.6+ (for tests)

## License

This implementation follows the project's licensing terms.

## Contributing

Please refer to the project's contribution guidelines and ensure all tests pass before submitting changes.

## Status

✅ Core Implementation Complete  
✅ Register Bank Complete  
✅ Platform Integration Complete  
✅ Test Suite Complete  
✅ Documentation Complete  
⏳ Validation Testing In Progress

---

For detailed implementation information, see the [Implementation Guide](docs/implementation-guide.md).