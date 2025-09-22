# Simics Watchdog Device Model Specification

> Device: Watchdog Timer (WDT)
> Platform: Multi-platform (QSP/SPR/GNR/Custom)
> Created: 2025-09-22
> Type: Simics Device Model

## Overview

A configurable 32-bit down-counter watchdog device with interrupt and reset capabilities for system monitoring and failsafe operations in virtual platforms. This device model provides progressive escalation from interrupt notification to system reset, ensuring system reliability in embedded and server virtual platforms.

## Device Basic Information
- **Device Name**: Watchdog Timer (WDT) 
- **Device Type**: System Timer/Watchdog
- **Platform**: Multi-platform (QSP/SPR/GNR/Custom)
- **Interface**: APB (Advanced Peripheral Bus)
- **Register Width**: 32 bits
- **Memory Mapped**: Yes
- **Interrupt Capable**: Yes

## Hardware Interface

### Interface Type
- **Primary Interface**: APB (Advanced Peripheral Bus)
- **Register Width**: 32 bits
- **Memory Mapped**: Yes
- **Address Space**: 4KB bytes, 4-byte aligned

### Register Bank
| Offset | Register Name | Width | Access | Reset Value | Description |
|--------|---------------|-------|--------|-------------|-------------|
| 0x000  | WDOGLOAD     | 32    | R/W    | 0xFFFFFFFF  | Timer reload value |
| 0x004  | WDOGVALUE    | 32    | RO     | 0xFFFFFFFF  | Current counter value |
| 0x008  | WDOGCONTROL  | 32    | R/W    | 0x00000000  | Control register |
| 0x00C  | WDOGINTCLR   | 32    | WO     | 0x00000000  | Interrupt clear |
| 0x010  | WDOGRIS      | 32    | RO     | 0x00000000  | Raw interrupt status |
| 0x014  | WDOGMIS      | 32    | RO     | 0x00000000  | Masked interrupt status |
| 0xC00  | WDOGLOCK     | 32    | R/W    | 0x00000000  | Write access lock |
| 0xF00  | WDOGITCR     | 32    | R/W    | 0x00000000  | Integration test control |
| 0xF04  | WDOGITOP     | 32    | WO     | 0x00000000  | Integration test output |
| 0xFD0-0xFEC | PeripheralID0-3, PCellID0-3 | 32 | RO | Fixed | Device identification |
| 0xFF0-0xFFC | PrimeCellID0-3 | 32 | RO | Fixed | Component identification |

### Interrupts
- **Interrupt Capable**: Yes
- **Interrupt Lines**: 1 (`wdogint` signal)
- **Interrupt Conditions**: Counter reaches zero with INTEN=1

### Reset Lines
- **Reset Capable**: Yes
- **Reset Lines**: 1 (`wdogreset` signal)
- **Reset Conditions**: Second counter timeout with RESEN=1

## Behavioral Specification

### Functional Requirements
1. **32-bit Down Counter** - Configurable countdown timer from WDOGLOAD value
2. **Clock Frequency Division** - Configurable step_value for different operating frequencies
3. **Interrupt Generation** - Level-triggered interrupt on first timeout
4. **Reset Escalation** - System reset on second timeout if enabled
5. **Security Lock** - Write protection mechanism for critical registers
6. **Integration Testing** - Direct signal control for validation

### Device States
- **DISABLED**: Device is disabled, counter stopped
- **UNLOCKED**: Device unlocked for configuration
- **CONFIGURED**: Device configured but not running
- **RUNNING**: Counter actively counting down
- **INTERRUPT_PENDING**: First timeout occurred, interrupt asserted
- **RESET_PENDING**: Second timeout occurred, reset asserted
- **TEST_MODE**: Integration test mode active

### State Transitions
```
DISABLED --[WDOGLOCK=0x1ACCE551]--> UNLOCKED
UNLOCKED --[Configure WDOGCONTROL]--> CONFIGURED  
CONFIGURED --[INTEN=1]--> RUNNING
RUNNING --[Counter=0 & INTEN=1]--> INTERRUPT_PENDING
INTERRUPT_PENDING --[WDOGINTCLR write]--> RUNNING
INTERRUPT_PENDING --[Counter=0 again & RESEN=1]--> RESET_PENDING
RESET_PENDING --[System Reset]--> DISABLED
ANY_STATE --[WDOGITCR=1]--> TEST_MODE
TEST_MODE --[WDOGITCR=0]--> Previous State
```

### Timing Requirements
- **Simulation Accuracy**: Functional level with cycle-accurate timing
- **Event Handling**: Event-driven with precise timeout detection
- **Performance Targets**: Minimal simulation overhead

## Platform Integration

### Platform Requirements
- **Target Platform**: QSP/SPR/GNR/Custom platforms
- **Dependencies**: APB bus interface, interrupt controller, reset controller
- **Integration Points**: System clock domain, interrupt routing, reset management

### Configuration Parameters
- **sys_mhz**: integer - System frequency in MHz for clock translation (default: 1000)
- **base_address**: uint64 - Device base address in memory map (default: 0x0)
- **debug_enabled**: boolean - Enable debug output and logging (default: false)

