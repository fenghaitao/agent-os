# Create Python TestBench Device

Create a new Python testbench device for the SRV-PM project using the Python Device Modeling Framework.

## Usage
```bash
create-py-tb-device <osal_source> <ip_name> <module_name>
```

### Required Parameters (ALL MANDATORY)
- `osal_source`: OSAL source (tarball name, URL, or directory path)
- `ip_name`: IP name in OSAL (e.g., "psf20_dmrpc5psf123_psf0")  
- `module_name`: Target module name (e.g., "srv-pm-tb-devices")

## Implementation Workflow
Refer to the complete implementation instructions:
@.pmssbot/instructions/core/create-py-tb-device.md