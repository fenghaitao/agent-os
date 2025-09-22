# Makefile for Simics Watchdog Device Model
#
# This Makefile builds the watchdog device model for the Simics simulator
# using the Device Modeling Language (DML) compiler.

# Simics installation path - modify as needed
SIMICS_BASE ?= /opt/simics-6.0

# Compiler and tools
DML_COMPILER = $(SIMICS_BASE)/bin/dml-compile
SIMICS_CC = $(SIMICS_BASE)/bin/simics-cc

# Source files
DML_SRC = watchdog.dml
MODULE_NAME = watchdog-device
TARGET = $(MODULE_NAME).so

# Build flags
DML_FLAGS = -Wall -Werror
CC_FLAGS = -O2 -g

# Default target
all: $(TARGET)

# Build the device module
$(TARGET): $(DML_SRC)
	@echo "Compiling watchdog device model..."
	$(DML_COMPILER) $(DML_FLAGS) -o $(TARGET) $(DML_SRC)
	@echo "Build complete: $(TARGET)"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -f $(TARGET)
	rm -f *.o *.so *.pyc
	rm -rf __pycache__
	@echo "Clean complete"

# Install to Simics modules directory
install: $(TARGET)
	@echo "Installing watchdog device module..."
	cp $(TARGET) $(SIMICS_BASE)/modules/
	@echo "Installation complete"

# Run basic syntax check
check: $(DML_SRC)
	@echo "Checking DML syntax..."
	$(DML_COMPILER) -c $(DML_SRC)
	@echo "Syntax check passed"

# Development targets
.PHONY: all clean install check

# Help target
help:
	@echo "Available targets:"
	@echo "  all     - Build the watchdog device module (default)"
	@echo "  clean   - Remove build artifacts"
	@echo "  install - Install module to Simics"
	@echo "  check   - Run syntax check only"
	@echo "  help    - Show this help message"
	@echo ""
	@echo "Environment variables:"
	@echo "  SIMICS_BASE - Path to Simics installation (default: /opt/simics-6.0)"