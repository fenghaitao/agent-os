# Claude Code Integration

<cite>
**Referenced Files in This Document**   
- [context-fetcher.md](file://claude-code/agents/context-fetcher.md)
- [date-checker.md](file://claude-code/agents/date-checker.md)
- [file-creator.md](file://claude-code/agents/file-creator.md)
- [git-workflow.md](file://claude-code/agents/git-workflow.md)
- [project-manager.md](file://claude-code/agents/project-manager.md)
- [test-runner.md](file://claude-code/agents/test-runner.md)
- [installer.py](file://src/installer.py)
- [cli.py](file://src/cli.py)
- [execute-tasks.md](file://commands/execute-tasks.md)
- [execute-tasks.md](file://instructions/core/execute-tasks.md)
- [execute-task.md](file://instructions/core/execute-task.md)
- [post-execution-tasks.md](file://instructions/core/post-execution-tasks.md)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Agent OS Architecture Overview](#agent-os-architecture-overview)
3. [Claude Code Agent System](#claude-code-agent-system)
4. [Core Agent Analysis](#core-agent-analysis)
5. [Agent Integration and Installation](#agent-integration-and-installation)
6. [Workflow Orchestration](#workflow-orchestration)
7. [CLI Command Invocation](#cli-command-invocation)
8. [Common Issues and Solutions](#common-issues-and-solutions)
9. [Performance Considerations](#performance-considerations)
10. [Conclusion](#conclusion)

## Introduction

Agent OS provides a structured framework for AI-assisted software development, with Claude Code integration at its core. The system leverages specialized Markdown templates that define agent behavior, responsibilities, and interaction patterns to transform AI coding assistants from general-purpose tools into focused development partners. This document details how Agent OS orchestrates Claude Code agents through a sophisticated system of templates, workflows, and installation processes that enable consistent, high-quality code generation aligned with project standards and requirements.

The integration centers on six specialized agents—context-fetcher, date-checker, file-creator, git-workflow, project-manager, and test-runner—each designed with specific capabilities and constraints to handle distinct aspects of the development workflow. These agents operate within a larger ecosystem of instructions, standards, and CLI tools that coordinate their activities and ensure cohesive operation across the development lifecycle.

**Section sources**
- [README.md](file://README.md#L1-L33)
- [INSTALL.md](file://INSTALL.md#L1-L20)

## Agent OS Architecture Overview

Agent OS implements a modular architecture that separates concerns across different components and platforms. The system is designed to integrate seamlessly with various AI coding platforms while maintaining a consistent interface and workflow pattern. At its core, Agent OS provides standardized development workflows that can be adapted to different AI assistants through platform-specific templates and configurations.

The architecture consists of several key layers:
- **Core System**: Contains instructions, standards, and configuration files that define the development process
- **Platform Integrations**: Platform-specific templates for Claude Code, Cursor, GitHub Copilot, Qwen Code, and ADK
- **Agents**: Specialized Markdown templates that define focused AI behaviors for specific tasks
- **Commands**: High-level workflow definitions that orchestrate agent activities
- **Installation System**: Python-based and shell-based installers that deploy the system to projects

This layered approach allows Agent OS to maintain consistent development practices across different AI coding platforms while providing the flexibility to leverage platform-specific features and interfaces.

```mermaid
graph TB
subgraph "Core System"
Instructions[.agent-os/instructions/]
Standards[.agent-os/standards/]
Config[.agent-os/config.yml]
end
subgraph "Platform Integrations"
Claude[.claude/agents/]
Cursor[.cursor/rules/]
Copilot[.github/prompts/]
Qwen[.qwen/commands/]
ADK[.adk/agents/]
end
subgraph "Agents"
CF[context-fetcher]
DC[date-checker]
FC[file-creator]
GW[git-workflow]
PM[project-manager]
TR[test-runner]
end
subgraph "Installation"
CLI[agent-os CLI]
Installer[installer.py]
end
Instructions --> |Provides| Claude
Instructions --> |Provides| Cursor
Instructions --> |Provides| Copilot
Instructions --> |Provides| Qwen
Instructions --> |Provides| ADK
Standards --> |Provides| Claude
Standards --> |Provides| Cursor
Standards --> |Provides| Copilot
Standards --> |Provides| Qwen
Standards --> |Provides| ADK
Config --> |Configures| CLI
CLI --> |Installs| Project
Installer --> |Deploys| Project
class CF,DC,FC,GW,PM,TR clickable
```

**Diagram sources**
- [INSTALL.md](file://INSTALL.md#L50-L100)
- [ADK_INTEGRATION_SUMMARY.md](file://ADK_INTEGRATION_SUMMARY.md#L1-L20)

## Claude Code Agent System

The Claude Code agent system in Agent OS consists of six specialized agents, each defined by a Markdown template that specifies its name, description, tools, color, and detailed behavioral instructions. These agents are designed to work together in a coordinated fashion, with each focusing on a specific aspect of the development workflow while adhering to strict constraints that prevent role overlap and ensure predictable behavior.

The agent templates follow a consistent structure with YAML frontmatter defining metadata and a Markdown body containing detailed instructions. This structure allows for easy configuration and extension while maintaining readability and maintainability. Each agent is assigned specific tools (Read, Grep, Glob, Write, Bash) that define its capabilities and limit its actions to appropriate domains.

The system leverages a "subagent" pattern where higher-level workflows can invoke these specialized agents to handle specific tasks, creating a hierarchical delegation model that optimizes for both efficiency and accuracy. This approach allows the main agent to focus on high-level planning and coordination while delegating mechanical or specialized tasks to agents optimized for those purposes.

**Section sources**
- [context-fetcher.md](file://claude-code/agents/context-fetcher.md#L1-L10)
- [date-checker.md](file://claude-code/agents/date-checker.md#L1-L10)
- [file-creator.md](file://claude-code/agents/file-creator.md#L1-L10)

## Core Agent Analysis

### Context Fetcher Agent

The context-fetcher agent specializes in retrieving and extracting relevant information from Agent OS documentation files while avoiding duplication. It operates with a "context check first" principle, determining if requested information is already available before retrieving new content.

```mermaid
flowchart TD
Start([Request Received]) --> CheckContext["Check if information<br/>already in context"]
CheckContext --> |Already in context| ReturnContext["Return: ✓ Already in context"]
CheckContext --> |Not in context| LocateFiles["Locate requested file(s)"]
LocateFiles --> ExtractContent["Extract relevant sections only"]
ExtractContent --> UseGrep["Use grep for targeted searches"]
UseGrep --> ReturnContent["Return: 📄 Retrieved from [file-path]"]
ReturnContext --> End([Response])
ReturnContent --> End
```

**Diagram sources**
- [context-fetcher.md](file://claude-code/agents/context-fetcher.md#L15-L50)

**Section sources**
- [context-fetcher.md](file://claude-code/agents/context-fetcher.md#L1-L67)

### Date Checker Agent

The date-checker agent determines the current date using file system timestamps, providing a reliable method for AI systems to access temporal information without requiring direct user input.

```mermaid
flowchart TD
Start([Date Request]) --> CheckContext["Check if date already<br/>in context (YYYY-MM-DD)"]
CheckContext --> |Date in context| ReturnExisting["Return: ✓ Date already in context"]
CheckContext --> |Date not in context| CreateTemp["Create temporary file:<br/>.agent-os/specs/.date-check"]
CreateTemp --> ReadTimestamp["Read file timestamp<br/>with ls -la"]
ReadTimestamp --> ParseDate["Parse timestamp to<br/>YYYY-MM-DD format"]
ParseDate --> Validate["Validate date format<br/>& reasonableness"]
Validate --> Cleanup["Clean up temporary file"]
Cleanup --> ReturnDate["Return: Today's date: YYYY-MM-DD"]
ReturnExisting --> End([Response])
ReturnDate --> End
```

**Diagram sources**
- [date-checker.md](file://claude-code/agents/date-checker.md#L20-L50)

**Section sources**
- [date-checker.md](file://claude-code/agents/date-checker.md#L1-L95)

### File Creator Agent

The file-creator agent handles the creation of files, directories, and application of templates according to Agent OS conventions, ensuring consistent project structure and documentation.

```mermaid
classDiagram
class FileCreator {
+createDirectory(path)
+createFile(path, content)
+applyTemplate(template, data)
+handleBatchCreation(request)
+validatePathReferences()
+manageDirectoryStructure()
}
class Template {
+spec_md
+spec_lite_md
+technical_spec_md
+database_schema_md
+api_spec_md
+tests_md
+tasks_md
+mission_md
+mission_lite_md
+tech_stack_md
+roadmap_md
+decisions_md
}
class TemplateData {
+SPEC_NAME
+CURRENT_DATE
+OVERVIEW_CONTENT
+USER_STORIES_CONTENT
+SCOPE_CONTENT
+OUT_OF_SCOPE_CONTENT
+DELIVERABLE_CONTENT
+FRAMEWORK
+VERSION
+DATABASE
+JS_FRAMEWORK
+CSS_FRAMEWORK
+DECISION_CONTENT
+CONTEXT_CONTENT
+RATIONALE_CONTENT
}
FileCreator --> Template : "uses"
FileCreator --> TemplateData : "populates"
Template --> TemplateData : "requires"
```

**Diagram sources**
- [file-creator.md](file://claude-code/agents/file-creator.md#L15-L50)

**Section sources**
- [file-creator.md](file://claude-code/agents/file-creator.md#L1-L359)

### Git Workflow Agent

The git-workflow agent manages git operations including branch creation, commits, and pull request creation, following Agent OS conventions for branch naming and commit messages.

```mermaid
sequenceDiagram
participant Main as Main Agent
participant GW as git-workflow Agent
participant Git as Git System
Main->>GW : "Complete git workflow for feature"
GW->>Git : git status
Git-->>GW : Current branch info
alt On main branch
GW->>Git : git checkout -b feature-name
end
GW->>Git : git add .
GW->>Git : git commit -m "descriptive message"
GW->>Git : git push origin feature-name
GW->>Git : gh pr create
Git-->>GW : PR #123 created
GW-->>Main : "✓ Created branch, committed, pushed, created PR"
```

**Diagram sources**
- [git-workflow.md](file://claude-code/agents/git-workflow.md#L15-L30)

**Section sources**
- [git-workflow.md](file://claude-code/agents/git-workflow.md#L1-L145)

### Project Manager Agent

The project-manager agent tracks task completion and updates project documentation, maintaining accurate records of progress across specifications and roadmaps.

```mermaid
flowchart TD
Start([Task Completion]) --> VerifyImplementation["Verify implementation meets<br/>specification requirements"]
VerifyImplementation --> CheckTesting["Check for proper testing<br/>& documentation"]
CheckTesting --> ValidateCriteria["Validate task acceptance<br/>criteria are met"]
ValidateCriteria --> UpdateTasks["Mark tasks as complete<br/>in tasks.md with [x]"]
UpdateTasks --> UpdateRoadmap["Update roadmap.md with<br/>completed milestones"]
UpdateRoadmap --> CreateRecap["Create dated recap file in<br/>.agent-os/product/recaps/"]
CreateRecap --> End([Documentation Updated])
```

**Diagram sources**
- [project-manager.md](file://claude-code/agents/project-manager.md#L15-L30)

**Section sources**
- [project-manager.md](file://claude-code/agents/project-manager.md#L1-L42)

### Test Runner Agent

The test-runner agent executes tests and analyzes failures, providing focused feedback without attempting to fix issues, maintaining a clear separation of concerns.

```mermaid
sequenceDiagram
participant Main as Main Agent
participant TR as test-runner Agent
participant Test as Test System
Main->>TR : "Run specified tests"
TR->>Test : Execute test command
Test-->>TR : Test results
alt Tests Pass
TR-->>Main : "✅ All tests passing"
else Tests Fail
TR->>TR : Analyze failures
loop Each failed test
TR->>TR : Extract test name, location
TR->>TR : Compare expected vs actual
TR->>TR : Identify fix location
TR->>TR : Suggest fix approach
end
TR-->>Main : "❌ Failing tests with analysis"
end
```

**Diagram sources**
- [test-runner.md](file://claude-code/agents/test-runner.md#L15-L30)

**Section sources**
- [test-runner.md](file://claude-code/agents/test-runner.md#L1-L60)

## Agent Integration and Installation

The integration of Claude Code agents into projects occurs through the Agent OS installation system, which copies agent templates from the source repository to the target project directory. This process is managed by both Python-based and shell-based installers that handle platform-specific file mappings and directory structures.

The installation system follows a consistent pattern across different platforms, with Claude Code agents being copied from `claude-code/agents/` in the source repository to `.claude/agents/` in the target project. This mapping ensures that agents are available in the expected location for the AI coding assistant to access them during development workflows.

```mermaid
flowchart LR
Source[Agent OS Repository] --> |Copy| Target[Project Directory]
subgraph Source
S1[claude-code/agents/]
S2[instructions/]
S3[standards/]
S4[config.yml]
end
subgraph Target
T1[.claude/agents/]
T2[.agent-os/instructions/]
T3[.agent-os/standards/]
T4[.agent-os/config.yml]
end
S1 --> T1
S2 --> T2
S3 --> T3
S4 --> T4
```

**Diagram sources**
- [installer.py](file://src/installer.py#L50-L100)
- [INSTALL.md](file://INSTALL.md#L50-L80)

**Section sources**
- [installer.py](file://src/installer.py#L1-L155)
- [INSTALL.md](file://INSTALL.md#L1-L154)

## Workflow Orchestration

Agent OS orchestrates complex development workflows through a hierarchical system of instructions that coordinate the activities of multiple agents. The core workflow for executing tasks, defined in `execute-tasks.md`, demonstrates this orchestration by integrating several agents in a structured sequence across three phases: pre-execution setup, task execution loop, and post-execution tasks.

The workflow begins with context analysis using the context-fetcher agent to gather essential information from documentation files, followed by git branch management using the git-workflow agent to ensure proper isolation. During task execution, the system leverages the test-runner agent for focused test verification and concludes with post-execution tasks that involve multiple agents for comprehensive verification and documentation.

```mermaid
flowchart TD
A[execute-tasks.md] --> B[Phase 1: Pre-Execution]
A --> C[Phase 2: Task Execution Loop]
A --> D[Phase 3: Post-Execution]
B --> B1[Step 1: Task Assignment]
B --> B2[Step 2: Context Analysis]
B2 --> CF[context-fetcher]
B --> B3[Step 3: Git Branch Management]
B3 --> GW[git-workflow]
C --> C1[Step 4: Task Execution Loop]
C1 --> ET[execute-task.md]
ET --> ET1[Step 1: Task Understanding]
ET --> ET2[Step 2: Technical Spec Review]
ET --> ET3[Step 3: Best Practices Review]
ET3 --> CF[context-fetcher]
ET --> ET4[Step 4: Code Style Review]
ET4 --> CF[context-fetcher]
ET --> ET5[Step 5: Task Execution]
ET --> ET6[Step 6: Task-Specific Test Verification]
ET6 --> TR[test-runner]
ET --> ET7[Step 7: Task Status Updates]
D --> D1[Step 1: Run All Tests]
D1 --> TR[test-runner]
D --> D2[Step 2: Git Workflow]
D2 --> GW[git-workflow]
D --> D3[Step 3: Tasks Completion Verification]
D3 --> PM[project-manager]
D --> D4[Step 4: Roadmap Progress Update]
D4 --> PM[project-manager]
D --> D5[Step 5: Create Recap Document]
D5 --> PM[project-manager]
D --> D6[Step 6: Completion Summary]
D6 --> PM[project-manager]
D --> D7[Step 7: Task Completion Notification]
D7 --> PM[project-manager]
```

**Diagram sources**
- [execute-tasks.md](file://instructions/core/execute-tasks.md#L1-L20)
- [execute-task.md](file://instructions/core/execute-task.md#L1-L20)
- [post-execution-tasks.md](file://instructions/core/post-execution-tasks.md#L1-L20)

**Section sources**
- [execute-tasks.md](file://instructions/core/execute-tasks.md#L1-L187)
- [execute-task.md](file://instructions/core/execute-task.md#L1-L263)
- [post-execution-tasks.md](file://instructions/core/post-execution-tasks.md#L1-L249)

## CLI Command Invocation

The Agent OS CLI provides a user-friendly interface for installing and managing the system in project directories. The `agent-os install` command serves as the primary entry point, accepting flags to enable specific platforms including Claude Code, and handling the installation process through the underlying `installer.py` module.

The CLI implementation uses Click for command-line interface definition and Rich for enhanced terminal output, providing progress indicators and formatted messages that improve user experience. Platform selection flags (`--claude-code`, `--cursor`, etc.) map directly to the platform configuration in the installer, creating a seamless connection between user input and installation behavior.

```mermaid
sequenceDiagram
participant User
participant CLI
participant Installer
participant FileSystem
User->>CLI : agent-os install --claude-code --cursor
CLI->>CLI : Parse command line arguments
CLI->>Installer : Initialize AgentOsInstaller
CLI->>Installer : Set platform flags
CLI->>Installer : Set overwrite flags
Installer->>FileSystem : Check source directory
loop Each installation item
Installer->>FileSystem : Copy source to destination
alt Directory
FileSystem-->>Installer : Copy directory recursively
else File
FileSystem-->>Installer : Copy file
end
end
Installer-->>CLI : Return success status
CLI-->>User : Display installation results
```

**Diagram sources**
- [cli.py](file://src/cli.py#L50-L100)
- [installer.py](file://src/installer.py#L100-L150)

**Section sources**
- [cli.py](file://src/cli.py#L1-L187)
- [installer.py](file://src/installer.py#L1-L155)

## Common Issues and Solutions

### Prompt Ambiguity

Prompt ambiguity can occur when agent instructions are not specific enough, leading to inconsistent or incorrect behavior. The Agent OS system addresses this through several mechanisms:

1. **Structured Templates**: Agent templates use clear YAML frontmatter and standardized sections to ensure consistent structure
2. **Explicit Constraints**: Each agent includes "Important Constraints" sections that define boundaries and limitations
3. **Output Format Specifications**: Agents are required to follow specific output formats, reducing variability in responses
4. **Context Checking**: Agents like context-fetcher and date-checker include explicit context checking to avoid redundant operations

### Agent Role Overlap

Role overlap between agents could lead to confusion about which agent should handle specific tasks. Agent OS prevents this through:

1. **Specialized Responsibilities**: Each agent has clearly defined core responsibilities that distinguish it from others
2. **Tool Restrictions**: Agents are limited to specific tool sets that align with their intended functions
3. **Behavioral Constraints**: Explicit "Important Constraints" sections prevent agents from performing actions outside their domain
4. **Hierarchical Orchestration**: Higher-level workflows explicitly specify which agent to use for each task

For example, while both file-creator and git-workflow agents can use Bash commands, file-creator is restricted to file and directory operations, while git-workflow is specialized for git operations, with clear boundaries defined in their respective templates.

**Section sources**
- [context-fetcher.md](file://claude-code/agents/context-fetcher.md#L50-L60)
- [git-workflow.md](file://claude-code/agents/git-workflow.md#L50-L60)
- [file-creator.md](file://claude-code/agents/file-creator.md#L300-L320)

## Performance Considerations

### Response Accuracy

Agent OS enhances response accuracy through several design principles:

1. **Focused Specialization**: Each agent is specialized for a narrow domain, improving expertise and reducing errors
2. **Context Minimization**: Agents retrieve only necessary context, reducing the risk of information overload
3. **Template-Driven Output**: Standardized templates ensure consistent and predictable output formats
4. **Validation Rules**: Agents include validation rules (e.g., date-checker's format validation) to ensure correctness

The system also implements a hierarchical delegation model where complex tasks are broken down into smaller, more manageable operations handled by specialized agents, improving overall accuracy through division of labor.

### Token Usage Optimization

Token usage is optimized through several strategies:

1. **Context Checking**: Agents check if information is already in context before retrieving it, avoiding redundant content
2. **Selective Extraction**: Agents extract only specific sections needed rather than entire files
3. **Concise Output**: Agents are instructed to keep responses focused and minimal
4. **Efficient Workflows**: Orchestration workflows minimize redundant operations and agent invocations

For example, the context-fetcher agent uses grep to find relevant sections rather than reading entire files, significantly reducing token usage for information retrieval tasks. Similarly, the date-checker agent uses a file system timestamp method rather than requesting the date from the user, minimizing interaction overhead.

**Section sources**
- [context-fetcher.md](file://claude-code/agents/context-fetcher.md#L10-L20)
- [date-checker.md](file://claude-code/agents/date-checker.md#L10-L20)
- [execute-tasks.md](file://instructions/core/execute-tasks.md#L50-L60)

## Conclusion

Agent OS provides a comprehensive framework for integrating Claude Code and other AI coding assistants into structured development workflows. Through its system of specialized agents, each defined by detailed Markdown templates, the platform transforms general-purpose AI assistants into focused development partners with clearly defined roles and responsibilities.

The integration is achieved through a sophisticated installation system that deploys agent templates to project directories, where they can be invoked by higher-level workflows to handle specific tasks. This approach enables a division of labor where each agent excels in its specialized domain, from context retrieval and date determination to file creation, git operations, task management, and test execution.

The orchestration of these agents through hierarchical workflows ensures that complex development processes are executed consistently and reliably, with each agent contributing its specialized capabilities to the overall workflow. This structured approach addresses common challenges in AI-assisted development, including prompt ambiguity, role overlap, and token efficiency, resulting in a more predictable and effective development experience.

By providing a standardized framework that can be adapted to different AI coding platforms, Agent OS enables teams to leverage the power of AI assistants while maintaining control over code quality, project structure, and development processes.