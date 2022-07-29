import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge
from AES_model import *

@cocotb.test()
async def test_seq_bug1(dut):
    
    dut.valid_in.value = 0
    clock = Clock(dut.clk, 1, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk) 
    dut.reset.value = 1 
    A = AES()
    
    dut.valid_in.value = 1
    for i in range(1):   #2**10):
        inp = random.randint(0, 2**128)
        dut.data_in.value = inp
        
        inp = bin(inp)
        
        inp = inp[2:]
        block = (int(inp[0:32],2), int(inp[32:64],2), int(inp[64:96],2), int(inp[96:128],2))
       
        
        out1 = A.mixcolumns(block)
        out1 = [bin(out1[0])[2:].zfill(32), bin(out1[1])[2:].zfill(32), bin(out1[2])[2:].zfill(32), bin(out1[3])[2:].zfill(32)]
                     
        await FallingEdge(dut.clk)  
        dut_out = bin(dut.data_out.value)[2:].zfill(128)
        print(dut_out[0:32])
        print(out1[3])
        print(dut_out[32:64])
        print(out1[2])

        
        #print(dut.data_in.value)
        
        cocotb.log.info(f'Input = {dut.data_in.value}, DUT Output = {dut.valid_out.value},{dut_out}, Expected = {out1}')            
        assert dut_out[0:32] == out1[0] and dut_out[32:64] == out1[1] and dut_out[64:96] == out1[2] and dut_out[96:128] == out1[3] , "Random test failed with input: {A}, and output: {B}, Expected ouput = {C}".format(
            A=inp,B=dut_out,C=out1)
        
        #await FallingEdge(dut.clk)
        