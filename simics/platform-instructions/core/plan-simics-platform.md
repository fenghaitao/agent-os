---
description: Simics Platform Product Planning Rules for Agent OS
globs:
alwaysApply: false
version: 1.0
encoding: UTF-8
---

# Simics Platform Product Planning Rules

## Overview

Generate comprehensive product documentation for Simics platforms (QSP, SPR, GNR, or custom platforms), treating platforms as products with mission, technical architecture, device portfolio, and development roadmap.

<pre_flight_check>
  EXECUTE: @.agent-os/simics/platform-instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" subagent="context-fetcher" name="platform_type_identification">

### Step 1: Platform Type Identification

Use the context-fetcher subagent to identify the target platform type and gather initial requirements.

<platform_type_selection>
  <predefined_platforms>
    - QSP: Quick Start Platform (Embedded/IoT focus)
    - SPR: Sapphire Rapids Server Platform (Current server validation)
    - GNR: Granite Rapids Server Platform (Next-gen server research)
    - CUSTOM: User-defined custom platform
  </predefined_platforms>
</platform_type_selection>

<platform_context_gathering>
  IF predefined_platform (QSP|SPR|GNR):
    USE platform template and characteristics
    GATHER specific customization requirements
  ELSE IF custom_platform:
    REQUEST complete platform definition:
      - Target system type and use cases
      - Architecture class (embedded/server/specialized)
      - Device portfolio requirements
      - Performance and accuracy targets
</platform_context_gathering>

<platform_templates>
  <qsp_template>
    category: "embedded"
    focus: "Embedded/IoT development"
    complexity: "Low to Medium"
    target_users: ["Embedded developers", "IoT engineers"]
    default_devices: ["UART", "GPIO", "SPI", "I2C", "Timer"]
  </qsp_template>
  <spr_template>
    category: "server"
    focus: "Server/Data center validation"
    complexity: "High"
    target_users: ["System architects", "Server developers"]
    default_devices: ["PCIe Controller", "DDR5 Controller", "CXL Interface", "NUMA Node"]
  </spr_template>
  <gnr_template>
    category: "server"
    focus: "Next-generation server research"
    complexity: "Very High"
    target_users: ["Architecture researchers", "Advanced developers"]
    default_devices: ["AI Accelerator", "Advanced Memory Controller", "Future Interconnect"]
  </gnr_template>
</platform_templates>

</step>

<step number="2" subagent="context-fetcher" name="platform_requirements_clarification">

### Step 2: Platform Requirements Clarification

Use the context-fetcher subagent to clarify platform-specific requirements and technical specifications.

<clarification_areas>
  <platform_scope>
    - target_systems: specific system types to be modeled
    - use_cases: primary development and validation scenarios
    - accuracy_requirements: functional vs cycle-accurate simulation
    - performance_targets: simulation speed and memory footprint
  </platform_scope>
  <device_portfolio>
    - core_devices: essential devices for platform functionality
    - optional_devices: additional devices for extended functionality
    - custom_devices: platform-specific or specialized devices
    - integration_requirements: device interconnection specifications
  </device_portfolio>
  <technical_constraints>
    - simics_version: minimum Simics version requirements
    - host_requirements: development and simulation host requirements
    - integration_points: external tool and framework integration
    - validation_scope: testing and validation requirements
  </technical_constraints>
</clarification_areas>

</step>

<step number="3" subagent="file-creator" name="create_platform_documentation_structure">

### Step 3: Create Platform Documentation Structure

Use the file-creator subagent to create the platform product documentation structure.

<file_structure>
  .agent-os/
  └── platform-products/
      └── [platform-name]/
          ├── mission.md              # Platform product mission and vision
          ├── mission-lite.md         # Condensed mission for AI context
          ├── tech-stack.md          # Platform technical architecture
          ├── roadmap.md             # Development phases and milestones
          └── device-portfolio.md     # Device specifications and requirements
</file_structure>

</step>

