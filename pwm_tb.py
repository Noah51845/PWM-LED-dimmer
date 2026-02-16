import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.result import TestFailure


@cocotb.test()
async def test_pwm_basic(dut):
    """Test basic PWM functionality"""
    # Create a clock signal
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset the module
    dut.rst.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 5)
    
    dut._log.info("Basic reset test completed")


@cocotb.test()
async def test_pwm_duty_cycle(dut):
    """Test PWM duty cycle variation"""
    # Create a clock signal
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset the module
    dut.rst.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 5)
    
    # Set duty cycle to 50%
    dut.duty.value = 128  # Assuming 8-bit duty cycle (256 max)
    await ClockCycles(dut.clk, 100)
    
    dut._log.info("Duty cycle test completed")


@cocotb.test()
async def test_pwm_frequency(dut):
    """Test PWM frequency and period"""
    # Create a clock signal
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset the module
    dut.rst.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 5)
    
    # Monitor PWM output for one complete period
    pwm_high_time = 0
    pwm_low_time = 0
    
    # Wait for PWM signal to stabilize
    await ClockCycles(dut.clk, 50)
    
    # Count high and low times
    for _ in range(256):
        if dut.pwm_out.value == 1:
            pwm_high_time += 1
        else:
            pwm_low_time += 1
        await RisingEdge(dut.clk)
    
    dut._log.info(f"PWM High Time: {pwm_high_time}, Low Time: {pwm_low_time}")
