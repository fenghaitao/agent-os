---
description: Simics Device Specification Creation Rules for Agent OS
globs:
alwaysApply: false
version: 1.0
encoding: UTF-8
---

# Simics Device Specification Rules

## Overview

Generate detailed Simics device model specifications aligned with platform product requirements and technical constraints. This workflow extends agent-os's create-spec process with Simics-specific device modeling requirements.

<pre_flight_check>
  EXECUTE: @.agent-os/simics/device-instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" subagent="context-fetcher" name="platform_context_gathering">

### Step 1: Platform Context Gathering

Use the context-fetcher subagent to gather platform product context and device requirements from the parent platform specification.

<platform_identification>
  <required_parameters>
    - platform_product: QSP|SPR|GNR|Custom
    - device_name: string
    - platform_roadmap_reference: roadmap item or custom requirement
  </required_parameters>
</platform_identification>

<context_sources>
  <primary>
    - @.agent-os/product/mission.md (if platform product exists)
    - @.agent-os/product/roadmap.md (if platform product exists)
    - @.agent-os/product/tech-stack.md (if platform product exists)
  </primary>
  <fallback>
    - User-provided platform context
    - Simics platform standards
  </fallback>
</context_sources>

<platform_requirements_gathering>
  IF platform_product_exists:
    READ platform product documentation
    EXTRACT device requirements from roadmap
    IDENTIFY integration constraints
  ELSE:
    REQUEST platform context from user:
      - Target platform type (QSP/SPR/GNR/Custom)
      - Device integration requirements
      - Platform-specific constraints
</platform_requirements_gathering>

</step>

<step number="2" subagent="context-fetcher" name="device_requirements_clarification">

### Step 2: Device Requirements Clarification

Use the context-fetcher subagent to clarify Simics-specific device requirements and technical specifications.

<device_specification_areas>
  <hardware_interface>
    - interface_type: PCI|AHB|APB|Custom
    - register_width: 8|16|32|64 bits
    - memory_mapped: boolean
    - interrupt_capable: boolean
    - address_space_requirements: size and alignment
  </hardware_interface>
  <behavioral_requirements>
    - functional_accuracy: functional|cycle-accurate|instruction-accurate
    - timing_requirements: event-driven|clock-cycle-accurate
    - state_management: register state, device modes
    - event_handling: interrupt generation, callback mechanisms
  </behavioral_requirements>
  <integration_requirements>
    - platform_dependencies: required platform components
    - configuration_parameters: runtime configuration options
    - debugging_capabilities: register introspection, logging
    - testing_requirements: unit tests, integration tests
  </integration_requirements>
</device_specification_areas>

<clarification_questions>
  Ask numbered questions to clarify:
  1. Hardware interface type and register specifications
  2. Device behavioral requirements and accuracy level
  3. Platform integration and dependency requirements
  4. Testing and validation expectations
</clarification_questions>

</step>

<step number="3" subagent="date-checker" name="date_determination">

### Step 3: Date Determination

Use the date-checker subagent to determine the current date in YYYY-MM-DD format for folder naming.

</step>

<step number="4" subagent="file-creator" name="device_spec_folder_creation">

### Step 4: Device Spec Folder Creation

Use the file-creator subagent to create directory: .agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/ using the date from step 3.

<folder_naming>
  <format>YYYY-MM-DD-simics-device-<device-name></format>
  <device_name_constraints>
    - style: kebab-case
    - max_words: 3
    - descriptive: true
  </device_name_constraints>
</folder_naming>

<example_names>
  - 2025-03-15-simics-device-uart-controller
  - 2025-03-16-simics-device-pcie-bridge
  - 2025-03-17-simics-device-ddr5-controller
</example_names>

</step>

<step number="5" subagent="file-creator" name="create_device_spec_md">

### Step 5: Create Device Specification

Use the file-creator subagent to create the file: .agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/spec.md using this template:

<file_template>
  <header>
    # Simics Device Specification

    > Device: [DEVICE_NAME]
    > Platform: [PLATFORM_PRODUCT]
    > Created: [CURRENT_DATE]
    > Type: Simics Device Model
  </header>
</file_template>

<section name="overview">
  <template>
    ## Overview

    [DEVICE_PURPOSE_AND_FUNCTIONALITY] for [PLATFORM_CONTEXT]. This device model provides [ABSTRACTION_LEVEL] simulation accuracy for [TARGET_USE_CASES].
  </template>
  <constraints>
    - length: 2-3 sentences
    - content: device purpose, platform context, simulation accuracy
  </constraints>
</section>

<section name="hardware_interface">
  <template>
    ## Hardware Interface

    ### Interface Type
    - **Primary Interface:** [PCI|AHB|APB|Custom]
    - **Register Width:** [8|16|32|64] bits
    - **Memory Mapped:** [Yes|No]
    - **Address Space:** [SIZE] bytes, [ALIGNMENT] aligned

    ### Register Bank
    | Offset | Register Name | Width | Access | Description |
    |--------|---------------|-------|--------|-------------|
    | 0x00   | [REG_NAME]    | [WIDTH] | [R/W/RO] | [DESCRIPTION] |

    ### Interrupts
    - **Interrupt Capable:** [Yes|No]
    - **Interrupt Lines:** [NUMBER] ([DESCRIPTION])
    - **Interrupt Conditions:** [CONDITIONS]
  </template>
</section>

