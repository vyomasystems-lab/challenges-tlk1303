# Level1_Design1 MUX Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![](seq_ss.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. 

The test drives inputs to the Design Under Test (sequence detector module - seq_detect_1011.v) which takes a Clock, Reset and Input bit signal as its inputs. The Design Under Test(DUT) drives an output *seq_seen* whenever the sequence *1011* is detected. The Sequence detection should includes overlapping sequences of *1011*.

The Minimum constraint the DUT has to satisfy is, to detect the sequence *1011*. The Maximum constraint for sequence detector is, to detect the two overlapped sequence *1011011*. Therfore by checking the output for all possible 7-bit sequence the Design can be verified for all possible input sequences. The Test starts with a constraint input sequence and verifies the output. Then a radomized 7-bit sequence is applied to the input of DUT and its output is verified. The randomized input is applied for an appropriate number of times to cover all possible cases(2^7 = 128).

The Clock Input is driven using the cocotb.clock module whose period is specified by the following statements,
```
clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
cocotb.start_soon(clock.start())        # Start the clock
```

The DUT is reset to its *IDLE* state before driving the input sequence. This is done by the stimulating the reset signal as given below,
```
dut.reset.value = 1
await FallingEdge(dut.clk)  
dut.reset.value = 0
await FallingEdge(dut.clk)
```
To Reset the sequence detector the Reset signal value is set *HIGH* till a falling edge of the clock is seen. Then the Reset signal is set to *LOW*, and the test waits for the next falling edge before proceeding with the test.

The Input sequence is stored in a list inp and driven to the *inp_bit* for a Clock period between two falling edges of the clock.
```
dut.inp_bit.value = inp[j]
await FallingEdge(dut.clk)
```
Before the next input sequence is applied the sequence detector is reset by using the following reset signal,
```
dut.reset.value = 1
await FallingEdge(dut.clk)  
dut.reset.value = 0
```

The assert statement is used for comparing the mux's output to the expected value.

The following error is seen:
```
assert dut.out.value == ival[i], "Test failed with: {S} {Ival} != {Out}".format(Ival=ival[i], S=dut.sel.value, Out=dut.out.value)
                     AssertionError: Test failed with: 01100 1 != 00
```
## Test Scenario-1 
- Test Inputs: inp12=1 sel=12
- Expected Output: out=1
- Observed Output in the DUT dut.out=0

Output mismatches for the above inputs as inp12 is 1 and when sel is 12 expected output is the value in inp12. 
Therefore this proves that there is a design bug

## Design Bug-1
Based on the above test input and analysing the design, we see the following

```
 begin
    case(sel)
    5'b01101: out = inp12;           ====> BUG
    5'b01101: out = inp13;
    endcase
  end

```
For a proper mux design, the case should be ``5'b01100: out = inp12`` instead of ``5'b01101: out = inp12`` as in the design code. This statement connects inp12 to out when ``sel = 13``, and there is no case for ``sel=12``. Therefore the output comes from a default case.

## Design Fix-1
The design fix here must include a case where ``sel=12`` and connect inp12 to out when ``sel=12``.
```
5'b01100: out = inp12;
```

Updating the design and re-running the test makes the test pass for this case.

```
770.00ns INFO     sel=00012 model=1 DUT=1
```



Then The second error is seen:
```
assert dut.out.value == ival[i], "Test failed with: {S} {Ival} != {Out}".format(Ival=ival[i], S=dut.sel.value, Out=dut.out.value)
                     AssertionError: Test failed with: 11110 1 != 00
```
## Test Scenario-2
- Test Inputs: inp30=1 sel=30
- Expected Output: out=1
- Observed Output in the DUT dut.out=0

Output mismatches for the above inputs as inp30 is 1 and when sel is 30 expected output is the value in inp30. 
Therefore this proves that there is a design bug

## Design Bug-2
Based on the above test input and analysing the design, we see the following

```
 begin
    case(sel)
    5'b11101: out = inp29;   ====> BUG
    default: out = 0;
    endcase
  end

```
The given mux design does not have a case for ``sel=30`` that is ``sel=5'b11110``. Therefore the mux design gives a default case output of 0 while the expected output for ``sel=30`` is 1.

## Design Fix-2
The design fix here must include a case where ``sel=30`` and connect inp30 to out when ``sel=30``.
```
5'b11110: out = inp30;
```

Updating the design and re-running the test makes the test pass for this case.

![](result1_screenshot.png)


## Verification Strategy
  The Verification strategy followed was to stimulate a single input line to logic HIGH and keep all other input lines at logic LOW. At the same time each input line was selected one after the other by using the select line. The corresponding observed outputs were checked against the expected output and mismatches were logged. 

## Is the verification complete ?
  The Verification for the given mux is complete and the design bugs were identified and fixed. The fixed design has passed all the test cases.
