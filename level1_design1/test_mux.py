# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    s=0;
    dut.sel.value=s;
    ival=[0]*31
    ival[0]=1  
    dut.inp0.value=ival[0]
    dut.inp1.value=ival[1]
    dut.inp2.value=ival[2]
    dut.inp3.value=ival[3]
    dut.inp4.value=ival[4]
    dut.inp5.value=ival[5]
    dut.inp6.value=ival[6]
    dut.inp7.value=ival[7]
    dut.inp8.value=ival[8] 
    dut.inp9.value=ival[9]
    dut.inp10.value=ival[10]
    dut.inp11.value=ival[11]
    dut.inp12.value=ival[12]
    dut.inp13.value=ival[13]
    dut.inp14.value=ival[14]
    dut.inp15.value=ival[15]
    dut.inp16.value=ival[16]
    dut.inp17.value=ival[17]
    dut.inp18.value=ival[18]
    dut.inp19.value=ival[19]
    dut.inp20.value=ival[20]
    dut.inp21.value=ival[21]
    dut.inp22.value=ival[22]
    dut.inp23.value=ival[23]
    dut.inp24.value=ival[24]
    dut.inp25.value=ival[25]
    dut.inp26.value=ival[26]
    dut.inp27.value=ival[27]
    dut.inp28.value=ival[28]
    dut.inp29.value=ival[29]
    dut.inp30.value=ival[30]
    
    
    await Timer(2, units='ns')


    cocotb.log.info(f'sel={s:05} model={ival[s]:01} DUT={int(dut.out.value):01}')