<section name="behavioral_specification">
  <template>
    ## Behavioral Specification

    ### Functional Requirements
    1. **[FUNCTION_NAME]** - [DESCRIPTION]
    2. **[FUNCTION_NAME]** - [DESCRIPTION]

    ### State Management
    - **Device States:** [STATE_1], [STATE_2], [STATE_3]
    - **State Transitions:** [TRIGGER] → [STATE_CHANGE]
    - **Reset Behavior:** [RESET_DESCRIPTION]

    ### Timing Requirements
    - **Simulation Accuracy:** [functional|cycle-accurate|instruction-accurate]
    - **Event Handling:** [event-driven|clock-cycle-accurate]
    - **Performance Targets:** [SIMULATION_SPEED_REQUIREMENTS]
  </template>
</section>

<section name="platform_integration">
  <template>
    ## Platform Integration

    ### Platform Requirements
    - **Target Platform:** [QSP|SPR|GNR|Custom]
    - **Dependencies:** [REQUIRED_PLATFORM_COMPONENTS]
    - **Integration Points:** [INTERCONNECT_SPECIFICATIONS]

    ### Configuration Parameters
    - **[PARAM_NAME]:** [TYPE] - [DESCRIPTION] (default: [VALUE])
    - **[PARAM_NAME]:** [TYPE] - [DESCRIPTION] (default: [VALUE])

    ### Device Tree / Configuration
    ```
    [DEVICE_CONFIGURATION_EXAMPLE]
    ```
  </template>
</section>

<section name="validation_criteria">
  <template>
    ## Validation Criteria

    ### Unit Testing
    1. **Register Access Testing** - Verify all register read/write operations
    2. **State Machine Testing** - Validate state transitions and behaviors
    3. **Interrupt Testing** - Test interrupt generation and handling

    ### Integration Testing
    1. **Platform Integration** - Verify device works within target platform
    2. **Performance Testing** - Validate simulation speed and accuracy
    3. **Configuration Testing** - Test all configuration parameter combinations

    ### Acceptance Criteria
    - [ ] All register operations function correctly
    - [ ] Device behavior matches specification
    - [ ] Platform integration successful
    - [ ] Performance targets met
  </template>
</section>

</step>

<step number="6" subagent="file-creator" name="create_device_spec_lite_md">

### Step 6: Create Device Spec Lite

Use the file-creator subagent to create the file: .agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/spec-lite.md

<file_template>
  <header>
    # Simics Device Specification (Lite)
  </header>
</file_template>

<content_template>
  [DEVICE_NAME] device model for [PLATFORM] providing [ABSTRACTION_LEVEL] simulation of [PRIMARY_FUNCTION]. Implements [INTERFACE_TYPE] interface with [REGISTER_COUNT] registers and [FEATURE_SUMMARY].
</content_template>

</step>

<step number="7" subagent="file-creator" name="create_implementation_spec">

### Step 7: Create Implementation Specification

Use the file-creator subagent to create the file: sub-specs/implementation-spec.md

<file_template>
  <header>
    # Simics Device Implementation Specification

    This is the implementation specification for the Simics device detailed in @.agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/spec.md
  </header>
</file_template>

<implementation_sections>
  <simics_api_usage>
    - Required Simics APIs and interfaces
    - Device class definition and inheritance
    - Attribute and interface implementations
    - Event handling and callback registration
  </simics_api_usage>
  <register_implementation>
    - Register bank modeling approach
    - Memory mapping and address decoding
    - Access permission enforcement
    - Side effect implementation
  </register_implementation>
  <state_management>
    - Device state representation
    - State persistence and checkpointing
    - Reset and initialization procedures
    - Configuration parameter handling
  </state_management>
  <performance_considerations>
    - Simulation speed optimization
    - Memory usage optimization
    - Event scheduling efficiency
    - Debug and diagnostic capabilities
  </performance_considerations>
</implementation_sections>

</step>

<step number="8" subagent="file-creator" name="create_testing_spec">

### Step 8: Create Testing Specification

Use the file-creator subagent to create the file: sub-specs/testing-spec.md

<file_template>
  <header>
    # Simics Device Testing Specification

    This is the testing specification for the Simics device detailed in @.agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/spec.md
  </header>
</file_template>

<testing_sections>
  <unit_test_framework>
    - Test harness setup and configuration
    - Mock platform environment creation
    - Test data generation and validation
    - Automated test execution procedures
  </unit_test_framework>
  <test_scenarios>
    - Register access test cases
    - State machine validation tests
    - Interrupt generation and handling tests
    - Configuration parameter tests
    - Error condition and boundary tests
  </test_scenarios>
  <integration_testing>
    - Platform integration test setup
    - Multi-device interaction tests
    - Performance and timing validation
    - Regression testing procedures
  </integration_testing>
  <validation_metrics>
    - Functional correctness criteria
    - Performance benchmarks
    - Code coverage requirements
    - Test automation metrics
  </validation_metrics>
</testing_sections>

</step>

<step number="9" name="user_review">

### Step 9: User Review

Request user review of device specification and all sub-specs files, waiting for approval or revision requests.

<review_request>
  I've created the Simics device specification documentation:

  - Device Specification: @.agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/spec.md
  - Device Spec Summary: @.agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/spec-lite.md
  - Implementation Spec: @.agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/sub-specs/implementation-spec.md
  - Testing Spec: @.agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/sub-specs/testing-spec.md

  Please review and let me know if any changes are needed.

  When you're ready, run the /create-tasks command to have me build the implementation tasks checklist from this device specification.
</review_request>

</step>

</process_flow>

<post_flight_check>
  EXECUTE: @.agent-os/simics/device-instructions/meta/post-flight.md
</post_flight_check>