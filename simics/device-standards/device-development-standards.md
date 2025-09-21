# Simics Device Development Standards

## Code Organization Standards

### File Structure
- Device model source files: `src/devices/[device-name]/`
- Register definitions: `src/devices/[device-name]/registers.h`
- Implementation: `src/devices/[device-name]/[device-name].c`
- Tests: `tests/devices/[device-name]/`

### Naming Conventions
- Device class names: `[vendor]_[device]_device`
- Register names: `[DEVICE]_[REGISTER]_REG`
- Bit field names: `[REGISTER]_[FIELD]_MASK`
- Function names: `[device]_[operation]`

## Implementation Standards

### Register Modeling
- Use structured register definitions
- Implement proper access permissions
- Handle side effects correctly
- Provide reset value definitions

### State Management
- Implement proper device state tracking
- Support checkpointing and restoration
- Handle configuration parameters
- Maintain device lifecycle properly

### Error Handling
- Validate all input parameters
- Provide meaningful error messages
- Handle edge cases gracefully
- Log important events appropriately

## Documentation Standards

### Code Documentation
- Document all public interfaces
- Explain complex algorithms
- Provide usage examples
- Document configuration options

### Specification Alignment
- Maintain traceability to specifications
- Document implementation decisions
- Explain accuracy trade-offs
- Provide validation evidence