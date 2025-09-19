#!/bin/bash

# PMSSBOT Agent Installation Script
# This script installs the pmssbot agent in a project directory with GitHub Copilot integration

set -e  # Exit on error

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PMSSBOT_SOURCE_DIR="$SCRIPT_DIR"

# Initialize flags
GITHUB_COPILOT=false
OVERWRITE=false
TARGET_DIR=""
OVERWRITE=false

# Usage function
usage() {
    cat << EOF
Usage: $0 [OPTIONS] [TARGET_DIRECTORY]

Install PMSSBOT agent for PMSS development with Python testbench device support.

OPTIONS:
    --github-copilot       Install GitHub Copilot integration files only
    --overwrite            Overwrite existing files
    -h, --help             Show this help message

ARGUMENTS:
    TARGET_DIRECTORY       Directory to install pmssbot (default: current directory)

EXAMPLES:
    $0 --github-copilot ~/my-srv-pm-project          # GitHub Copilot integration (recommended)
    $0 --github-copilot --overwrite .
    $0 ~/srv-pm                                      # Base installation (for future integrations)
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --github-copilot|--copilot)
            GITHUB_COPILOT=true
            shift
            ;;
        --overwrite)
            OVERWRITE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            usage
            exit 1
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            else
                echo "Error: Multiple target directories specified" >&2
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Set default target directory if not specified
if [[ -z "$TARGET_DIR" ]]; then
    TARGET_DIR="$(pwd)"
fi

# Convert to absolute path
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || {
    echo "Error: Target directory '$TARGET_DIR' does not exist" >&2
    exit 1
}

echo "Installing PMSSBOT Agent..."
echo "Source: $PMSSBOT_SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo "GitHub Copilot: $GITHUB_COPILOT"

# Verify source directory exists
if [[ ! -d "$PMSSBOT_SOURCE_DIR" ]]; then
    echo "Error: PMSSBOT source directory not found: $PMSSBOT_SOURCE_DIR" >&2
    exit 1
fi

# Create .pmssbot directory and copy all pmssbot files (for all installation modes)
echo "Creating .pmssbot directory structure..."
mkdir -p "$TARGET_DIR/.pmssbot"

# Copy entire pmssbot structure to .pmssbot
echo "Copying pmssbot files to .pmssbot/..."

# Copy pmssbot.yml to .pmssbot directory
if [[ -f "$SCRIPT_DIR/pmssbot.yml" ]]; then
    target_config="$TARGET_DIR/.pmssbot/pmssbot.yml"
    if [[ -f "$target_config" ]] && [[ "$OVERWRITE" != true ]]; then
        echo "Warning: .pmssbot/pmssbot.yml already exists, skipping (use --overwrite to replace)"
    else
        cp "$SCRIPT_DIR/pmssbot.yml" "$target_config"
        echo "  Installed: .pmssbot/pmssbot.yml"
    fi
fi

# Copy all pmssbot directories
for subdir in commands instructions github-copilot; do
    if [[ -d "$PMSSBOT_SOURCE_DIR/$subdir" ]]; then
        echo "Copying $subdir..."
        if [[ -d "$TARGET_DIR/.pmssbot/$subdir" ]] && [[ "$OVERWRITE" != true ]]; then
            echo "Warning: .pmssbot/$subdir already exists, skipping (use --overwrite to replace)"
        else
            cp -r "$PMSSBOT_SOURCE_DIR/$subdir" "$TARGET_DIR/.pmssbot/"
            echo "  Installed: .pmssbot/$subdir/"
        fi
    fi
done

