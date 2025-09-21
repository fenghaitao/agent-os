#!/usr/bin/env python3
"""
Validation tests for Simics integration functionality.
Tests the integration of Simics workflows with agent-os core system.
"""

import unittest
import os
import yaml
import tempfile
import shutil
from pathlib import Path

class TestSimicsIntegration(unittest.TestCase):
    """Test Simics integration with agent-os"""
    
    def setUp(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.agent_os_root = Path(__file__).parent.parent
        self.config_path = self.agent_os_root / "config.yml"
        
    def tearDown(self):
        """Cleanup test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
    def test_config_yml_simics_integration(self):
        """Test that config.yml contains proper Simics integration"""
        self.assertTrue(self.config_path.exists(), "config.yml not found")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Test project types exist
        self.assertIn('project_types', config)
        project_types = config['project_types']
        
        # Test Simics project types
        self.assertIn('simics-device', project_types)
        self.assertIn('simics-platform', project_types)
        self.assertIn('simics-simulation', project_types)
        
        # Test project type structure
        for project_type in ['simics-device', 'simics-platform', 'simics-simulation']:
            self.assertIn('instructions', project_types[project_type])
            self.assertIn('standards', project_types[project_type])
            
        # Test Simics configuration section
        self.assertIn('simics', config)
        simics_config = config['simics']
        self.assertIn('version', simics_config)
        self.assertIn('api_version', simics_config)
        self.assertIn('default_accuracy', simics_config)
        
    def test_simics_directory_structure(self):
        """Test that Simics directory structure exists"""
        simics_root = self.agent_os_root / "simics"
        self.assertTrue(simics_root.exists(), "Simics directory not found")
        
        # Test device instructions
        device_instructions = simics_root / "device-instructions"
        self.assertTrue(device_instructions.exists())
        self.assertTrue((device_instructions / "core").exists())
        self.assertTrue((device_instructions / "meta").exists())
        
        # Test platform instructions
        platform_instructions = simics_root / "platform-instructions"  
        self.assertTrue(platform_instructions.exists())
        self.assertTrue((platform_instructions / "core").exists())
        self.assertTrue((platform_instructions / "meta").exists())
        
        # Test simulation instructions
        simulation_instructions = simics_root / "simulation-instructions"
        self.assertTrue(simulation_instructions.exists())
        self.assertTrue((simulation_instructions / "core").exists())
        self.assertTrue((simulation_instructions / "meta").exists())
        
        # Test standards directories
        self.assertTrue((simics_root / "device-standards").exists())
        self.assertTrue((simics_root / "platform-standards").exists())
        self.assertTrue((simics_root / "simulation-standards").exists())
        
    def test_simics_commands_exist(self):
        """Test that Simics commands are properly created"""
        commands_dir = self.agent_os_root / "commands"
        
        # Test command files exist
        simics_commands = [
            "plan-simics-platform.md",
            "create-simics-device.md", 
            "analyze-simics-platform.md",
            "assemble-platform.md",
            "validate-platform.md",
            "model-device-interface.md"
        ]
        
        for command in simics_commands:
            command_path = commands_dir / command
            self.assertTrue(command_path.exists(), f"Command {command} not found")
            
            # Test command file format
            with open(command_path, 'r') as f:
                content = f.read()
                self.assertIn("# ", content)  # Has markdown header
                self.assertIn("@.agent-os/simics/", content)  # References Simics instructions
                
    def test_simics_instruction_files(self):
        """Test that Simics instruction files are properly created"""
        simics_root = self.agent_os_root / "simics"
        
        # Test core instruction files
        core_instructions = [
            ("device-instructions/core", "create-simics-device.md"),
            ("device-instructions/core", "model-device-interface.md"),
            ("platform-instructions/core", "plan-simics-platform.md"),
            ("platform-instructions/core", "assemble-platform.md"),
            ("platform-instructions/core", "validate-platform.md"),
            ("simulation-instructions/core", "simulation-testing.md")
        ]
        
        for instruction_dir, instruction_file in core_instructions:
            instruction_path = simics_root / instruction_dir / instruction_file
            self.assertTrue(instruction_path.exists(), 
                           f"Instruction {instruction_dir}/{instruction_file} not found")
            
            # Test instruction file format
            with open(instruction_path, 'r') as f:
                content = f.read()
                self.assertIn("---", content)  # Has YAML frontmatter
                self.assertIn("description:", content)  # Has description
                self.assertIn("process_flow", content)  # Has process flow
                
    def test_simics_meta_files(self):
        """Test that Simics meta instruction files exist"""
        simics_root = self.agent_os_root / "simics"
        
        # Test meta files
        meta_files = [
            "device-instructions/meta/pre-flight.md",
            "device-instructions/meta/post-flight.md",
            "platform-instructions/meta/pre-flight.md", 
            "platform-instructions/meta/post-flight.md",
            "simulation-instructions/meta/pre-flight.md",
            "simulation-instructions/meta/post-flight.md"
        ]
        
        for meta_file in meta_files:
            meta_path = simics_root / meta_file
            self.assertTrue(meta_path.exists(), f"Meta file {meta_file} not found")
            
    def test_simics_standards_files(self):
        """Test that Simics standards files exist"""
        simics_root = self.agent_os_root / "simics"
        
        # Test standards files
        standards_files = [
            "device-standards/device-development-standards.md",
            "platform-standards/platform-development-standards.md"
        ]
        
        for standards_file in standards_files:
            standards_path = simics_root / standards_file
            self.assertTrue(standards_path.exists(), f"Standards file {standards_file} not found")
            
    def test_simics_template_files(self):
        """Test that Simics template files exist"""
        simics_root = self.agent_os_root / "simics"
        
        # Test template files
        template_files = [
            "device-standards/device-model-template.md",
            "platform-standards/platform-assembly-template.md",
            "simulation-standards/simulation-testing-template.md"
        ]
        
        for template_file in template_files:
            template_path = simics_root / template_file
            self.assertTrue(template_path.exists(), f"Template file {template_file} not found")
            
            # Test template content
            with open(template_path, 'r') as f:
                content = f.read()
                self.assertIn("[", content)  # Has template variables
                self.assertIn("]", content)  # Has template variables
                
    def test_simics_documentation(self):
        """Test that Simics documentation exists"""
        doc_files = [
            self.agent_os_root / "SIMICS_INTEGRATION.md",
            self.agent_os_root / "simics" / "INTEGRATION_STATUS.md"
        ]
        
        for doc_file in doc_files:
            self.assertTrue(doc_file.exists(), f"Documentation file {doc_file} not found")
            
            # Test documentation content
            with open(doc_file, 'r') as f:
                content = f.read()
                self.assertIn("# ", content)  # Has markdown headers
                self.assertIn("Simics", content)  # Contains Simics content
                
    def test_simics_workflow_patterns(self):
        """Test that Simics workflows follow agent-os patterns"""
        simics_root = self.agent_os_root / "simics"
        
        # Test device workflow pattern
        device_create_instruction = simics_root / "device-instructions/core/create-simics-device.md"
        with open(device_create_instruction, 'r') as f:
            content = f.read()
            
        # Should follow agent-os patterns
        self.assertIn("subagent", content.lower())  # Uses subagents
        self.assertIn("context-fetcher", content)  # Uses context-fetcher
        self.assertIn("file-creator", content)  # Uses file-creator  
        self.assertIn("date-checker", content)  # Uses date-checker
        self.assertIn("pre_flight_check", content)  # Has pre-flight checks
        self.assertIn("post_flight_check", content)  # Has post-flight checks
        
    def test_integration_completeness(self):
        """Test that integration is complete and functional"""
        # Test all major components exist
        simics_root = self.agent_os_root / "simics"
        
        required_components = [
            # Configuration
            (self.agent_os_root / "config.yml", "Configuration file"),
            
            # Commands
            (self.agent_os_root / "commands/plan-simics-platform.md", "Platform planning command"),
            (self.agent_os_root / "commands/create-simics-device.md", "Device creation command"),
            
            # Instructions
            (simics_root / "device-instructions/core/create-simics-device.md", "Device creation instruction"),
            (simics_root / "platform-instructions/core/plan-simics-platform.md", "Platform planning instruction"),
            
            # Standards
            (simics_root / "device-standards/device-development-standards.md", "Device standards"),
            (simics_root / "platform-standards/platform-development-standards.md", "Platform standards"),
            
            # Templates
            (simics_root / "device-standards/device-model-template.md", "Device template"),
            (simics_root / "platform-standards/platform-assembly-template.md", "Platform template"),
            
            # Documentation
            (self.agent_os_root / "SIMICS_INTEGRATION.md", "Integration documentation")
        ]
        
        for component_path, description in required_components:
            self.assertTrue(component_path.exists(), 
                           f"{description} not found at {component_path}")

class TestSimicsWorkflowIntegration(unittest.TestCase):
    """Test Simics workflow integration patterns"""
    
    def setUp(self):
        """Setup test environment"""
        self.agent_os_root = Path(__file__).parent.parent
        self.simics_root = self.agent_os_root / "simics"
        
    def test_instruction_file_format(self):
        """Test that instruction files follow proper format"""
        instruction_files = [
            self.simics_root / "device-instructions/core/create-simics-device.md",
            self.simics_root / "platform-instructions/core/plan-simics-platform.md"
        ]
        
        for instruction_file in instruction_files:
            with open(instruction_file, 'r') as f:
                content = f.read()
                
            # Test YAML frontmatter
            self.assertTrue(content.startswith("---"), 
                           f"{instruction_file} missing YAML frontmatter")
            
            # Test required frontmatter fields
            self.assertIn("description:", content)
            self.assertIn("version:", content)
            
            # Test process flow structure
            self.assertIn("process_flow", content)
            self.assertIn("step number=", content)
            
    def test_subagent_usage_patterns(self):
        """Test that subagent usage follows patterns"""
        instruction_file = self.simics_root / "device-instructions/core/create-simics-device.md"
        
        with open(instruction_file, 'r') as f:
            content = f.read()
            
        # Test subagent usage patterns
        self.assertIn('subagent="context-fetcher"', content)
        self.assertIn('subagent="file-creator"', content)
        self.assertIn('subagent="date-checker"', content)
        
        # Test step structure
        self.assertIn('step number="1"', content)
        self.assertIn('step number="2"', content)

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)