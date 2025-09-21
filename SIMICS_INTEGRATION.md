# Simics Integration for Agent-OS

## Overview

The Simics integration extends agent-os with specialized workflows for virtual platform development, device modeling, and simulation within the Simics ecosystem. This integration treats Simics platforms as products and individual device modules as specifications, leveraging agent-os's established workflow patterns.

## Platform as Product Model

### Supported Platform Products

- **QSP Platform Product**: Quick Start Platform for embedded/IoT development
- **SPR Server Platform Product**: Sapphire Rapids server platform for data center validation  
- **GNR Server Platform Product**: Granite Rapids server platform for next-gen server research
- **Custom Platform Products**: User-defined platforms for specialized requirements

### Platform Product Workflow

1. **Plan Platform Product**: Use `plan-simics-platform` to establish platform mission, roadmap, and device portfolio
2. **Analyze Platform**: Use `analyze-simics-platform` to assess existing platforms for integration
3. **Create Device Specifications**: Use `create-simics-device` to specify individual device models
4. **Assemble Platform**: Use `assemble-platform` to integrate devices into complete platform
5. **Validate Platform**: Use `validate-platform` to execute comprehensive platform validation

## Device Specifications

### Device Development Workflow

Device modules are treated as specifications within agent-os, following enhanced create-spec patterns:

```bash
# Create a device specification for a specific platform
agent-os create-simics-device --platform=qsp --device-name=uart-controller

# Model detailed device interfaces  
agent-os model-device-interface --spec=uart-controller

# Create implementation tasks
agent-os create-tasks --spec=uart-controller

# Execute device implementation
agent-os execute-tasks --spec=uart-controller
```

### Device Types by Platform

| Platform | Device Examples | Complexity | Integration |
|----------|----------------|------------|-------------|
| **QSP** | UART, GPIO, SPI, I2C, Timer | Low-Medium | Standard peripheral bus |
| **SPR** | PCIe Controller, DDR5 Controller, CXL Interface | High | Server topology integration |
| **GNR** | AI Accelerator, Advanced Memory Controller | Very High | Next-gen architecture |

## Project Types

The integration introduces three specialized project types:

### simics-device
For individual device model development with register modeling and behavioral simulation.

### simics-platform  
For virtual platform assembly, system-level configuration, and multi-device integration.

### simics-simulation
For simulation environment setup, test scenario development, and automated testing.

## Configuration

The Simics integration extends agent-os configuration in `config.yml`:

```yaml
# Simics project types
project_types:
  simics-device:
    instructions: ~/.agent-os/simics/device-instructions  
    standards: ~/.agent-os/simics/device-standards
    
  simics-platform:
    instructions: ~/.agent-os/simics/platform-instructions
    standards: ~/.agent-os/simics/platform-standards
    
  simics-simulation:
    instructions: ~/.agent-os/simics/simulation-instructions
    standards: ~/.agent-os/simics/simulation-standards

# Simics-specific configuration
simics:
  version: "6.0+"
  api_version: "latest"
  default_accuracy: "functional"
  enable_debugging: true
  performance_monitoring: true
```

## Usage Examples

### Create QSP Platform Product

```bash
# Plan QSP platform as a product
agent-os plan-product --project-type=simics-platform --platform-name=qsp

# This creates:
# .agent-os/platform-products/qsp/mission.md
# .agent-os/platform-products/qsp/roadmap.md  
# .agent-os/platform-products/qsp/tech-stack.md
# .agent-os/platform-products/qsp/device-portfolio.md
```

### Create Device for Platform

```bash
# Create UART device specification for QSP platform
agent-os create-spec --project-type=simics-device --platform=qsp --device-name=uart-controller

# This creates:
# .agent-os/specs/YYYY-MM-DD-simics-device-uart-controller/spec.md
# .agent-os/specs/YYYY-MM-DD-simics-device-uart-controller/sub-specs/implementation-spec.md
# .agent-os/specs/YYYY-MM-DD-simics-device-uart-controller/sub-specs/testing-spec.md
```

### Assemble Complete Platform

```bash
# Assemble devices into complete platform
agent-os assemble-platform --product=qsp --phase=foundation

# Validate assembled platform
agent-os validate-platform --product=qsp
```

## Integration Benefits

- **Structured Development**: Platform products provide clear mission and roadmap
- **Specification-Driven**: Device models follow detailed specification requirements
- **Consistent Standards**: Unified development standards across all Simics projects
- **Automated Workflows**: Agent-os automation for specification, tasks, and execution
- **Quality Assurance**: Built-in testing and validation frameworks
- **Documentation**: Comprehensive documentation generation and maintenance

## Next Steps

1. Choose target platform product (QSP/SPR/GNR/Custom)
2. Use `plan-simics-platform` to establish platform foundation
3. Create device specifications with `create-simics-device`
4. Generate implementation tasks with `create-tasks`
5. Execute development with `execute-tasks`
6. Assemble and validate complete platform