<step number="4" subagent="file-creator" name="create_platform_mission_md">

### Step 4: Create Platform Mission

Use the file-creator subagent to create the file: .agent-os/platform-products/[platform-name]/mission.md

<file_template>
  <header>
    # [Platform Name] Platform Product Mission
  </header>
</file_template>

<section name="platform_pitch">
  <template>
    ## Platform Pitch

    [PLATFORM_NAME] is a [PLATFORM_TYPE] virtual platform that enables [TARGET_USERS] to [PRIMARY_VALUE_PROPOSITION] by providing [KEY_CAPABILITIES] for [TARGET_SYSTEMS].
  </template>
  <platform_specific_examples>
    QSP: "QSP is an embedded virtual platform that enables embedded developers to rapidly prototype and validate IoT systems by providing comprehensive peripheral support and industry-standard configurations for embedded computing scenarios."
    SPR: "SPR is a server virtual platform that enables system architects to validate and develop enterprise server solutions by providing high-performance multi-socket simulation and advanced I/O capabilities for data center computing."
    GNR: "GNR is a next-generation server virtual platform that enables architecture researchers to explore and develop future server technologies by providing cutting-edge architectural simulation and emerging technology support for next-generation computing."
  </platform_specific_examples>
</section>

<section name="target_users">
  <template>
    ## Target Users

    ### Primary Users
    - **[USER_TYPE_1]:** [DESCRIPTION_AND_USE_CASES]
    - **[USER_TYPE_2]:** [DESCRIPTION_AND_USE_CASES]

    ### User Scenarios
    **[SCENARIO_NAME]**
    - **User:** [USER_TYPE]
    - **Goal:** [PRIMARY_GOAL]
    - **Context:** [DEVELOPMENT_CONTEXT]
    - **Platform Benefits:** [SPECIFIC_PLATFORM_ADVANTAGES]
  </template>
</section>

<section name="platform_problems">
  <template>
    ## Platform Problems Solved

    ### [PROBLEM_CATEGORY]
    [PROBLEM_DESCRIPTION] affects [TARGET_USERS] by [IMPACT_DESCRIPTION].

    **Platform Solution:** [PLATFORM_SOLUTION_DESCRIPTION]
    **Measurable Impact:** [QUANTIFIABLE_BENEFITS]
  </template>
</section>

<section name="platform_differentiators">
  <template>
    ## Platform Differentiators

    ### [DIFFERENTIATOR_TITLE]
    Unlike [ALTERNATIVE_SOLUTION], [PLATFORM_NAME] provides [SPECIFIC_ADVANTAGE]. This enables [USER_BENEFIT] and results in [MEASURABLE_OUTCOME].
  </template>
</section>

<section name="device_portfolio">
  <template>
    ## Device Portfolio

    ### Core Platform Devices
    - **[DEVICE_NAME]:** [DEVICE_PURPOSE] - [PLATFORM_INTEGRATION_ROLE]

    ### Optional Enhancement Devices  
    - **[DEVICE_NAME]:** [DEVICE_PURPOSE] - [ENHANCED_FUNCTIONALITY]

    ### Platform-Specific Devices
    - **[DEVICE_NAME]:** [SPECIALIZED_FUNCTIONALITY] - [PLATFORM_ADVANTAGE]
  </template>
</section>

</step>

<step number="5" subagent="file-creator" name="create_platform_tech_stack_md">

### Step 5: Create Platform Technical Architecture

Use the file-creator subagent to create the file: .agent-os/platform-products/[platform-name]/tech-stack.md

<file_template>
  <header>
    # [Platform Name] Technical Architecture
  </header>
</file_template>

