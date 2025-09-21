---
description: Simics Device Interface Modeling Rules for Agent OS
globs:
alwaysApply: false
version: 1.0
encoding: UTF-8
---

# Simics Device Interface Modeling Rules

## Overview

Define and implement detailed device interfaces and register banks within platform context, extending existing device specifications with implementation-ready interface definitions.

<pre_flight_check>
  EXECUTE: @.agent-os/simics/device-instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" subagent="context-fetcher" name="existing_spec_analysis">

### Step 1: Existing Specification Analysis

Use the context-fetcher subagent to locate and analyze existing device specification for interface enhancement.

<specification_location>
  FIND: .agent-os/specs/**/spec.md with device name match
  READ: Device specification and current interface definitions
  IDENTIFY: Interface gaps and implementation requirements
</specification_location>

</step>

<step number="2" subagent="context-fetcher" name="interface_requirements_gathering">

### Step 2: Interface Requirements Gathering

Use the context-fetcher subagent to gather detailed interface implementation requirements.

<interface_specification_areas>
  <register_detailed_definition>
    - bit_fields: individual bit definitions and purposes
    - access_behavior: read effects, write side effects, reserved bits
    - reset_values: power-on and reset state definitions
    - register_dependencies: inter-register relationships
  </register_detailed_definition>
  <memory_mapping_details>
    - address_decoding: base address and size requirements
    - alignment_constraints: register and field alignment
    - endianness: byte order specifications
    - access_permissions: read/write/execute permissions
  </memory_mapping_details>
  <interrupt_implementation>
    - interrupt_sources: conditions that trigger interrupts
    - interrupt_masking: enable/disable mechanisms
    - interrupt_status: status and acknowledgment registers
    - interrupt_priorities: priority levels and arbitration
  </interrupt_implementation>
</interface_specification_areas>

</step>

<step number="3" subagent="file-creator" name="create_interface_detail_spec">

### Step 3: Create Detailed Interface Specification

Use the file-creator subagent to create the file: sub-specs/interface-detail-spec.md in the existing device specification folder.

<file_template>
  <header>
    # Detailed Interface Specification

    This extends the device interface specification in @.agent-os/specs/YYYY-MM-DD-simics-device-<device-name>/spec.md with implementation-ready details.
  </header>
</file_template>

<detailed_register_specification>
  ## Register Detailed Definitions

  ### [REGISTER_NAME] (Offset: 0x[OFFSET])

  **Purpose:** [REGISTER_PURPOSE]
  **Width:** [WIDTH] bits
  **Reset Value:** 0x[RESET_VALUE]
  **Access:** [R/W/RO/WO]

  | Bits | Field Name | Access | Reset | Description |
  |------|------------|--------|-------|-------------|
  | [RANGE] | [FIELD_NAME] | [ACCESS] | [VALUE] | [DESCRIPTION] |

  **Access Behavior:**
  - **Read Effects:** [READ_SIDE_EFFECTS]
  - **Write Effects:** [WRITE_SIDE_EFFECTS]
  - **Reserved Bits:** [RESERVED_BIT_BEHAVIOR]

  **Dependencies:**
  - **Affects:** [LIST_OF_AFFECTED_REGISTERS]
  - **Affected By:** [LIST_OF_AFFECTING_REGISTERS]
</detailed_register_specification>

<memory_mapping_specification>
  ## Memory Mapping Implementation

  ### Address Decoding
  - **Base Address:** 0x[BASE_ADDRESS]
  - **Address Space Size:** [SIZE] bytes
  - **Address Alignment:** [ALIGNMENT] byte aligned
  - **Decode Logic:** [ADDRESS_DECODE_DESCRIPTION]

  ### Access Characteristics
  - **Endianness:** [BIG|LITTLE] endian
  - **Supported Access Sizes:** [8|16|32|64] bit access
  - **Unaligned Access:** [SUPPORTED|NOT_SUPPORTED]
  - **Error Handling:** [ERROR_RESPONSE_BEHAVIOR]
</memory_mapping_specification>

<interrupt_detailed_specification>
  ## Interrupt Implementation Details

  ### Interrupt Sources
  | Source | Bit Position | Description | Mask Register | Status Register |
  |--------|--------------|-------------|---------------|-----------------|
  | [SOURCE] | [BIT] | [DESCRIPTION] | [MASK_REG] | [STATUS_REG] |

  ### Interrupt Flow
  1. **Trigger Condition:** [CONDITION_DESCRIPTION]
  2. **Status Update:** [STATUS_REGISTER_UPDATE]
  3. **Mask Check:** [MASK_EVALUATION]
  4. **Signal Generation:** [INTERRUPT_SIGNAL_ASSERTION]
  5. **Acknowledgment:** [ACK_MECHANISM]

  ### Priority and Arbitration
  - **Priority Levels:** [NUMBER] levels ([PRIORITY_SCHEME])
  - **Arbitration Logic:** [ARBITRATION_DESCRIPTION]
  - **Nested Interrupts:** [SUPPORTED|NOT_SUPPORTED]
</interrupt_detailed_specification>

</step>

<step number="4" subagent="file-creator" name="create_register_implementation">

