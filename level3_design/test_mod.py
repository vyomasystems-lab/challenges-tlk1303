import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge
from AES_model import *

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """
    dut.valid_in.value = 0
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk) 
    dut.reset.value = 1 
    
    dut.valid_in.value = 1

    dut.data_in.value = 2**128-1
    A = AES()
    inp = bin(2**128-1)
    
    inp = inp[2:]
    block = (int(inp[:32],2), int(inp[32:64],2), int(inp[64:96],2), int(inp[96:128],2))
    print(block)
    
    out1 = A.mixcolumns(block)
    out1 = [bin(out1[0])[2:], bin(out1[1])[2:], bin(out1[2])[2:], bin(out1[3])[2:]]
    out1[0] = str(out1[0])
    out1[1] = str(out1[1])
    out1[2] = str(out1[2])
    out1[3] = str(out1[3])

    expected_out = ""
    for i in out1:
        
        expected_out +=i
    
    expected_out = int(expected_out)

    await FallingEdge(dut.clk)  
    #await FallingEdge(dut.clk) 
    #await FallingEdge(dut.clk)  
    #await FallingEdge(dut.clk)  
 

    
                    
    #assert dut.seq_seen.value == 1, "Random test failed with input sequence: {A}, and output: {B}, Expected ouput = 1".format(
    
    cocotb.log.info(f'Input sequence = {dut.data_in.value}, Expected output = {expected_out}, DUT Output = {dut.valid_out.value},{dut.data_out.value}')
                                   
                
   
    

        