<technical_architecture_sections>
  <platform_specifications>
    ## Platform Specifications

    ### Simulation Platform
    - **Simics Version:** [VERSION_REQUIREMENT]
    - **Modeling Accuracy:** [functional|cycle-accurate|instruction-accurate]
    - **Performance Targets:** [SIMULATION_SPEED_REQUIREMENTS]
    - **Memory Footprint:** [MEMORY_USAGE_LIMITS]

    ### Architecture Class
    - **Primary Architecture:** [ARM|x86|Custom]
    - **CPU Configuration:** [SINGLE_CORE|MULTI_CORE|MULTI_SOCKET]
    - **Memory Hierarchy:** [MEMORY_SUBSYSTEM_DESCRIPTION]
    - **I/O Subsystem:** [IO_ARCHITECTURE_DESCRIPTION]
  </platform_specifications>

  <device_integration_architecture>
    ## Device Integration Architecture

    ### Interconnect Framework
    - **Primary Bus:** [AHB|APB|PCIe|Custom]
    - **Address Space:** [ADDRESS_SPACE_ORGANIZATION]
    - **Interrupt System:** [INTERRUPT_ARCHITECTURE]
    - **Clock Domains:** [CLOCK_DOMAIN_STRUCTURE]

    ### Device Categories
    - **Core Devices:** [ESSENTIAL_PLATFORM_DEVICES]
    - **Peripheral Devices:** [STANDARD_PERIPHERAL_DEVICES]
    - **Platform-Specific Devices:** [SPECIALIZED_DEVICES]
  </device_integration_architecture>

  <development_environment>
    ## Development Environment

    ### Host Requirements
    - **Operating System:** [SUPPORTED_HOST_OS]
    - **Hardware Requirements:** [CPU_MEMORY_STORAGE_REQUIREMENTS]
    - **Software Dependencies:** [REQUIRED_SOFTWARE_TOOLS]

    ### Integration Points
    - **Development Tools:** [SUPPORTED_DEVELOPMENT_TOOLS]
    - **Testing Frameworks:** [TESTING_AND_VALIDATION_TOOLS]
    - **External Interfaces:** [EXTERNAL_TOOL_INTEGRATION]
  </development_environment>
</technical_architecture_sections>

</step>

<step number="6" subagent="file-creator" name="create_platform_roadmap_md">

### Step 6: Create Platform Development Roadmap

Use the file-creator subagent to create the file: .agent-os/platform-products/[platform-name]/roadmap.md

<roadmap_structure>
  <platform_specific_phases>
    QSP_PHASES: ["Foundation (3 months)", "Enhancement (3 months)", "Extension (3 months)", "Optimization (3 months)"]
    SPR_PHASES: ["Server Foundation (4 months)", "Advanced Features (4 months)", "Enterprise Integration (4 months)", "Validation & Optimization (4 months)"]
    GNR_PHASES: ["Next-Gen Architecture (6 months)", "Advanced Capabilities (6 months)", "Ecosystem Integration (6 months)", "Production Readiness (6 months)"]
    CUSTOM_PHASES: ["Foundation", "Core Features", "Advanced Features", "Integration & Validation"]
  </platform_specific_phases>
</roadmap_structure>

<phase_template>
  ## Phase [NUMBER]: [PHASE_NAME]

  **Duration:** [TIME_ESTIMATE]
  **Goal:** [PHASE_OBJECTIVE]
  **Success Criteria:** [MEASURABLE_COMPLETION_CRITERIA]

  ### Core Deliverables
  - [ ] [DEVICE_NAME] Device Model - [DESCRIPTION] `[EFFORT_ESTIMATE]`
  - [ ] [INTEGRATION_COMPONENT] - [DESCRIPTION] `[EFFORT_ESTIMATE]`

  ### Platform Features
  - [ ] [PLATFORM_FEATURE] - [DESCRIPTION] `[EFFORT_ESTIMATE]`
  - [ ] [VALIDATION_FRAMEWORK] - [DESCRIPTION] `[EFFORT_ESTIMATE]`

  ### Dependencies
  - [DEPENDENCY_DESCRIPTION]
  - [EXTERNAL_REQUIREMENT]

  ### Risks and Mitigation
  - **Risk:** [RISK_DESCRIPTION]
  - **Mitigation:** [MITIGATION_STRATEGY]
