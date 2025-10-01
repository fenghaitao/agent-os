---
description: Create an Agent OS implementation plan (plan.md) for an approved feature spec
globs:
  alwaysApply: false
version: 1.0
encoding: UTF-8
---

# Planning Rules

## Overview

With the user's approval, create an implementation plan (plan.md) for the
current feature spec. This plan captures scope, constraints, dependencies,
risks, and execution considerations that will inform downstream tasks.

<pre_flight_check>
  EXECUTE: @.agent-os/instructions/meta/pre-flight.md
</pre_flight_check>

<process_flow>

<step number="1" name="preconditions_and_clarifications">

### Step 1: Preconditions and Clarifications

Ensure the feature spec exists and that clarifications are captured.

<requirements>
  - APPROVED_SPEC: The feature spec has been created and reviewed
  - CLARIFICATIONS: If significant ambiguities remain (vague adjectives,
    unresolved critical choices), prompt user to run /clarify before planning
</requirements>

<clarification_gate>
  IF clarifications section in spec is missing or empty AND user has not
  explicitly approved proceeding without clarifications:
    - PRESENT: summary of ambiguous areas detected
    - PROMPT: "I recommend running /clarify to reduce rework. Proceed anyway?"
    - IF user says NO: STOP and wait for /clarify
</clarification_gate>

</step>

<step number="2" subagent="file-creator" name="create_plan">

### Step 2: Create plan.md

Use the file-creator subagent to create file: plan.md inside the current
feature's spec folder.

<file_template>
  <header>
    # Implementation Plan
  </header>
</file_template>

<plan_template>
  ## Summary
  - Feature name and intent
  - Key user stories
  - Success and acceptance criteria

  ## Requirements Overview
  - Functional requirements
  - Non-functional requirements (performance, security, reliability)

  ## Technical Context
  - Tech stack and key libraries
  - Constraints and assumptions
  - Architectural approach

  ## Dependencies and Risks
  - Internal and external dependencies
  - Risks and mitigations

  ## Execution Considerations
  - Ordering principles (models before services, services before endpoints)
  - Parallelization guidance [P]
  - Tests-first (TDD) strategy

  ## Reference Inputs (if available)
  - Data model notes (entities)
  - Contracts/API endpoints
  - Quickstart scenarios / test scenarios

  ## Open Questions
  - Outstanding clarifications (link back to spec clarifications)

  ## Next Steps
  - Run /create-tasks to generate tasks.md using this plan
</plan_template>

</step>

<step number="3" name="plan_review">

### Step 3: Plan Review and Next Step

Present a concise plan summary to the user and request confirmation to proceed
with tasks generation.

<review_summary>
  - Plan location: @.agent-os/specs/YYYY-MM-DD-spec-name/plan.md
  - Key decisions and constraints (bullet list)
  - Noted dependencies and parallelization guidance
</review_summary>

<execution_prompt>
  PROMPT: "The implementation plan is ready. Would you like me to proceed with
  /create-tasks to generate tasks.md based on this plan?"
</execution_prompt>

</step>

</process_flow>

<post_flight_check>
  EXECUTE: @.agent-os/instructions/meta/post-flight.md
</post_flight_check>
