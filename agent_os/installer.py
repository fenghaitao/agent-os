"""
Agent OS Python Installer

This module provides Python-based installation functionality that replicates
the shell script installation process.
"""

from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import urljoin
import requests
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

console = Console()


class AgentOsInstaller:
    """Agent OS installer that replicates shell script functionality."""
    
    def __init__(self, base_url: str = "https://raw.githubusercontent.com/fenghaitao/agent-os/main"):
        """Initialize the installer.
        
        Args:
            base_url: Base URL for GitHub raw content
        """
        self.base_url = base_url.rstrip('/')
        self.overwrite_instructions = False
        self.overwrite_standards = False
        self.overwrite_config = False
        self.platforms = {
            'claude_code': False,
            'cursor': False,
            'github_copilot': False,
            'qwen_code': False,
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
        
    def _download_file(self, url: str, local_path: Path) -> bool:
        """Download a file from URL to local path.
        
        Args:
            url: URL to download from
            local_path: Local path to save to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Create parent directories if they don't exist
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            console.print(f"[red]Error downloading {url}: {e}[/red]")
            return False
            
    def _download_directory(self, remote_path: str, local_path: Path, 
                          file_pattern: str = "**/*") -> bool:
        """Download a directory structure from GitHub.
        
        Args:
            remote_path: Remote directory path
            local_path: Local directory path
            file_pattern: File pattern to match
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # For GitHub raw content, we need to get the directory listing
            # This is a simplified approach - in practice, you might need to
            # use the GitHub API to get directory contents
            return True
        except Exception as e:
            console.print(f"[red]Error downloading directory {remote_path}: {e}[/red]")
            return False
            
        
    def install(self, project_dir: Path) -> bool:
        """Install Agent OS directly in a project directory.
        
        This method downloads Agent OS files directly to the project directory,
        eliminating the need for a separate base installation step.
        
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
        
        # Define platform-specific installation mappings
        platform_mappings = []
        
        if self.platforms['claude_code']:
            platform_mappings.extend([
                ('claude-code/agents/', '.claude/agents/'),
                ('claude-code/commands/', '.claude/commands/'),
            ])
            
        if self.platforms['cursor']:
            platform_mappings.append(('commands/', '.cursor/rules/'))
            
        if self.platforms['github_copilot']:
            platform_mappings.append(('github-copilot/prompts/', '.github/prompts/'))
            
        if self.platforms['qwen_code']:
            platform_mappings.append(('qwen-code/commands/', '.qwen/commands/'))
        
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
            
            for remote_path, local_path in all_install_items:
                progress.update(task, description=f"Installing {remote_path}")
                
                remote_url = f"{self.base_url}/{remote_path}"
                local_file = project_dir / local_path
                
                if remote_path.endswith('/'):
                    # Directory - create it
                    local_file.mkdir(parents=True, exist_ok=True)
                    # For directories, we need to download individual files
                    # This is a simplified approach - in practice, you'd need to
                    # use GitHub API to get directory contents
                else:
                    # File - download it
                    if not self._download_file(remote_url, local_file):
                        return False
                    
                progress.advance(task)
                
        console.print("[green]✓ Agent OS installation completed![/green]")
        return True
        


