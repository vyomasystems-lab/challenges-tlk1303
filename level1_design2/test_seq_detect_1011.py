# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

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

    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  
    dut.inp_bit.value = 0
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  

    assert dut.seq_seen.value == 1, "Random test failed with input sequence: {A}, and output: {B}, Expected ouput = 1".format(
                        A = [1,0,1,1], B = dut.seq_seen.value)
    cocotb.log.info(f'Input sequence = 1011, Expected output = 1, DUT Output = {dut.seq_seen.value}')  

    #reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  
    dut.inp_bit.value = 0
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  

    assert dut.seq_seen.value == 1, "Random test failed with input sequence: {A}, and output: {B}, Expected ouput = 1".format(
                        A = [1,0,1,1], B = dut.seq_seen.value)
    cocotb.log.info(f'Input sequence = 1011, Expected output = 1, DUT Output = {dut.seq_seen.value}')  

    #reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  
    dut.inp_bit.value = 0
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)  

    assert dut.seq_seen.value == 1, "Random test failed with input sequence: {A}, and output: {B}, Expected ouput = 1".format(
                        A = [1,0,1,1], B = dut.seq_seen.value)
    cocotb.log.info(f'Input sequence = 1011, Expected output = 1, DUT Output = {dut.seq_seen.value}')  

    

        
