# Sensor data interface

| ![Simple version](./unispi.md) |

## Specification
We have a system with one sensor that communicate serially

Compared to the first unispi system, we add sensor B and C: 
* Sensor A has 3 data bytes each time ready is flagged. 
* Sensor B has 2 data bytes each time ready is flagged
* Sensor C has 5 data bytes each time ready is flagged

## Derived ASMD diagram
| ![ASM Diagram](./unispi-extended-ASMD.svg) |
| :---: | 
| ASM diagram |


## Testbench
The testbench features independent stimuli and checkers to ensure readability. 
This is made possible by the use of queues for sharing data between stimuli methods and checkers.  

Each stimuli model can run independently of the others since we use triggered stimuli generation. 
Triggered stimuli requires the use of ```start_soon(<task>)``` and ```Combine(<task>)```, in order to have each complete before program ends.  

The testbench is not intended as a full functional test. 
The checks applied are limited to checking that outgoing data and control signals matches the modeled input in whatever order they are applied. 
