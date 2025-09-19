# Create Python TestBench Device - Implementation Workflow

This instruction provides the complete workflow for creating a Python testbench device in the SRV-PM project.

## Overview

<objective>
Create a complete Python testbench device implementation that integrates with the SRV-PM build system and provides firmware validation capabilities.
</objective>

<requirements>
- Python Device Modeling Framework
- OSAL source with target IP definition
- confclass library access
- SRV-PM build environment
</requirements>

## Mandatory Parameter Validation

**CRITICAL**: Before proceeding with any implementation steps, validate that ALL THREE mandatory parameters are provided:

<parameter_validation>
### Required Parameters (ALL MANDATORY)

1. **OSAL SOURCE**: Must be provided in one of three formats:
   - **Tarball name**: "dmr_imh_1p0ab_tpmiww15.osal.tgz" (existing or new in download-data.cmake)
   - **Artifactory URL**: Full download URL for OSAL tarball
   - **Directory path**: "dmr_imh_fv/" (existing extracted OSAL)

2. **IP NAME**: Target IP name within the OSAL structure (e.g., "dmr_imh", "psf20_dmrpc5psf123_psf0")
   
   **How to discover IP names in your OSAL:**
   ```bash
   # Command to list all available IPs in the OSAL
   python3.11.1 scripts/osalgen.py ./linux64/snapshots/onesource/dmr/a0/dmr_imh_fv print-ip-list > ip_list.txt
   
   # Then check the generated file for available IP names
   cat ip_list.txt
   ```
   
   **CRITICAL - AI Agent Behavior Rules:**
   - ✅ **USE EXACTLY**: Whatever IP name the user provides - do NOT modify it
   - ❌ **NEVER MODIFY**: Do NOT add, remove, or change any characters in user-provided IP names
   - ❌ **COMMON MISTAKE**: Do NOT automatically append `[0]` or other array notation
   - **RULE**: If user provides `"dmr_imh"` → use `"dmr_imh"` 
   - **RULE**: If user provides `"psf0[0]"` → use `"psf0[0]"` (if that's what they specified)
   - **AI RESPONSIBILITY**: Use the EXACT string the user provided, validate it exists in OSAL as-is

3. **MODULE NAME**: Target module/build name (e.g., "srv-pm-tb-devices", "imh-py-tb-dev")

### Validation Logic

**IF any parameter is missing:**
- **STOP** the workflow immediately
- **REQUEST** the missing parameter(s) from the user with clear explanation
- **EXPLAIN** why each parameter is required for the workflow
- **DO NOT PROCEED** until all three parameters are provided
- **VALIDATE** parameter format and accessibility before continuing

**ONLY proceed to Implementation Steps after confirming all three parameters are provided and valid.**
</parameter_validation>

## Implementation Steps

### Step 1: Project Preparation

<pre_flight>
- Verify SRV-PM environment setup
- Confirm OSAL access and IP name
- Check Python Device Modeling Framework availability
- Validate build system prerequisites
</pre_flight>

### Step 2: OSAL Analysis and Preparation

<osal_analysis>
**Input**: OSAL directory path and IP name
**Process**:
1. Extract OSAL to working directory
2. Identify register banks in target IP
3. Analyze register structure and dependencies
4. Plan register bank renames if needed

**Output**: OSAL directory ready for osalgen processing
</osal_analysis>

### Step 3: CMake Configuration

<cmake_setup>
**Configure**: srv-pm.cmake with osalgen integration
```cmake
include(${CMAKE_CURRENT_LIST_DIR}/osalgen-pydev.cmake)

_osalgen_pydev(
    "${osal_path}"
    "${ip_name}"
    "${module_name}"
    osal_renames "${rename_mappings}"
)
```

**Action Items**:
- Add osalgen-pydev.cmake inclusion
- Configure _osalgen_pydev() call with parameters
- Set up register bank renaming if required
- Verify CMake variable assignments

**CMake Execution**:
```bash
# Trigger CMake to process the configuration and generate register classes
cd srv-pm/ && cmake --preset release && ninja -C bt/release auto-gen-pydevs
```
</cmake_setup>

### Step 4: Python Register Generation

<register_generation>
**Process**: Execute CMake to generate Python register classes
**Expected Output**:
- `auto/` directory with generated Python modules
- Register class definitions matching OSAL structure
- Import statements for device implementation

**Validation**:
- Verify all expected register banks generated
- Check register field definitions
- Confirm import structure correctness
</register_generation>

### Step 5: Device Class Implementation

<device_implementation>
**Create**: `tb_<device_name>.py` with confclass structure

```python
from simmod.py_bank_lib.libconfclass import confclass
from .auto import <generated_module>

class tb_<device_name>Customization:
    cls = confclass('tb_<device_name>', parent=<generated_module>.RegClsGenerator('tb_<device_name>'))
    
    # Custom attributes
    cls.attr.custom_attribute("enable_logging", default=False, doc="Enable device logging")
    
    # Register bank access
    <register_bank> = cls.bank.<register_bank>
    
    # Side effect implementations
    @<register_bank>.reg.<REGISTER_NAME>.writer
    def write_<register_name>(self, value):
        # Implement side effect logic
        self.bank.<register_bank>.reg.<REGISTER_NAME>.set(value)
        # Additional side effect processing
```

**Implementation Requirements**:
- Import generated register module
- Define confclass with proper inheritance
- Implement required side effects using decorators
- Add custom attributes for device behavior
- Handle error conditions and validation
</device_implementation>

### Step 6: Build System Integration

<build_integration>
**Update CMakeLists.txt**:
```cmake
set(PYTHON_FILES
    module_load.py
    tb_<device_name>.py
    ${GENERATED_PY_REG_FILES}
)

simics_add_module(<module_name>
    CLASSES
        tb_<device_name>
)
```

**Update module_load.py**:
```python
from .tb_<device_name> import tb_<device_name>Customization
```

**Update module.list**:
```
@py-file tb_<device_name>.py
```
</build_integration>

### Step 7: Die Component Integration

<component_integration>
**Locate Target Die Component**: Find die component file (e.g., dmr_standalone_comp.py)

**Add Device to Configuration**:
```python
_dev_classnames = [
    # ... existing devices
    "tb_<device_name>",
]
```

**Configure Device Parameters**:
- Set device-specific configuration
- Establish register mapping
- Configure sideband connections if needed
</component_integration>

### Step 8: Testing and Validation

<validation_process>
**Build Verification**:
1. **Execute CMake configuration**: Refer to "CMake Execution" in Step 3
2. **Build module and verify compilation**:
   ```bash
   cd srv-pm && cmake --preset release && ninja -c bt/release <module_name>
   ```
3. **Check device registration in Simics**:
   ```bash
   # Run Simics commands in Simics batch mode
   cd srv-pm/ && ./simics --batch-mode -e "load-module <module_name>"
   ```

**Complete Validation Example** (bank and port access, and attribute validation):
```bash
cd srv-pm && ./bin/simics --batch-mode \
  -e 'load-module srv-pm-tb-devices' \
  -e '@import simics' \
  -e '@dev = simics.SIM_create_object("tb_pmusvid", "test_pmusvid", [])' \
  -e '@print("✅ Device register banks available:")' \
  -e '@print("  DVP bank:", hasattr(dev.bank, "_ami_pmusvid0_dvp_regs_dvp_legacy_vrc_legacy_vrc_addrmap"))' \
  -e '@print("  PMSB bank:", hasattr(dev.bank, "sb_cr_pmsb"))' \
  -e '@print("  Memory bank:", hasattr(dev.bank, "sb_mem"))' \
  -e '@print("✅ SVID ports available:")' \
  -e '@print("  GPSB port:", hasattr(dev.port, "gpsb"))' \
  -e '@print("  PMSB port:", hasattr(dev.port, "pmsb"))' \
  -e 'print-device-reg-info register = test_pmusvid.bank.sb_mem.DVP_STATUS' \
  -e 'quit'
```

**Functional Testing**:
1. **Create test scenarios for register access**: Use the Simics command examples from the "Complete Validation Example" above, including:
   - `print-device-reg-info register = test_pmusvid.bank.sb_mem.DVP_STATUS`
   - Test register bank accessibility and register field information
2. Validate side effect implementations
3. Test integration with firmware flows
4. Verify error handling

**Documentation**:
1. Document device purpose and usage
2. Create configuration examples
3. Add troubleshooting notes
</validation_process>

### Step 9: Version Control Integration

<git_integration>
**Generated File Management**:
After successful device creation and validation, the main generated file needs to be added to version control.

**User Confirmation Process**:
1. **Identify Generated File**: The primary device file `tb_<device_name>.py` created in Step 5
2. **Ask User Permission**: 
   ```
   "The Python testbench device file tb_<device_name>.py has been successfully generated.
   Would you like to add this file to git version control? (y/n)"
   ```
3. **Execute if Confirmed**:
   ```bash
   git add tb_<device_name>.py
   ```
4. **Inform User**: Provide status of the git add operation and suggest next steps for committing

**Important Notes**:
- Only add the main device file, not auto-generated register classes (those are build artifacts)
- Always ask for user permission before executing git commands
- Provide clear feedback about what was added to git staging
</git_integration>

## Quality Assurance

<qa_checklist>
- [ ] OSAL extraction and analysis complete
- [ ] CMake configuration properly set up
- [ ] Python register classes generated successfully
- [ ] Device class implements required functionality
- [ ] Build system integration verified
- [ ] Die component integration complete
- [ ] Functional testing passed
- [ ] Documentation created
</qa_checklist>

## Troubleshooting

<common_issues>
**Issue**: Register generation fails
**Solution**: Verify OSAL path and IP name correctness

**Issue**: Build compilation errors
**Solution**: Check Python import statements and class names

**Issue**: Device not registered in Simics
**Solution**: Verify module.list and CMakeLists.txt configuration

**Issue**: Side effects not working
**Solution**: Check decorator syntax and register bank references
</common_issues>

<support_resources>
- Reference implementation: tb_dda.py
- Architecture guide: srv-pm/promark/team_portal/arch_bkm/00_vp_arch/python_tb_device_guide.mmd
- Build system documentation: srv-pm build guide
- confclass library documentation
</support_resources>