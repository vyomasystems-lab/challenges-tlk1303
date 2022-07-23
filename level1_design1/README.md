# Level1_Design1 MUX Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![](screenshot.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mux module here) which takes in 31 inputs from inp0, inp1 to inp30, along with a 5-bit select input sel and gives an output *out*

The values are assigned to the input port using 
```
dut.sel.value   = 12
dut.inp12.value = 1
```

The assert statement is used for comparing the mux's output to the expected value.

The following error is seen:
```
assert dut.sum.value == A+B, "Adder result is incorrect: {A} + {B} != {SUM}, expected value={EXP}".format(
                     AssertionError: Adder result is incorrect: 7 + 5 != 2, expected value=12
```
## Test Scenario **(Important)**
- Test Inputs: a=7 b=5
- Expected Output: sum=12
- Observed Output in the DUT dut.sum=2

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
 always @(a or b) 
  begin
    sum = a - b;             ====> BUG
  end
```
For the adder design, the logic should be ``a + b`` instead of ``a - b`` as in the design code.

## Design Fix
Updating the design and re-running the test makes the test pass.

![](https://i.imgur.com/5XbL1ZH.png)

The updated design is checked in as adder_fix.v

## Verification Strategy

## Is the verification complete ?