/*  Unidirectional Serial Perihperal Interface with interrupts (UNISPI)
    
    The purpose of this module is teaching how to get from ASM diagrams to VHDL code.
    The purpose here is not making a full SPI bus interface, there may be inconsistencies. 
    
    The code is intended for the second lecture in FSMs for IN3160/4160 (first use 2025). 
    The module shall connect to a three sensor devices "A", "B", "C". 
    Each sensor device has an interrupt line, prioritized by alphabet
    Any sensor serviced will send all its current data 
    A sends 3 bytes, B sends 2 bytes, C sends 5 bytes
            
*/
library IEEE;
  use IEEE.std_logic_1164.all; 
  use IEEE.numeric_std.all;
  
entity uniSPI is 
  generic(BYTE : integer := 8);
  port( 
    -- system clock and reset = register control
    clk, reset : in std_ulogic;
  
    -- Sensor interface
    intA, intB, intC, sin : in  std_ulogic;
    csA, csB, csC, sck    : out std_ulogic;

    -- CPU interface
    ready : out std_ulogic;
    control, data: out std_ulogic_vector(BYTE-1 downto 0)
  );
end entity uniSPI;  
  
architecture RTL of uniSPI is 
  constant Aid : std_ulogic_vector((BYTE/2)-1 downto 0) := "0001"; -- Sensor A id nibble
  constant Bid : std_ulogic_vector((BYTE/2)-1 downto 0) := "0010"; -- Sensor B id nibble
  constant Cid : std_ulogic_vector((BYTE/2)-1 downto 0) := "0011"; -- Sensor C id nibble
  
  type statetype is (idle, receive);  
  signal r_state, next_state : statetype;
  
  signal r_count, next_count : u_unsigned(6 downto 0);
  alias bitcount : u_unsigned is r_count(2 downto 0);
  alias bytecount : u_unsigned is r_count(6 downto 3);
  alias r_sck : std_ulogic is sck;
  alias r_ready : std_ulogic is ready;
  alias r_csA : std_ulogic is csA;
  alias r_csB : std_ulogic is csB;
  alias r_csC : std_ulogic is csC;
  signal next_csA, next_csB, next_csC : std_ulogic;
  signal next_sck, next_ready : std_ulogic;
  signal r_sreg, next_sreg : std_ulogic_vector(BYTE-1 downto 0);
  signal id, byte_threshold : integer range 0 to 15;

begin 
  CHIP_BASED_VALUES:
  byte_threshold <= 
    3 when csA else
    2 when csB else
    5 when csC else 
    0;
  id <= 
    1 when csA else
    2 when csB else
    3 when csC else 
    0;

  REGISTER_ASSIGNMENT: process(clk) is 
  begin 
    if rising_edge(clk) then 
      if reset then 
        r_sck     <= '1';
        r_state   <= idle;
        r_count   <= (others => '0');
        r_sreg    <= (others => '0');
        r_ready   <= '0';
        r_csA     <= '0';
        r_csB     <= '0';
        r_csC     <= '0';
      else
        r_sck     <= next_sck;
        r_state   <= next_state;
        r_count   <= next_count;
        r_sreg    <= next_sreg;
        r_ready   <= next_ready;
        r_csA     <= next_csA;
        r_csB     <= next_csB;
        r_csC     <= next_csC;
      end if;
    end if;
  end process;

  

  STATE_TRANSITIONS: process(all) is 
  begin 
    -- default state (has big impact on descision tree structure)
    next_state <= r_state; 
    -- state transitions
    case r_state is 
      when idle =>
        next_state <= receive when intA or intB or intC;
      when receive => 
        next_state <= idle when (sck = '0') and (bytecount = byte_threshold);
    -- when others => -- avoid others clause when not needed
    end case;
  end process;
  
  STATE_OUTPUT: process(all) is
  begin
    --default values:
    next_count   <= r_count;
    next_sck     <= '1';
    next_sreg    <= r_sreg;
    next_ready   <= '0';
    next_csA     <= r_csA;
    next_csB     <= r_csB;
    next_csC     <= r_csC;
    -- state based assignment
    case r_state is 
      when idle =>
        next_count <= (others => '0');
        if intA then 
          next_csA <= '1';
          next_csB <= '0';
          next_csC <= '0';
        elsif intB then 
          next_csA <= '0';
          next_csB <= '1';
          next_csC <= '0';
        elsif intC then 
          next_csA <= '0';
          next_csB <= '0';
          next_csC <= '1';
        else 
          next_csA <= '0';
          next_csB <= '0';
          next_csC <= '0';
        end if;
      when receive =>
        next_sck <= not r_sck;
        if r_sck = '1' then 
          next_count <= r_count + 1;
        else 
          next_sreg  <= r_sreg(6 downto 0) & sin ;
          if bitcount = 0 then 
            next_ready   <= '1';
          else
            null; -- assign default values 
          end if;
        end if;
    end case;
  end process;

  FLAGGED_OUTPUT: process(all) is 
  begin 
    if ready then 
      data <= r_sreg;
      control <= std_ulogic_vector(to_unsigned(id,BYTE/2)) & std_ulogic_vector(bytecount);
    else
      data <= (others => '0');
      control <= (others => '0');    
    end if;
  end process;
end architecture RTL;

  





  