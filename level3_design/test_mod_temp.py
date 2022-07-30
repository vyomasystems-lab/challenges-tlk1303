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
        block1 = (int(inp[0:8],2), int(inp[8:16],2), int(inp[16:24],2), int(inp[24:32],2))
        block2 = (int(inp[32:40],2), int(inp[40:48],2), int(inp[48:56],2), int(inp[56:64],2))
        block3 = (int(inp[64:72],2), int(inp[72:80],2), int(inp[80:88],2), int(inp[88:96],2))
        block4 = (int(inp[96:104],2), int(inp[104:112],2), int(inp[112:120],2), int(inp[120:128],2))
       
        
        out1 = A.mixcolumns(block1)
        out2 = A.mixcolumns(block2)
        out3 = A.mixcolumns(block3)
        out4 = A.mixcolumns(block4)
        
        out1 = [bin(out1[0])[2:].zfill(32), bin(out1[1])[2:].zfill(32), bin(out1[2])[2:].zfill(32), bin(out1[3])[2:].zfill(32)]
                     
        await FallingEdge(dut.clk)  
        dut_out = bin(dut.data_out.value)[2:].zfill(128)
        print(dut_out[0:32])
        print(out1)
        print(dut_out[32:64])
        print(out2)

        
        #print(dut.data_in.value)
        
        cocotb.log.info(f'Input = {dut.data_in.value}, DUT Output = {dut.valid_out.value},{dut_out}, Expected = {out1}')            
        assert dut_out[0:32] == out1[0] and dut_out[32:64] == out1[1] and dut_out[64:96] == out1[2] and dut_out[96:128] == out1[3] , "Random test failed with input: {A}, and output: {B}, Expected ouput = {C}".format(
            A=inp,B=dut_out,C=out1)
        
        #await FallingEdge(dut.clk)
        
