# Agent OS Installation

Agent OS can be installed using either Python pip (recommended) or manual shell scripts.

## Python Installation (Recommended)

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### 1. Install Agent OS

```bash
# Install from PyPI (when available)
pip install agent-os

# Or install from source
pip install git+https://github.com/fenghaitao/agent-os.git

# Or install in development mode
git clone https://github.com/fenghaitao/agent-os.git
cd agent-os
pip install -e .
```

### 2. Install Agent OS

Install Agent OS directly in your project directory:

```bash
# Install with all platforms in current directory
agent-os install --all

# Install with specific platforms in current directory
agent-os install --claude-code --cursor
agent-os install --github-copilot --qwen-code

# Install in specific project directory
agent-os install /path/to/project --claude-code --cursor
agent-os install /path/to/project --all

# Install from a specific branch
agent-os install --all --branch develop
```

### 3. Check Status

Check Agent OS installation status in a project:

```bash
# Check status in current directory
agent-os status .

# Check status in specific directory
agent-os status /path/to/project
```

### 4. Get Help

```bash
# Show general help
agent-os --help

# Show command-specific help
agent-os install --help
agent-os status --help
```

## Manual Installation

### 1. Base Installation (One-time setup)

The base installation creates a `.agent-os` folder in your current directory (base_folder) with all the Agent OS files and platform templates.

```bash
# Install Agent OS base with specific platforms
curl -sSL https://raw.githubusercontent.com/fenghaitao/agent-os/main/setup/base.sh | bash -s -- --claude-code --cursor
curl -sSL https://raw.githubusercontent.com/fenghaitao/agent-os/main/setup/base.sh | bash -s -- --github-copilot --qwen-code

# Or install all platforms at once
curl -sSL https://raw.githubusercontent.com/fenghaitao/agent-os/main/setup/base.sh | bash -s -- --all
```

This creates a `.agent-os/` folder containing:
- `instructions/` - Core Agent OS instruction files
- `standards/` - Development standards and best practices
- `claude-code/agents/` - Claude Code agent templates (if enabled)
- `github-copilot/prompts/` - GitHub Copilot prompt templates (if enabled)
- `qwen-code/commands/` - Qwen Code command templates (if enabled)
- `setup/project.sh` - Project installation script

**Note**: it's also able to install Agent OS from a developing branch like:
```bash
curl -sSL https://raw.githubusercontent.com/fenghaitao/agent-os/feat-br0/setup/base.sh | bash -s -- --claude-code --cursor --branch feat-br0
```


### 2. Project Installation

From the base installation directory (where `.agent-os/` folder exists), run the project script to install Agent OS in your project:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run the project installation script from the base directory
base_folder/.agent-os/setup/project.sh --github-copilot --qwen-code
```

Or if you're in the same directory as the `.agent-os` folder:

```bash
# Install in your project directory
./.agent-os/setup/project.sh --github-copilot --qwen-code
```

## Platform Support

Agent OS supports multiple AI coding platforms:

- **Claude Code**: `.claude/commands/` + `.claude/agents/`
- **Cursor**: `.cursor/rules/`
- **GitHub Copilot**: `.github/prompts/` (`.prompt.md` files)
- **Qwen Code**: `.qwen/commands/`

## Usage

After installation, use the platform-specific commands:

- **Cursor**: `@plan-product`, `@create-spec`, etc.
- **Claude Code**: Reference files in `.claude/commands/`
- **GitHub Copilot**: Attach `.github/prompts/` files in chat
- **Qwen Code**: Reference `.qwen/commands/` files in prompts

## Requirements

### Python Installation
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

### Manual Installation
- Bash (for manual installation)
- Git (for version control)

## Troubleshooting

If you encounter issues:

1. Ensure you have the required dependencies installed
2. Check that you're in a project directory (not a bare repository)
3. Verify your platform supports the Agent OS file structure
4. Check the [GitHub Issues](https://github.com/fenghaitao/agent-os/issues) for known problems
