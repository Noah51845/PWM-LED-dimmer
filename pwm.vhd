library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pwm is
  generic (
    WIDTH : integer := 8  -- resolution in bits (0..2^WIDTH-1)
  );
  port (
    clk     : in  std_logic;
    rst_n   : in  std_logic; -- active low synchronous reset
    duty    : in  unsigned(WIDTH-1 downto 0); -- duty value (0..2^WIDTH-1)
    pwm_out : out std_logic
  );
end entity pwm;

architecture rtl of pwm is
  signal counter : unsigned(WIDTH-1 downto 0) := (others => '0');
begin

  -- synchronous counter
  proc_clk: process(clk)
  begin
    if rising_edge(clk) then
      if rst_n = '0' then
        counter <= (others => '0');
      else
        counter <= counter + 1;
      end if;
    end if;
  end process proc_clk;

  -- compare for PWM output
  pwm_out <= '1' when counter < duty else '0';

end architecture rtl;

