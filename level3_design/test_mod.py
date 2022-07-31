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
    for i in range(2**10):
        inp = random.randint(0, 2**128)
        dut.data_in.value = inp
        
        inp = bin(inp)
        
        inp = inp[2:]
        
        inp = int(inp,2)
        block = [inp >> 96, inp >> 64 & 0xffffffff, inp >> 32 & 0xffffffff, inp & 0xffffffff]
        
        out1 = A.mixcolumns(block)
        out1 = [bin(out1[0])[2:].zfill(32), bin(out1[1])[2:].zfill(32), bin(out1[2])[2:].zfill(32), bin(out1[3])[2:].zfill(32)]
                     
        await FallingEdge(dut.clk)  
        dut_out = bin(dut.data_out.value)[2:].zfill(128)
              
               
        cocotb.log.info(f'Input = {dut.data_in.value}, DUT Output = {dut.valid_out.value},{dut_out}, Expected = {out1[0]}{out1[1]}{out1[2]}{out1[3]}')            
        assert dut_out[0:32] == out1[0] , "Random test failed with input: {A}, and output: {B}, Expected ouput = {C} in Word = 1".format(
            A=inp,B=dut_out[0:32],C=out1[0])
        assert dut_out[32:64] == out1[1] , "Random test failed with input: {A}, and output: {B}, Expected ouput = {C} in Word = 2".format(
            A=inp,B=dut_out[32:64],C=out1[1])
        assert dut_out[64:96] == out1[2] , "Random test failed with input: {A}, and output: {B}, Expected ouput = {C} in Word = 3".format(
            A=inp,B=dut_out[64:96],C=out1[2])
        assert dut_out[96:128] == out1[3] , "Random test failed with input: {A}, and output: {B}, Expected ouput = {C} in Word = 4".format(
            A=inp,B=dut_out[96:128],C=out1[3])
        
        
        