# Create .github directory structure for GitHub Copilot
if [[ "$GITHUB_COPILOT" == true ]]; then
    echo "Setting up GitHub Copilot integration..."
    
    # Create .github directories
    mkdir -p "$TARGET_DIR/.github/prompts"
    mkdir -p "$TARGET_DIR/.github/chatmodes"
    
    # Copy GitHub Copilot prompt files from .pmssbot
    if [[ -d "$TARGET_DIR/.pmssbot/github-copilot/prompts" ]]; then
        echo "Linking GitHub Copilot prompt files..."
        for prompt_file in "$TARGET_DIR/.pmssbot/github-copilot/prompts"/*; do
            if [[ -f "$prompt_file" ]]; then
                filename=$(basename "$prompt_file")
                target_file="$TARGET_DIR/.github/prompts/$filename"
                
                if [[ -f "$target_file" ]] && [[ "$OVERWRITE" != true ]]; then
                    echo "Warning: $target_file already exists, skipping (use --overwrite to replace)"
                else
                    cp "$prompt_file" "$target_file"
                    echo "  Installed: .github/prompts/$filename"
                fi
            fi
        done
    fi
    
    # Copy GitHub Copilot chatmode files from .pmssbot
    if [[ -d "$TARGET_DIR/.pmssbot/github-copilot/chatmodes" ]]; then
        echo "Linking GitHub Copilot chatmode files..."
        for chatmode_file in "$TARGET_DIR/.pmssbot/github-copilot/chatmodes"/*; do
            if [[ -f "$chatmode_file" ]]; then
                filename=$(basename "$chatmode_file")
                target_file="$TARGET_DIR/.github/chatmodes/$filename"
                
                if [[ -f "$target_file" ]] && [[ "$OVERWRITE" != true ]]; then
                    echo "Warning: $target_file already exists, skipping (use --overwrite to replace)"
                else
                    cp "$chatmode_file" "$target_file"
                    echo "  Installed: .github/chatmodes/$filename"
                fi
            fi
        done
    fi
fi

# Install additional files only if GitHub Copilot integration is not specified
if [[ "$GITHUB_COPILOT" != true ]]; then
    # Copy pmssbot.yml to root for backward compatibility
    if [[ -f "$TARGET_DIR/.pmssbot/pmssbot.yml" ]]; then
        target_config="$TARGET_DIR/pmssbot.yml"
        if [[ -f "$target_config" ]] && [[ "$OVERWRITE" != true ]]; then
            echo "Warning: pmssbot.yml already exists, skipping (use --overwrite to replace)"
        else
            cp "$TARGET_DIR/.pmssbot/pmssbot.yml" "$target_config"
            echo "  Installed: pmssbot.yml (compatibility copy)"
        fi
    fi

    # Create pmssbot directory and link to .pmssbot for backward compatibility
    if [[ ! -d "$TARGET_DIR/pmssbot" ]] || [[ "$OVERWRITE" == true ]]; then
        echo "Creating pmssbot compatibility link..."
        rm -rf "$TARGET_DIR/pmssbot" 2>/dev/null || true
        ln -sf ".pmssbot" "$TARGET_DIR/pmssbot"
        echo "  Created: pmssbot -> .pmssbot (symbolic link)"
    fi
fi

# Create README for pmssbot usage in .pmssbot directory
cat > "$TARGET_DIR/.pmssbot/README.md" << 'EOF'
# PMSSBOT - PMSS Development Agent

PMSSBOT is your expert AI assistant for PMSS (Power Management Sub-System) development, specializing in Python testbench device creation, register modeling, and power management validation.

## Quick Start

### GitHub Copilot Integration

Use PMSSBOT in GitHub Copilot Chat by referencing the chatmode file:

```
@workspace /.github/chatmodes/pmssbot.chatmode.md
```

Or use specific commands:

```
@workspace /.github/prompts/create-py-tb-dev.prompt.md
```

### ⚠️ Important: Reload GitHub Copilot

If VS Code was open during installation, reload GitHub Copilot to see the new files:
- Press Ctrl+Shift+P → "Developer: Reload Window" 
- Or Press Ctrl+Shift+P → "GitHub Copilot: Restart Extension"

### Available Commands

- **create-py-tb-device** - Create new Python testbench device with OSAL integration

### Example Usage

1. **Activate Powell agent:**
   ```
   @workspace /.github/chatmodes/pmssbot.chatmode.md
   ```

2. **Create a new testbench device:**
   ```
   @workspace I need to create a Python testbench device for the DDA IP using OSAL from dmr_imh_fv
   ```

2. **Analyze OSAL registers:**
   ```
   @workspace Analyze the register structure in psf20_dmrpc5psf123_psf0 IP
   ```

3. **Validate device implementation:**
   ```
   @workspace Validate my tb_pmss_ctrl device implementation
   ```

## Key Features

- **Systematic Development**: Follow structured workflows for device creation
- **OSAL Integration**: Automatic register generation from OSAL definitions
- **confclass Framework**: Python Device Modeling Framework support
- **Build System Integration**: CMake and Simics module configuration
- **Comprehensive Validation**: Testing and firmware compatibility

## References

- Architecture Guide: srv-pm/promark/team_portal/arch_bkm/00_vp_arch/python_tb_device_guide.mmd
- Reference Implementation: tb_dda.py device example
- Build System: srv-pm CMake integration patterns

Ready to accelerate your PMSS development workflow!
EOF

echo ""
echo "✅ PMSSBOT installation complete!"
echo ""
echo "📁 Installed Components:"
echo "   • .pmssbot/ - Complete pmssbot agent structure"
if [[ "$GITHUB_COPILOT" == true ]]; then
echo "   • .github/prompts/ - GitHub Copilot integration prompts"
echo "   • .github/chatmodes/ - GitHub Copilot chatmode files"
else
echo "   • pmssbot.yml - Agent configuration (compatibility copy)"
echo "   • pmssbot/ -> .pmssbot (symbolic link for compatibility)"
fi
echo ""
echo "🚀 Quick Start:"
if [[ "$GITHUB_COPILOT" == true ]]; then
echo "   • Use '@workspace /.github/chatmodes/pmssbot.chatmode.md' for full Powell agent"
echo "   • Use '@workspace #pmssbot' for quick access in GitHub Copilot Chat"
echo "   • Use '@workspace #create-device' for device creation"
echo "   • Or mention 'pmssbot' or 'Powell' in any GitHub Copilot conversation"
else
echo "   • Check .pmssbot/README.md or pmssbot/README.md for detailed usage instructions"
fi
echo "   • Repository automatically provides PMSSBOT context to GitHub Copilot"
echo ""
if [[ "$GITHUB_COPILOT" == true ]]; then
echo "⚠️  IMPORTANT: Reload GitHub Copilot if VS Code is already open!"
echo "   • Press Ctrl+Shift+P → 'Developer: Reload Window'"
echo "   • Or Press Ctrl+Shift+P → 'GitHub Copilot: Restart Extension'"
echo "   • Or restart VS Code completely"
echo "   (Without reloading, GitHub Copilot won't see the new files)"
echo ""
fi
echo "Happy PMSS development! 🔋⚡"