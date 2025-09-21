---
description: Simics Platform Assembly Rules for Agent OS
version: 1.0
---

# Platform Assembly Rules

## Overview
Assemble device specifications into complete platform implementation based on product roadmap.

<process_flow>

<step number="1" name="platform_analysis">
### Step 1: Platform Product Analysis
- Read platform product documentation
- Identify current roadmap phase deliverables  
- Assess device specification readiness
- Determine integration requirements

</step>

<step number="2" name="device_inventory">
### Step 2: Device Specification Inventory
- Scan available device specifications
- Filter specifications matching platform
- Assess completeness and integration readiness
- Prioritize based on roadmap phase

</step>

<step number="3" name="assembly_specification">
### Step 3: Create Platform Assembly Spec
Create: platform-assembly-spec.md with:
- Device integration plan and dependencies
- System architecture (memory map, interrupts, clocks)
- Configuration generation requirements
- Integration testing framework

</step>

<step number="4" name="configuration_generation">
### Step 4: Generate Platform Configuration
Create platform configuration scripts:
- Main platform configuration file
- Device configuration templates
- Memory mapping setup
- Interrupt routing configuration

</step>

<step number="5" name="integration_testing">
### Step 5: Create Integration Test Framework
- Device communication tests
- Interrupt system validation
- Platform performance tests
- Functional validation scenarios

</step>

<step number="6" name="assembly_execution">
### Step 6: Assembly Execution Coordination
Execute in dependency order:
1. Validate specifications
2. Generate configurations
3. Setup device integration
4. Execute integration tests
5. Validate platform functionality

</step>

</process_flow>