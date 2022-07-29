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

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)  
    
    dut.valid_in.value = 1

    dut.data_in.value = 2**128-1
    AES A;
    
    expected_out = A.mixcolumns(2**128-1)
    

    
                    
    #assert dut.seq_seen.value == 1, "Random test failed with input sequence: {A}, and output: {B}, Expected ouput = 1".format(
    
    cocotb.log.info(f'Input sequence = {dut.data_in.value}, Expected output = {expected_out}, DUT Output = {dut.valid_out.value},{dut.data_out.value}')
                                   
                
    #Reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0

        
