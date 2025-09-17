"""
Agent OS Command Line Interface

Provides a user-friendly CLI for Agent OS operations.
"""

from __future__ import annotations

import sys
import argparse
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from .installer import AgentOsInstaller

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="agent-os")
def cli():
    """Agent OS - A comprehensive product development workflow management system.
    
    Agent OS provides structured development workflows for AI coding platforms
    including Claude Code, Cursor, GitHub Copilot, and Qwen Code.
    """
    pass


@cli.command()
@click.argument('project_dir', type=click.Path(), default='.')
@click.option('--claude-code', is_flag=True, help='Enable Claude Code support')
@click.option('--cursor', is_flag=True, help='Enable Cursor support')
@click.option('--github-copilot', is_flag=True, help='Enable GitHub Copilot support')
@click.option('--qwen-code', is_flag=True, help='Enable Qwen Code support')
@click.option('--all', 'all_platforms', is_flag=True, help='Enable all platforms')
@click.option('--overwrite-instructions', is_flag=True, help='Overwrite existing instruction files')
@click.option('--overwrite-standards', is_flag=True, help='Overwrite existing standards files')
@click.option('--overwrite-config', is_flag=True, help='Overwrite existing config files')
@click.option('--branch', default='main', help='Git branch to install from')
def install(project_dir: str, claude_code: bool, cursor: bool, github_copilot: bool,
           qwen_code: bool, all_platforms: bool, overwrite_instructions: bool,
           overwrite_standards: bool, overwrite_config: bool, branch: str):
    """Install Agent OS in a project directory.
    
    This command installs Agent OS directly in your project directory,
    downloading all necessary files and setting up platform-specific
    configurations in one step.
    
    Examples:
        # Install with all platforms in current directory
        agent-os install --all
        
        # Install specific platforms in a project
        agent-os install /path/to/project --claude-code --cursor
        
        # Install from a specific branch
        agent-os install --all --branch develop
    """
    # Set up installer
    base_url = f"https://raw.githubusercontent.com/fenghaitao/agent-os/{branch}"
    installer = AgentOsInstaller(base_url)
    
    # Set platforms
    if all_platforms:
        installer.set_platforms(
            claude_code=True,
            cursor=True,
            github_copilot=True,
            qwen_code=True
        )
    else:
        installer.set_platforms(
            claude_code=claude_code,
            cursor=cursor,
            github_copilot=github_copilot,
            qwen_code=qwen_code
        )
    
    # Set overwrite flags
    installer.set_overwrite_flags(
        instructions=overwrite_instructions,
        standards=overwrite_standards,
        config=overwrite_config
    )
    
    # Perform installation
    project_path = Path(project_dir).resolve()
    
    try:
        success = installer.install(project_path)
        if success:
            console.print(Panel(
                Text("Agent OS installation completed successfully!", style="bold green"),
                title="Success"
            ))
        else:
            console.print(Panel(
                Text("Agent OS installation failed!", style="bold red"),
                title="Error"
            ))
            sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
def info():
    """Show Agent OS information and available platforms."""
    console.print(Panel(
        Text("Agent OS Information", style="bold blue"),
        title="Agent OS"
    ))
    
    # Create info table
    table = Table(title="Available Platforms")
    table.add_column("Platform", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Directory", style="green")
    
    table.add_row("Claude Code", "Claude Code agent templates", ".claude/commands/ + .claude/agents/")
    table.add_row("Cursor", "Cursor rule files", ".cursor/rules/")
    table.add_row("GitHub Copilot", "GitHub Copilot prompt templates", ".github/prompts/")
    table.add_row("Qwen Code", "Qwen Code command templates", ".qwen/commands/")
    
    console.print(table)
    
    console.print("\n[yellow]Usage Examples:[/yellow]")
    console.print("  agent-os install --all")
    console.print("  agent-os install /path/to/project --claude-code --cursor")
    console.print("  agent-os install --github-copilot --qwen-code")


@cli.command()
@click.argument('project_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def status(project_dir: str):
    """Check Agent OS status in a project directory."""
    project_path = Path(project_dir).resolve()
    
    console.print(Panel(
        Text(f"Agent OS Status for: {project_dir}", style="bold blue"),
        title="Status Check"
    ))
    
    # Check for platform directories
    platforms = {
        'Claude Code': project_path / '.claude',
        'Cursor': project_path / '.cursor',
        'GitHub Copilot': project_path / '.github',
        'Qwen Code': project_path / '.qwen',
    }
    
    table = Table(title="Platform Status")
    table.add_column("Platform", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Path", style="green")
    
    for platform, path in platforms.items():
        if path.exists():
            table.add_row(platform, "✓ Installed", str(path))
        else:
            table.add_row(platform, "✗ Not installed", str(path))
    
    console.print(table)


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
