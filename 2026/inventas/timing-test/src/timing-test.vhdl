/*
----------------------------------------------------------------------------------------------------
-- brief: 
--  This file is intended for a test for timing methods in cocotb, see ../test folder
--  The VHDL is supposed to showcase simple flipflop behavior
--  
-- file: timing-test.vhdl
-- author: Yngve Hafting
----------------------------------------------------------------------------------------------------
-- Copyright (c) 2026 by UiO – University of Oslo (www.uio.no) 
-- This code is licensed under the MIT license if applicable
----------------------------------------------------------------------------------------------------
-- File history:
--
-- Version | Date       | Author             | Remarks
----------------------------------------------------------------------------------------------------
-- 1.0     | 24.02.2026 | Y.Hafting          | Created Manually  
----------------------------------------------------------------------------------------------------
*/
library IEEE;
  use IEEE.STD_LOGIC_1164.all;

entity timingtest is
  port(	
    clk   : in std_ulogic;		 
    a     : in std_ulogic;
    x     : out std_ulogic);
end entity;

architecture RTL of timingtest is
begin
  x <= a when rising_edge(clk);
end architecture RTL;