</phase_template>

</step>

<step number="7" subagent="file-creator" name="create_device_portfolio_md">

### Step 7: Create Device Portfolio Specification

Use the file-creator subagent to create the file: .agent-os/platform-products/[platform-name]/device-portfolio.md

<device_portfolio_template>
  # [Platform Name] Device Portfolio

  ## Device Architecture Overview

  ### Device Classification
  - **Core Platform Devices:** Essential for basic platform functionality
  - **Standard Peripheral Devices:** Common I/O and communication interfaces
  - **Advanced Feature Devices:** Platform-specific or high-performance components
  - **Optional Extension Devices:** Additional functionality for specialized use cases

  ## Device Specifications

  ### [DEVICE_CATEGORY] Devices

  #### [Device Name]
  - **Purpose:** [DEVICE_FUNCTIONALITY_DESCRIPTION]
  - **Interface Type:** [PCI|AHB|APB|Custom]
  - **Integration Requirements:** [PLATFORM_INTEGRATION_NEEDS]
  - **Implementation Priority:** [High|Medium|Low]
  - **Estimated Effort:** [XS|S|M|L|XL]
  - **Dependencies:** [DEVICE_DEPENDENCIES]
  - **Specification Status:** [To Be Created|In Progress|Complete]

  ## Device Integration Matrix

  | Device | Interface | Address Range | Interrupts | Dependencies | Status |
  |--------|-----------|---------------|------------|--------------|---------|
  | [DEVICE] | [INTERFACE] | [ADDRESS_RANGE] | [IRQ_INFO] | [DEPS] | [STATUS] |

  ## Implementation Roadmap

  ### Phase Allocation
  - **Phase 1:** [CORE_DEVICES_LIST]
  - **Phase 2:** [STANDARD_DEVICES_LIST]  
  - **Phase 3:** [ADVANCED_DEVICES_LIST]
  - **Phase 4:** [OPTIONAL_DEVICES_LIST]
</device_portfolio_template>

</step>

<step number="8" subagent="file-creator" name="create_platform_mission_lite_md">

### Step 8: Create Platform Mission Lite

Use the file-creator subagent to create the file: .agent-os/platform-products/[platform-name]/mission-lite.md

<mission_lite_template>
  # [Platform Name] Platform Mission (Lite)

  [PLATFORM_ELEVATOR_PITCH_FROM_MISSION_MD]

  [1-3_SENTENCES_SUMMARIZING_PLATFORM_VALUE_TARGET_USERS_AND_PRIMARY_DIFFERENTIATOR]
</mission_lite_template>

</step>

<step number="9" name="user_review">

### Step 9: User Review

Request user review of platform product documentation, waiting for approval or revision requests.

<review_request>
  I've created the comprehensive platform product documentation:

  - Platform Mission: @.agent-os/platform-products/[platform-name]/mission.md
  - Platform Mission (Lite): @.agent-os/platform-products/[platform-name]/mission-lite.md
  - Technical Architecture: @.agent-os/platform-products/[platform-name]/tech-stack.md
  - Development Roadmap: @.agent-os/platform-products/[platform-name]/roadmap.md
  - Device Portfolio: @.agent-os/platform-products/[platform-name]/device-portfolio.md

  This establishes [PLATFORM_NAME] as a structured product with clear mission, technical architecture, and development roadmap. Individual device specifications can now be created using the create-simics-device workflow, referencing this platform product context.

  Please review and let me know if any changes are needed.

  Next steps:
  1. Use create-simics-device workflow to specify individual devices from the portfolio
  2. Use create-tasks workflow to generate implementation task lists
  3. Use execute-tasks workflow to implement the platform and devices
</review_request>

</step>

</process_flow>

<post_flight_check>
  EXECUTE: @.agent-os/simics/platform-instructions/meta/post-flight.md
</post_flight_check>