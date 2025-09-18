---
description: Create an Agent OS tasks list from an approved feature spec
globs:
alwaysApply: false
version: 1.1
encoding: UTF-8
---

# Spec Creation Rules

## Overview

With the user's approval, proceed to creating a tasks list based on the current feature spec.

<pre_flight_check>
  EXECUTE: @.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" subagent="file-creator" name="create_tasks">

### Step 1: Create tasks.md

Use the file-creator subagent to create file: tasks.md inside of the current feature's spec folder.

<simics_device_detection>
IF simics_device_model_detected:
  USE: simics_device_task_structure
ELSE:
  USE: standard_task_structure
</simics_device_detection>

<simics_device_task_structure>
  <header>
    # Device Model Implementation Tasks
  </header>

  <simics_task_types>
    <device_modeling_tasks>
      - register_implementation: Define and implement all device registers
      - signal_connection_implementation: Implement ports and interface connections
      - state_machine_implementation: Implement device state logic and transitions
      - event_timer_implementation: Implement events, timers, and interrupt handling
      - dml_compilation: Compile DML source to .so module
      - unit_testing: Create and run device model unit tests
    </device_modeling_tasks>
  </simics_task_types>

  <simics_task_template>
    ## Tasks

    - [ ] 1. **Device Register Implementation**
      - [ ] 1.1 Create DML device structure and register bank definitions
      - [ ] 1.2 Implement register read/write methods with side effects
      - [ ] 1.3 Add register reset values and access control
      - [ ] 1.4 Verify register behavior against hardware specification

    - [ ] 2. **Signal and Connection Implementation**
      - [ ] 2.1 Define input/output ports for external signals
      - [ ] 2.2 Implement interface connections (memory, interrupt, etc.)
      - [ ] 2.3 Add signal handling and protocol implementation
      - [ ] 2.4 Test signal and connection functionality

    - [ ] 3. **State Machine and Event Implementation**
      - [ ] 3.1 Implement device state variables and transitions
      - [ ] 3.2 Add event handlers for timers and asynchronous operations
      - [ ] 3.3 Implement interrupt generation and handling
      - [ ] 3.4 Verify state machine behavior and event timing

    - [ ] 4. **DML Compilation and Build**
      - [ ] 4.1 Set up DML build environment and dependencies
      - [ ] 4.2 Compile DML source code to .so module
      - [ ] 4.3 Resolve compilation errors and warnings
      - [ ] 4.4 Verify successful module loading in Simics

    - [ ] 5. **Device Model Unit Testing**
      - [ ] 5.1 Create unit test framework for device model
      - [ ] 5.2 Write tests for register operations and side effects
      - [ ] 5.3 Write tests for signal/connection behavior
      - [ ] 5.4 Write tests for state machine and event handling
      - [ ] 5.5 Run all tests and verify 100% pass rate
  </simics_task_template>
</simics_device_task_structure>

<standard_task_structure>
<file_template>
  <header>
    # Spec Tasks
  </header>
</file_template>

<task_structure>
  <major_tasks>
    - count: 1-5
    - format: numbered checklist
    - grouping: by feature or component
  </major_tasks>
  <subtasks>
    - count: up to 8 per major task
    - format: decimal notation (1.1, 1.2)
    - first_subtask: typically write tests
    - last_subtask: verify all tests pass
  </subtasks>
</task_structure>

<task_template>
  ## Tasks

  - [ ] 1. [MAJOR_TASK_DESCRIPTION]
    - [ ] 1.1 Write tests for [COMPONENT]
    - [ ] 1.2 [IMPLEMENTATION_STEP]
    - [ ] 1.3 [IMPLEMENTATION_STEP]
    - [ ] 1.4 Verify all tests pass

  - [ ] 2. [MAJOR_TASK_DESCRIPTION]
    - [ ] 2.1 Write tests for [COMPONENT]
    - [ ] 2.2 [IMPLEMENTATION_STEP]
</task_template>
</standard_task_structure>

<ordering_principles>
  <simics_ordering>
    - Start with register definitions (foundation)
    - Add signal/connection infrastructure
    - Implement state machine and events
    - Build and compile DML code
    - Test complete device functionality
  </simics_ordering>
  <standard_ordering>
    - Consider technical dependencies
    - Follow TDD approach
    - Group related functionality
    - Build incrementally
  </standard_ordering>
</ordering_principles>

</step>

<step number="2" name="execution_readiness">

### Step 2: Execution Readiness Check

Evaluate readiness to begin implementation by presenting the first task summary and requesting user confirmation to proceed.

<readiness_summary>
  <present_to_user>
    - Spec name and description
    - First task summary from tasks.md
    - Estimated complexity/scope
    - Key deliverables for task 1
  </present_to_user>
</readiness_summary>

<execution_prompt>
  PROMPT: "The spec planning is complete. The first task is:

  **Task 1:** [FIRST_TASK_TITLE]
  [BRIEF_DESCRIPTION_OF_TASK_1_AND_SUBTASKS]

  Would you like me to proceed with implementing Task 1? I will focus only on this first task and its subtasks unless you specify otherwise.

  Type 'yes' to proceed with Task 1, or let me know if you'd like to review or modify the plan first."
</execution_prompt>

<execution_flow>
  IF user_confirms_yes:
    REFERENCE: @.agent-os/instructions/core/execute-tasks.md
    FOCUS: Only Task 1 and its subtasks
    CONSTRAINT: Do not proceed to additional tasks without explicit user request
  ELSE:
    WAIT: For user clarification or modifications
</execution_flow>

</step>

</process_flow>

<post_flight_check>
  EXECUTE: @.agent-os/instructions/meta/post-flight.md
</post_flight_check>
