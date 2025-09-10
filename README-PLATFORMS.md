# Agent OS Platform Support

Agent OS now supports multiple AI platforms with a unified approach:

## Supported Platforms

### 1. Claude Code (Original)
- **Directory**: `.claude/`
- **Structure**: Commands and agents with full subagent support
- **Usage**: `/plan-product`, `/create-spec`, etc.

### 2. Cursor
- **Directory**: `.cursor/rules/`
- **Structure**: Simple rule files with @ references
- **Usage**: `@plan-product`, `@create-spec`, etc.

### 3. GitHub Copilot (New)
- **Directory**: `.github/prompts/`
- **Structure**: Markdown files (`.md`) with @ references
- **Source**: `github-copilot/prompts/` in Agent OS codebase
- **Usage**: Attach files in Copilot Chat sessions, use @.agent-os/instructions/ for full workflow

### 4. Qwen Code (New)
- **Directory**: `.qwen/commands/`
- **Structure**: TOML files (`.toml`) with @ references
- **Usage**: Reference files in prompts, use @.agent-os/instructions/ for full workflow

## Installation

Install Agent OS with platform support:

```bash
# Install with specific platforms
./setup/project.sh --claude-code --cursor --github-copilot --qwen-code

# Install with all platforms
./setup/project.sh --claude-code --cursor --github-copilot --qwen-code
```

## Platform-Specific Usage

### GitHub Copilot
1. Attach `.github/prompts/` files in Copilot Chat sessions
2. Use `@.agent-os/instructions/` references for full Agent OS workflow
3. Example: "Follow the plan-product instructions to create a new product"

### Qwen Code
1. Reference `.qwen/commands/` files in your prompts
2. Use `@.agent-os/instructions/` references for full Agent OS workflow
3. Example: "Follow the plan-product instructions to create a new product"

## Architecture

All platforms follow the same core principle:
- **Simple rule files** that reference the main Agent OS instructions
- **@ references** to load the full workflow from `.agent-os/instructions/`
- **Consistent experience** across all AI platforms

This approach ensures that:
- GitHub Copilot and Qwen Code get the same powerful workflows as Cursor
- No complex subagent implementations needed
- Easy to maintain and extend
- Consistent user experience across platforms