### Device Tree Configuration
```
watchdog@40000000 {
    compatible = "arm,sp805-wdt";
    reg = <0x40000000 0x1000>;
    interrupts = <0 32 4>;
    clocks = <&wdogclk>;
    clock-names = "wdogclk";
};
```

## Register Detailed Specifications

### WDOGLOAD Register (0x000)
**Purpose**: Timer reload value configuration
**Width**: 32 bits
**Reset Value**: 0xFFFFFFFF
**Access**: R/W

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:0 | wdog_load | R/W | 0xFFFFFFFF | Timer reload value in watchdog cycles |

### WDOGVALUE Register (0x004)  
**Purpose**: Current counter value readback
**Width**: 32 bits
**Reset Value**: 0xFFFFFFFF
**Access**: RO

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:0 | count_read | RO | 0xFFFFFFFF | Current counter value (read-only) |

### WDOGCONTROL Register (0x008)
**Purpose**: Timer control and configuration
**Width**: 32 bits
**Reset Value**: 0x00000000
**Access**: R/W

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:5 | Reserved | - | - | Reserved bits |
| 4:2 | step_value | R/W | 3'b000 | Clock division configuration |
| 1 | RESEN | R/W | 1'b0 | Reset enable on second timeout |
| 0 | INTEN | R/W | 1'b0 | Interrupt enable and counter start |

### WDOGINTCLR Register (0x00C)
**Purpose**: Interrupt acknowledgment and counter reload
**Width**: 32 bits
**Reset Value**: 0x00000000
**Access**: WO

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:0 | intclr | WO | 0x00 | Write any value to clear interrupt |

### WDOGRIS Register (0x010)
**Purpose**: Raw interrupt status
**Width**: 32 bits
**Reset Value**: 0x00000000
**Access**: RO

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:1 | Reserved | - | - | Reserved |
| 0 | raw_interrupt | RO | 1'b0 | Raw interrupt status |

### WDOGMIS Register (0x014)
**Purpose**: Masked interrupt status
**Width**: 32 bits
**Reset Value**: 0x00000000
**Access**: RO

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:1 | Reserved | - | - | Reserved |
| 0 | masked_interrupt | RO | 1'b0 | Masked interrupt status (WDOGRIS & INTEN) |

### WDOGLOCK Register (0xC00)
**Purpose**: Security write protection
**Width**: 32 bits
**Reset Value**: 0x00000000
**Access**: R/W

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:0 | wdog_lock | R/W | 0x00000000 | Write 0x1ACCE551 to unlock, others to lock |

### WDOGITCR Register (0xF00)
**Purpose**: Integration test mode control
**Width**: 32 bits
**Reset Value**: 0x00000000
**Access**: R/W

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:1 | Reserved | - | - | Reserved |
| 0 | test_enable | R/W | 1'b0 | Integration test mode enable |

### WDOGITOP Register (0xF04)
**Purpose**: Integration test signal output control
**Width**: 32 bits
**Reset Value**: 0x00000000
**Access**: WO

| Bits | Field Name | Access | Reset | Description |
|------|------------|--------|-------|-------------|
| 31:2 | Reserved | - | - | Reserved |
| 1 | test_wdogint | WO | 1'b0 | Direct interrupt control in test mode |
| 0 | test_wdogres | WO | 1'b0 | Direct reset control in test mode |

## Clock Domain and Frequency Configuration

### Step Value Configuration
| step_value | Division Factor | Target Frequency | Use Case |
|------------|----------------|------------------|----------|
| 3'b000 | 1 | 1 GHz | High-precision timing |
| 3'b001 | 2 | 500 MHz | Standard server applications |
| 3'b010 | 4 | 250 MHz | Embedded systems |
| 3'b011 | 8 | 125 MHz | Low-power applications |
| 3'b100 | 16 | 62.5 MHz | Very low power modes |

## Validation Criteria

### Functional Validation
- [ ] All register read/write operations work correctly
- [ ] Counter countdown operates at correct frequency
- [ ] Interrupt generation occurs on first timeout
- [ ] Reset generation occurs on second timeout with RESEN=1
- [ ] Lock mechanism protects registers correctly
- [ ] Integration test mode provides direct signal control

### Performance Validation
- [ ] Simulation performance within acceptable limits
- [ ] Clock domain translation accurate
- [ ] Timing precision meets requirements

### Platform Integration Validation
- [ ] APB bus interface compliance
- [ ] Interrupt controller integration
- [ ] Reset controller integration
- [ ] Multi-platform compatibility

### Security Validation
- [ ] Lock protection prevents unauthorized access
- [ ] Unlock sequence works correctly
- [ ] Reserved bits behave properly

## Implementation Notes

### DML 1.4 Requirements
- Device must be implemented using DML 1.4 syntax
- Register banks using `bank` construct
- Clock domains using `clock` construct
- Signal interfaces using `signal` construct
- Event handling using `event` construct

### Signal Interface Requirements
- `wdogint` signal for interrupt output
- `wdogreset` signal for reset output
- APB bus signals for register access
- Clock input signal for timing reference

### Reset Handling Requirements
- Multiple reset domains (WRESET, PRESET, WDOGRESET)
- Proper reset value initialization
- Reset propagation to external systems

This specification provides the foundation for implementing a comprehensive Simics watchdog device model that meets the requirements outlined in the strategic design document.