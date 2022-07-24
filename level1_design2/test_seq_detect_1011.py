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

    for i in range(128):
        inp = [random.randint(0, 1),random.randint(0, 1),random.randint(0, 1),random.randint(0, 1),
                random.randint(0, 1),random.randint(0, 1),random.randint(0, 1)]
        
        for j in range(0,6):
            dut.inp_bit.value = inp[j]
            await FallingEdge(dut.clk)
        
            
            if(j >= 3):
                
                if(inp[j-3:j] == [1,0,1,1]):
                    assert dut.seq_seen.value == 1, "Random test failed with input sequence: {A}, and output: {B}".format(
                        A = inp[:j], B = dut.seq_seen.value
                    )
                    cocotb.log.info(f'Input sequence = {inp[:j]}, Expected output = 1, DUT Output = {dut.seq_seen.value}')
                else:
                    assert dut.seq_seen.value == 0, "Random test failed with input sequence: {A}, and output: {B}".format(
                        A = inp[:j], B = dut.seq_seen.value
                    )
                    cocotb.log.info(f'Input sequence = {inp[:j]}, Expected output = 0, DUT Output = {dut.seq_seen.value}')




        
