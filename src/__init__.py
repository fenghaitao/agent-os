"""
Agent OS - A comprehensive product development workflow management system.

Agent OS provides structured development workflows for AI coding platforms including
Claude Code, Cursor, GitHub Copilot, and Qwen Code.
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Agent OS Team"
__email__ = "agent-os@example.com"

from .installer import AgentOsInstaller
from .cli import main as cli_main

__all__ = [
    "AgentOsInstaller",
    "cli_main",
]
