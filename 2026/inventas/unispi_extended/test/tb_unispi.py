# Testbench for unispi
import cocotb
from cocotb import start_soon
from cocotb.triggers import ClockCycles, Combine, ReadOnly
from cocotb.utils import get_sim_time   
from cocotb.clock import Clock
from cocotb.queue import Queue 

import random 
from random import randrange

A_patterns =  (
            (0x01, 0x02, 0x03),
            (0x11, 0x12, 0x13),
            (0x21, 0x22, 0x23),
            (0xA1, 0xB2, 0xC3),
            (0xD1, 0xE2, 0xF3)
         )

B_patterns = (
            (0x21, 0x22),
            (0x2F, 0x2E),
            (0xE2, 0xF2)
         )
         
C_patterns = (
            (0x31, 0x32, 0x33, 0x34, 0x35),
            (0x3F, 0x3E, 0x3D, 0x3C, 0x3B),
            (0xB3, 0xC3, 0xD3, 0xE3, 0xF3),
            (0x31, 0x32, 0x33, 0x34, 0x35)
         )         

async def reset(dut):
    dut.intA.value = 0
    dut.intB.value = 0
    dut.intC.value = 0
    dut.sin.value = 0
    dut.reset.value = 1
    await ClockCycles(dut.clk, 2)
    dut.reset.value = 0
    await ClockCycles(dut.clk, 1)
        
async def set_byte(dut, byte):
    """Sends one byte serially and stores each bit in the process"""
    for i in range(8):
        await dut.SCK.falling_edge
        bit = (byte>>(7-i)) & 1
        dut.sin.value = bit  

async def stimuli(dut, ByteQ):
    taskA = start_soon(stimA(dut, ByteQ))
    taskB = start_soon(stimB(dut, ByteQ))
    taskC = start_soon(stimC(dut, ByteQ))
    #cocotb 2.1 shall use gather?: Keep this for future ref. I think Combine is fine 
    # await gather(taskA, taskB, taskC)
    # All three must complete but we do not know which comes first. 
    await Combine(taskA, taskB, taskC)

  
async def stimA(dut, ByteQ):
    for pattern in A_patterns:
        dut.intA.value = 1
        await dut.csA.rising_edge
        dut.intA.value = 0
        for byte in pattern: 
            ByteQ.put_nowait((byte, 1, pattern.index(byte)+1))
            await set_byte(dut, byte)
        await ClockCycles(dut.clk, randrange(5, 55, 10))

async def stimB(dut, ByteQ):
    for pattern in B_patterns:
        dut.intB.value = 1
        await dut.csB.rising_edge
        dut.intB.value = 0
        for byte in pattern: 
            ByteQ.put_nowait((byte, 2, pattern.index(byte)+1))
            await set_byte(dut, byte)
        await ClockCycles(dut.clk, randrange(7,77,10))

async def stimC(dut, ByteQ):
    for pattern in C_patterns:
        dut.intC.value = 1
        await dut.csC.rising_edge
        dut.intC.value = 0
        for byte in pattern: 
            ByteQ.put_nowait((byte, 3, pattern.index(byte)+1))
            await set_byte(dut, byte)
        await ClockCycles(dut.clk, randrange(3,33,3))
 
async def pattern_check(dut, ByteQ):
    while True:
        await dut.ready.rising_edge
        await ReadOnly()
        sentdata = ByteQ.get_nowait()
        sentvalue = sentdata[0]
        sent_id = sentdata[1]
        sent_byte = sentdata[2]
        received_id = int(dut.control.value)>>4
        received_byte  = int(dut.control.value) & 0x0F
        # Print statement may well be used to create a log file
        print(f"S/R: value: {sentvalue:3d}, {int(dut.data.value):3d}, \
            id = {int(sent_id)}, {int(received_id) } \
            byte# = {sent_byte}, {int(received_byte)}") 
        assert dut.data.value == sentvalue, f"Ready flagged, data != input pattern"
        assert received_id == sent_id, f"Sent ID != received id"
        assert received_byte == sent_byte, f"Sent byte count != received byte count"
        
async def off_check(dut):
    while True:
        await dut.ready.falling_edge
        await ReadOnly()
        assert dut.data.value == 0, f"Data nonzero after ready has been removed"
        assert dut.control.value == 0, f"Control nonzero after ready has been removed"
 
async def monitor(dut, ByteQ):
    start_soon(pattern_check(dut, ByteQ))
    start_soon(off_check(dut))
        
@cocotb.test()
async def main_test(dut):
    """ Starts comparator and stimuli """
    dut._log.info("Starting clock...")
    start_soon(Clock(dut.clk, 10, unit='ns').start())
    dut._log.info("Resetting...")
    await reset(dut)
    
    ByteQ = Queue()
    dut._log.info("Starting checks...")
    start_soon(monitor(dut, ByteQ))
    dut._log.info("Starting stimuli...")
    await stimuli(dut, ByteQ)
      
    dut._log.info("test done!")
