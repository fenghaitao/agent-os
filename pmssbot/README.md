# PMSSBOT - PMSS Development Agent

A self-contained AI agent for PMSS (Power Management Sub-System) development, specializing in Python testbench device creation, register modeling, and power management validation for the SRV-PM project.

## 📁 Directory Structure

```
pmssbot/
├── pmssbot.yml                          # Agent configuration and metadata
├── install-pmssbot.sh                   # Self-contained installation script
├── README.md                            # This documentation
├── commands/                            # Command definitions
│   └── create-py-tb-device.md           # Device creation command
├── instructions/                        # Detailed implementation workflows
│   ├── core/                           # Core instruction workflows
│   │   └── create-py-tb-device.md       # Complete device creation workflow
│   └── meta/                           # Meta workflow files (pre/post flight)
└── github-copilot/                     # GitHub Copilot integration
    ├── chatmodes/                      # GitHub Copilot chatmode files
    │   └── pmssbot.chatmode.md         # Full Powell persona and chat interface
    └── prompts/                        # GitHub Copilot prompt files
        └── create-py-tb-dev.prompt.md  # Device creation prompt
```

## 🚀 Quick Installation

### Install in Your Project

```bash
# Install with GitHub Copilot integration
./install-pmssbot.sh --github-copilot /path/to/your/srv-pm-project

# Install in current directory with overwrite
./install-pmssbot.sh --github-copilot --overwrite .

# Basic installation without GitHub Copilot
./install-pmssbot.sh ~/my-project
```

### Installation Options

- `--github-copilot`: Install GitHub Copilot integration files in `.github/prompts/` and `.github/chatmodes/`
- `--overwrite`: Overwrite existing files during installation
- `-h, --help`: Show detailed help and examples

### ⚠️ Important: Reload GitHub Copilot After Installation

If VS Code is already open when you install pmssbot, you **must reload GitHub Copilot** to pick up the new files:

1. **Option 1: Reload VS Code Window**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Developer: Reload Window" and press Enter

2. **Option 2: Restart GitHub Copilot Extension**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "GitHub Copilot: Restart Extension" and press Enter

3. **Option 3: Restart VS Code**
   - Close and reopen VS Code

Without reloading, GitHub Copilot won't see the newly installed prompt and chatmode files.

## 💬 Usage with GitHub Copilot

### Chatmode Integration (Full Agent Experience)
```
@workspace /.github/chatmodes/pmssbot.chatmode.md
```
This activates the full Powell persona with complete PMSS development capabilities.

### Quick Access Commands
```
@workspace #pmssbot                    # Main chat interface
@workspace #create-py-tb-device        # Create Python testbench device
```

### Direct File References
```
# Complete Powell agent experience (recommended)
@workspace /.github/chatmodes/pmssbot.chatmode.md

# Individual command prompt files
@workspace /.github/prompts/create-py-tb-dev.prompt.md
```

### Natural Language
Just mention "pmssbot" or "Powell" in any GitHub Copilot conversation:
```
@workspace I need pmssbot to create a testbench device for the DDA IP
@workspace Help me with Powell's expertise on OSAL register analysis
```

## 🎯 Core Capabilities

### **Python TestBench Device Creation**
- Complete device creation workflow with OSAL integration
- confclass framework implementation
- Register generation from OSAL definitions
- Side effect implementations
- CMake build system integration

### **Register Analysis and Modeling**
- OSAL structure analysis
- Register bank organization
- Field definition extraction
- Python generation compatibility assessment
- Renaming suggestions for compatibility

### **Power Management Algorithms**
- P-state management implementation
- C-state transition algorithms
- FIVR control logic
- Power budget enforcement
- Thermal throttling mechanisms

### **Validation and Testing**
- Device implementation validation
- Register access testing
- Side effect verification
- Build system integration testing
- Performance impact assessment

## 🔧 Technical Details

### **Frameworks and Dependencies**
- Python Device Modeling Framework
- confclass library for device modeling
- osalgen framework for register generation
- Simics simulation platform
- CMake build system integration

### **Integration Points**
- SRV-PM project structure
- OSAL register definitions
- Die component integration
- Module loading and registration
- GitHub Copilot Chat interface

### **Reference Materials**
- Architecture guide: `srv-pm/promark/team_portal/arch_bkm/00_vp_arch/python_tb_device_guide.mmd`
- Reference implementation: `tb_dda.py`
- Build system documentation: srv-pm CMake patterns

## 👨‍💻 Meet Powell - Your PMSS Expert

PMSSBOT embodies **Powell**, an expert PMSS Development Engineer with:
- **Systematic approach** to device development
- **Interactive guidance** through complex workflows
- **Comprehensive validation** at every step
- **Integration focus** for seamless SRV-PM compatibility
- **Performance awareness** for simulation efficiency

## 📚 Command Reference

| Command | Purpose | Usage |
|---------|---------|--------|
| `*create-py-tb-device` | Create new Python testbench device | Device name, IP name, OSAL path |
| `*help` | Show all available commands | Interactive command list |

## 🎨 Self-Contained Design

This pmssbot directory is completely **self-contained**:
- ✅ All configuration files included
- ✅ Installation script with all dependencies
- ✅ Complete documentation and workflows
- ✅ GitHub Copilot integration ready
- ✅ No external dependencies on parent Agent OS structure
- ✅ Portable across different projects and environments

## 🚀 Getting Started

1. **Navigate to pmssbot directory**
2. **Run installation**: `./install-pmssbot.sh --github-copilot /your/project`
3. **⚠️ Reload GitHub Copilot** (if VS Code was already open)
4. **Open GitHub Copilot Chat** in your project
5. **Start conversation**: `@workspace /.github/chatmodes/pmssbot.chatmode.md`
6. **Create your first device**: Ask Powell to help create a testbench device

## 🔧 Troubleshooting

### GitHub Copilot Can't Find PMSSBOT Files

If GitHub Copilot shows "File not found" errors:

1. **Verify installation**: Check that `.github/chatmodes/` and `.github/prompts/` directories exist
2. **Reload GitHub Copilot**: Use one of these methods:
   - `Ctrl+Shift+P` → "Developer: Reload Window"
   - `Ctrl+Shift+P` → "GitHub Copilot: Restart Extension"  
   - Restart VS Code completely
3. **Check file paths**: Ensure you're using the correct paths:
   - `@workspace /.github/chatmodes/pmssbot.chatmode.md`
   - `@workspace /.github/prompts/create-py-tb-dev.prompt.md`

### PMSSBOT Not Responding as Expected

- Try using the full chatmode path: `@workspace /.github/chatmodes/pmssbot.chatmode.md`
- Wait for the Powell persona to activate before giving commands
- Use the `*` prefix for commands (e.g., `*create-py-tb-device`)

Ready to accelerate your PMSS development workflow! 🔋⚡