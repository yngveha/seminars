#--------------------------------------------------------------------------------------------------
# brief: 
#   This testbench demonstrates data being assigned and read using different timing methods in 
#   cosimulation with cocotb.
#  
#   - using Timer() 
#   - using ClockCycles()
#   - using .rising_edge
#   - using Timer + ReadOnly() 
#
#   The timer goes before clockcycles, which means stimuli applied using the timer will
#   be applied on events following clock-edges that occur at the same time. 
#
#   In real world application, we should expect results comparable to when data is applied after 
#   the clock edge has occured. 
#
#   Design rules for RTL testbenches: 
#   STIMULI: 
#      should be normally be applied after the clock edge (awaiting .rising_edge or ClockCycles(..))
#      Using the timer to set out data (as shown here) can camouflage or cause erronous behaviour
#   CHECKS:
#      should normally be performed after the event queue is resolved (awaiting ReadOnly)
#      regardless of what method was used to go to the timestep. 
#   DEBUGGING:
#      can make use of all methods, 
#      but there will be a lot less of it when applying the rules above from start ;^)
#   
# file: tb_timingtest.py
# author: Yngve Hafting
#--------------------------------------------------------------------------------------------------
# Copyright (c) 2026 by UIO – University of Oslo (www.uio.no)
#--------------------------------------------------------------------------------------------------
# File history:
#
# Version | Date       | Author             | Remarks
#--------------------------------------------------------------------------------------------------
# 1.0     | 24.02.2026 | Y. Hafting         | Created
#--------------------------------------------------------------------------------------------------

import cocotb
from cocotb import start_soon
from cocotb.utils import get_sim_time
from cocotb.triggers import ClockCycles, Timer, ReadOnly
from cocotb.clock import Clock

async def stimuli(dut):
    dut.a.value = 0
    print_status(dut.a.value, dut.x.value, "STIMULI: a=0, at simulation start")
    await ClockCycles(dut.clk, 1)   #  0ns
    print_status(dut.a.value, dut.x.value, "STIMULI: unchanged, awaited Clockcycles(dut.clk, 1) clk transitioned to '1' once: U>1")
    await dut.clk.rising_edge       # 10ns
    dut.a.value = 1
    print_status(dut.a.value, dut.x.value, "STIMULI: a=1, after awaiting rising_edge(clk)")
    await Timer(10, unit="ns")      # 20ns
    await dut.clk.rising_edge       # 20ns
    dut.a.value = 0
    print_status(dut.a.value, dut.x.value, "STIMULI: a=0 after awaiting +10ns using timer, then awaited rising_edge(clk)")
    await Timer(10, unit="ns")      # 30ns
    dut.a.value = 1
    print_status(dut.a.value, dut.x.value, "STIMULI: a=1 after awaiting +10 ns using timer")
    await Timer(10, unit="ns")      # 40ns
    dut.a.value = 0
    print_status(dut.a.value, dut.x.value, "STIMULI: a=0 after awaiting +10 ns using timer")
    await dut.clk.falling_edge      # 45ns Allow all checks to finish, without starting over.

def print_status(a,x,method):
    now = get_sim_time(unit='ns')
    print(f"{now:{9}.0f}ns  ",
          f"a: {a}  ", 
          f"x: {x}  ", 
          f"{method}")

async def timed_check(dut):     
    '''Awaiting timer, we intercept simulation before the event queue at that time has begun to resolve'''
    while True:
        await Timer(10, 'ns')
        print_status(dut.a.value, dut.x.value, "awaited Timer(10,'ns')");
  
async def cycle_check(dut):
    '''Cycle based triggers is based on edge triggering and is equivalent in terms of the event queue'''
    while True:
        await ClockCycles(dut.clk, 1)
        print_status(dut.a.value, dut.x.value, "awaited ClockCycles(dut.clk,1)");
        
async def edge_check(dut):
    '''Edge based triggers intercepts simulation at that event, whenever in the event queue that was'''
    while True: 
        await dut.clk.rising_edge
        print_status(dut.a.value, dut.x.value, "awaited rising_edge(dut.clk)");

async def settled_check(dut):
    '''Awaiting Readonly() the event queue at the current timeslot resolves =>
       Normal checks shall always be in the ReadOnly phase for this purpose.  
    '''
    while True: 
        await Timer(10, unit="ns")
        #await ClockCycles(dut.clk, 1)
        #await dut.clk.rising_edge
        await ReadOnly()
        print_status(dut.a.value, dut.x.value, "All settled; awaited Timer + ReadOnly()");

def run_checks(dut):
    start_soon(settled_check(dut)) 
    #start_soon(edge_check(dut))
    start_soon(cycle_check(dut))  # Cycle and edge checks are equivalent
    start_soon(edge_check(dut))   # Whichever goes first here comes first when printing. 
    start_soon(timed_check(dut))  
    
    
@cocotb.test()
async def main_test(dut):   
    """Try accessing the design."""
    dut._log.info("Running test...")
    dut._log.info("Starting clock at 100MHz")
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    run_checks(dut)
    await stimuli(dut)
    dut._log.info("Running test...done")