### Step 4: Create Register Implementation Templates

Use the file-creator subagent to create the file: sub-specs/register-implementation.md

<file_template>
  <header>
    # Register Implementation Templates

    Simics-specific implementation templates for device registers and memory mapping.
  </header>
</file_template>

<simics_register_templates>
  ## Simics Register Class Definition

  ```c
  // Register class definition template
  typedef struct {
      uint[WIDTH]_t value;
      uint[WIDTH]_t reset_value;
      uint[WIDTH]_t write_mask;
      uint[WIDTH]_t read_mask;
      // Additional state fields
  } [device_name]_[register_name]_t;
  ```

  ## Register Access Handler Templates

  ```c
  // Read handler template
  uint[WIDTH]_t [device_name]_[register_name]_read(conf_object_t *obj) {
      [device_name]_t *dev = ([device_name]_t *)obj;
      // Read side effects implementation
      return dev->[register_name].value;
  }

  // Write handler template
  void [device_name]_[register_name]_write(conf_object_t *obj, uint[WIDTH]_t value) {
      [device_name]_t *dev = ([device_name]_t *)obj;
      // Write side effects implementation
      dev->[register_name].value = value & dev->[register_name].write_mask;
  }
  ```

  ## Memory Mapping Template

  ```c
  // Memory mapping registration
  static const memory_map_entry_t [device_name]_memory_map[] = {
      { 0x[OFFSET], sizeof(uint[WIDTH]_t), [device_name]_[register_name]_read, [device_name]_[register_name]_write },
      // Additional register mappings
      { 0, 0, NULL, NULL } // Terminator
  };
  ```
</simics_register_templates>

<bit_field_implementation>
  ## Bit Field Access Templates

  ```c
  // Bit field extraction macro
  #define [REGISTER_NAME]_[FIELD_NAME]_GET(reg_val) \
      (((reg_val) >> [SHIFT]) & [MASK])

  // Bit field insertion macro
  #define [REGISTER_NAME]_[FIELD_NAME]_SET(reg_val, field_val) \
      (((reg_val) & ~([MASK] << [SHIFT])) | (((field_val) & [MASK]) << [SHIFT]))

  // Bit field validation macro
  #define [REGISTER_NAME]_[FIELD_NAME]_VALID(field_val) \
      (((field_val) & ~[MASK]) == 0)
  ```
</bit_field_implementation>

</step>

<step number="5" subagent="file-creator" name="create_interrupt_implementation">

### Step 5: Create Interrupt Implementation Templates

Use the file-creator subagent to create the file: sub-specs/interrupt-implementation.md

<interrupt_implementation_templates>
  ## Interrupt State Management

  ```c
  // Interrupt state structure
  typedef struct {
      uint32_t status;        // Interrupt status register
      uint32_t mask;          // Interrupt mask register
      uint32_t pending;       // Pending interrupts (status & ~mask)
      bool interrupt_line;    // Current interrupt line state
  } [device_name]_interrupt_t;
  ```

  ## Interrupt Generation Logic

  ```c
  // Interrupt update function
  void [device_name]_update_interrupts([device_name]_t *dev) {
      dev->interrupt.pending = dev->interrupt.status & ~dev->interrupt.mask;
      bool new_interrupt_state = (dev->interrupt.pending != 0);
      
      if (new_interrupt_state != dev->interrupt.interrupt_line) {
          dev->interrupt.interrupt_line = new_interrupt_state;
          // Signal interrupt to platform
          if (new_interrupt_state) {
              SIM_signal_raise(dev->interrupt_signal);
          } else {
              SIM_signal_lower(dev->interrupt_signal);
          }
      }
  }
  ```

  ## Interrupt Handler Templates

  ```c
  // Interrupt status register write handler
  void [device_name]_interrupt_status_write(conf_object_t *obj, uint32_t value) {
      [device_name]_t *dev = ([device_name]_t *)obj;
      // Clear-on-write behavior for status bits
      dev->interrupt.status &= ~value;
      [device_name]_update_interrupts(dev);
  }

  // Interrupt mask register write handler
  void [device_name]_interrupt_mask_write(conf_object_t *obj, uint32_t value) {
      [device_name]_t *dev = ([device_name]_t *)obj;
      dev->interrupt.mask = value;
      [device_name]_update_interrupts(dev);
  }
  ```
</interrupt_implementation_templates>

</step>

<step number="6" name="user_review">

### Step 6: User Review

Request user review of interface implementation specifications.

<review_request>
  I've created detailed interface implementation specifications:

  - Detailed Interface Spec: sub-specs/interface-detail-spec.md
  - Register Implementation: sub-specs/register-implementation.md
  - Interrupt Implementation: sub-specs/interrupt-implementation.md

  These extend the existing device specification with implementation-ready details including:
  - Detailed register bit field definitions
  - Memory mapping and access behavior
  - Interrupt generation and handling logic
  - Simics-specific implementation templates

  Please review and let me know if any changes are needed before proceeding with implementation tasks.
</review_request>

</step>

</process_flow>

<post_flight_check>
  EXECUTE: @.agent-os/simics/device-instructions/meta/post-flight.md
</post_flight_check>