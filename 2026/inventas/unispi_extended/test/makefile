# Makefile

# Simulator and language selection
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# GHDL specific arguments: VHDL 2008
EXTRA_ARGS +=--std=08

# Specify timestep to get correct timescale in waveform
COCOTB_HDL_TIMEPRECISION = 1fs

# TOPLEVEL is the name of the toplevel module in your VHDL file
TOPLEVEL ?= unispi

# Optional: Specify toplevel architecture when there more than one available
# ARCH = <architecture name in your VHDL file>

#VHDL_SOURCES += $(PWD)/../src/$(TOPLEVEL).vhd
VHDL_SOURCES += $(PWD)/../src/*.vhd*

# SIM_ARGS is Simulation arguments. --wave determines name and type of waveform  
SIM_ARGS +=--wave=$(TOPLEVEL).ghw

# -g<GENERIC> is used to set generics defined in the toplevel entity
SIM_ARGS +=-gbyte=8

# MODULE is the basename of the Python test file
COCOTB_TEST_MODULES = tb_$(TOPLEVEL)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# removing generated binary of top entity and .o-file on make clean
clean::
	-@rm -rf __pycache__
	-@rm -rf sim_build/
