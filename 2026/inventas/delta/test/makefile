# Makefile

# Simulator and language selection
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# GHDL specific arguments: VHDL 2008
EXTRA_ARGS +=--std=08

# Specify timestep to get correct timescale in waveform
COCOTB_HDL_TIMEPRECISION = 1fs

# TOPLEVEL is the name of the toplevel module in your VHDL file
TOPLEVEL ?= delta

# Optional: Specify toplevel architecture 
# ARCH = <architecture name in your VHDL file>

#VHDL_SOURCES += $(PWD)/../src/$(TOPLEVEL).vhd
VHDL_SOURCES += $(PWD)/../src/*.vhd*

# SIM_ARGS is Simulation arguments. --wave determines name and type of waveform  
SIM_ARGS +=--wave=$(TOPLEVEL).ghw

# -g<GENERIC> is used to set generics defined in the toplevel entity
#SIM_ARGS +=-gWIDTH=32

# COCOTB_TEST_MODULES is the basename of the Python test file(s)
COCOTB_TEST_MODULES ?= tb_$(TOPLEVEL)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# removing generated binaries
clean::
	-@rm -rf sim_build/
	-@rm -rf __pycache__
