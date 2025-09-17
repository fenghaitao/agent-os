"""
Agent OS Python Installer

This module provides Python-based installation functionality that copies
Agent OS files from the local repository to target project directories.
"""

from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

console = Console()


class AgentOsInstaller:
    """Agent OS installer that copies files from the local repository."""
    
    def __init__(self):
        """Initialize the installer."""
        self.overwrite_instructions = False
        self.overwrite_standards = False
        self.overwrite_config = False
        self.platforms = {
            'claude_code': False,
            'cursor': False,
            'github_copilot': False,
            'qwen_code': False,
            'adk': False,
        }
        
    def set_platforms(self, **kwargs) -> None:
        """Set platform flags.
        
        Args:
            **kwargs: Platform flags (claude_code, cursor, github_copilot, qwen_code)
        """
        for platform, enabled in kwargs.items():
            if platform in self.platforms:
                self.platforms[platform] = enabled
                
    def set_overwrite_flags(self, instructions: bool = False, standards: bool = False, 
                           config: bool = False) -> None:
        """Set overwrite flags.
        
        Args:
            instructions: Overwrite instruction files
            standards: Overwrite standards files
            config: Overwrite config files
        """
        self.overwrite_instructions = instructions
        self.overwrite_standards = standards
        self.overwrite_config = config
        
            
        
    def install(self, project_dir: Path) -> bool:
        """Install Agent OS directly in a project directory.
        
        This method copies Agent OS files from the local repository to the project directory.
        
        Args:
            project_dir: Project directory to install into
            
        Returns:
            True if successful, False otherwise
        """
        console.print(Panel(
            Text(f"Installing Agent OS in project: {project_dir}", style="bold blue"),
            title="Agent OS Installer"
        ))
        
        # Ensure project directory exists
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Get the source directory (where this installer is located)
        source_dir = Path(__file__).parent.parent
        
        # Define platform-specific installation mappings
        platform_mappings = []
        
        if self.platforms['claude_code']:
            platform_mappings.extend([
                ('claude-code/agents/', '.claude/agents/'),
            ])
            
        if self.platforms['cursor']:
            platform_mappings.append(('commands/', '.cursor/rules/'))
            
        if self.platforms['github_copilot']:
            platform_mappings.append(('github-copilot/prompts/', '.github/prompts/'))
            
        if self.platforms['qwen_code']:
            platform_mappings.append(('qwen-code/commands/', '.qwen/commands/'))
            
        # Handle ADK installation - installs to project .adk/
        if self.platforms['adk']:
            platform_mappings.extend([
                ('adk/agents/', '.adk/agents/'),
                ('commands/', '.adk/commands/'),
            ])
        
        # Always install core files
        core_files = [
            ('instructions/', '.agent-os/instructions/'),
            ('standards/', '.agent-os/standards/'),
            ('config.yml', '.agent-os/config.yml'),
        ]
        
        all_install_items = core_files + platform_mappings
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Installing Agent OS files...", total=len(all_install_items))
            
            for source_path, dest_path in all_install_items:
                progress.update(task, description=f"Installing {source_path}")
                
                source_file = source_dir / source_path
                dest_file = project_dir / dest_path
                
                if source_path.endswith('/'):
                    # Directory - copy recursively
                    if source_file.exists():
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        if dest_file.exists():
                            shutil.rmtree(dest_file)
                        shutil.copytree(source_file, dest_file)
                    else:
                        console.print(f"[yellow]Warning: Source directory {source_file} not found[/yellow]")
                else:
                    # File - copy it
                    if source_file.exists():
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_file, dest_file)
                    else:
                        console.print(f"[yellow]Warning: Source file {source_file} not found[/yellow]")
                    
                progress.advance(task)
                
        console.print("[green]✓ Agent OS installation completed![/green]")
        return True
        


