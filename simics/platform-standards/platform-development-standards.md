# Simics Platform Development Standards

## Platform Architecture Standards

### Platform Organization
- Platform products: `.agent-os/platform-products/[platform-name]/`
- Assembly artifacts: `assembly/` subdirectory
- Configuration scripts: `assembly/platform-config.simics`
- Device configurations: `assembly/device-configs/`

### Platform Naming
- Platform names: kebab-case (qsp-platform, spr-server-platform)
- Configuration files: `[platform-name]-config.simics`
- Device instances: `[platform]_[device]_[instance]`

## Development Phase Standards

### Phase Definitions
- Foundation: Core platform and essential devices
- Enhancement: Standard peripherals and features
- Advanced: Platform-specific and high-performance components
- Optimization: Performance tuning and validation

### Deliverable Standards
- Each phase has clear success criteria
- Deliverables are measurable and testable
- Dependencies are explicitly documented
- Risk mitigation strategies are defined

## Integration Standards

### Device Integration
- Consistent memory mapping schemes
- Standardized interrupt allocation
- Unified configuration parameters
- Common debugging interfaces

### Configuration Management
- Version controlled configurations
- Parameterized platform templates
- Automated configuration validation
- Documentation of configuration changes

## Quality Assurance

### Testing Requirements
- Unit tests for individual devices
- Integration tests for device interactions
- System tests for complete platform scenarios
- Performance benchmarks for simulation metrics

### Documentation Standards
- Platform mission and architecture documented
- Device integration specifications maintained
- Configuration procedures documented
- Troubleshooting guides provided