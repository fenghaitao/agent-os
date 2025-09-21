# Device Model Specification Template

## Device Basic Information
- **Device Name**: [DEVICE_NAME]
- **Device Type**: [UART|GPIO|SPI|I2C|PCIe|DDR|Custom]
- **Platform**: [QSP|SPR|GNR|Custom]
- **Interface**: [PCI|AHB|APB|Custom]
- **Register Width**: [8|16|32|64] bits
- **Memory Mapped**: [Yes|No]
- **Interrupt Capable**: [Yes|No]

## Hardware Interface Template

### Register Bank Template
| Offset | Register Name | Width | Access | Reset Value | Description |
|--------|---------------|-------|--------|-------------|-------------|
| 0x00   | CTRL_REG      | 32    | R/W    | 0x00000000  | Control register |
| 0x04   | STATUS_REG    | 32    | RO     | 0x00000000  | Status register |
| 0x08   | DATA_REG      | 32    | R/W    | 0x00000000  | Data register |
| 0x0C   | INT_REG       | 32    | R/W    | 0x00000000  | Interrupt register |

### Register Bit Fields Template
```
CTRL_REG (0x00):
  [31:8]  RESERVED    - Reserved bits
  [7]     INT_EN      - Interrupt enable
  [6:4]   MODE        - Operating mode
  [3:1]   RESERVED    - Reserved bits
  [0]     ENABLE      - Device enable
```

### Memory Mapping Template
```
Base Address: 0x[BASE_ADDR]
Address Space: [SIZE] bytes
Alignment: [ALIGNMENT] byte aligned
Decode Logic: [ADDRESS_DECODE_DESCRIPTION]
```

## Behavioral Specification Template

### Device States
- **IDLE**: Device is idle and ready for operation
- **ACTIVE**: Device is actively processing
- **ERROR**: Device encountered an error condition
- **DISABLED**: Device is disabled

### State Transitions
```
DISABLED --[ENABLE=1]--> IDLE
IDLE --[START_OPERATION]--> ACTIVE  
ACTIVE --[OPERATION_COMPLETE]--> IDLE
ANY_STATE --[ERROR_CONDITION]--> ERROR
ERROR --[RESET]--> DISABLED
```

### Interrupt Specification Template
```
Interrupt Sources:
- DATA_READY: Data is ready for reading
- OPERATION_COMPLETE: Operation has completed
- ERROR_CONDITION: Error has occurred

Interrupt Priority: [HIGH|MEDIUM|LOW]
Interrupt Type: [LEVEL|EDGE]
```

## Implementation Template

### Simics Class Definition
```c
typedef struct {
    // Base device structure
    conf_object_t obj;
    
    // Register bank
    uint32_t ctrl_reg;
    uint32_t status_reg;
    uint32_t data_reg;
    uint32_t int_reg;
    
    // Device state
    device_state_t state;
    
    // Interrupt handling
    bool interrupt_pending;
    conf_object_t *interrupt_target;
    
    // Configuration parameters
    uint64_t base_address;
    bool debug_enabled;
} [device_name]_t;
```

### Register Access Templates
```c
// Read handler template
uint32_t [device_name]_reg_read(conf_object_t *obj, uint32_t offset) {
    [device_name]_t *dev = ([device_name]_t *)obj;
    switch (offset) {
        case 0x00: return dev->ctrl_reg;
        case 0x04: return dev->status_reg;
        case 0x08: return dev->data_reg;
        case 0x0C: return dev->int_reg;
        default: return 0;
    }
}

// Write handler template
void [device_name]_reg_write(conf_object_t *obj, uint32_t offset, uint32_t value) {
    [device_name]_t *dev = ([device_name]_t *)obj;
    switch (offset) {
        case 0x00: 
            dev->ctrl_reg = value;
            [device_name]_update_state(dev);
            break;
        case 0x08: 
            dev->data_reg = value;
            [device_name]_process_data(dev);
            break;
        case 0x0C: 
            dev->int_reg = value;
            [device_name]_update_interrupts(dev);
            break;
    }
}
```

## Testing Template

### Unit Test Categories
- **Register Access Tests**: Verify all register read/write operations
- **State Machine Tests**: Validate state transitions and behaviors
- **Interrupt Tests**: Test interrupt generation and handling
- **Configuration Tests**: Test all configuration parameters
- **Error Condition Tests**: Test error handling and recovery

### Test Case Template
```python
def test_[device_name]_[test_category]():
    # Test setup
    device = create_[device_name]_device()
    
    # Test execution
    result = device.[test_operation]()
    
    # Test validation
    assert result == expected_result
    
    # Cleanup
    destroy_device(device)
```