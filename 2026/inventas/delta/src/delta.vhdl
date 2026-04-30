library IEEE;
  use IEEE.std_logic_1164.all;

entity delta is
  port(
    a : in std_ulogic;
    c : out std_ulogic
  );
end entity delta;

architecture dataflow of delta is 
  signal b : std_ulogic;
begin 
  b <= not a;
  c <= b and a;
end architecture;
