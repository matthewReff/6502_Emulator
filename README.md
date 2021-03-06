# 6502_Emulator

An emulator for the 6502 processor written in Python for a class in computer organization and arcitecture. 

Included in this project are test files that can be run on the pseduo command line, as well as a large suite of sample runs as tests. This was originally meant to ensure functionality for the class but now allows for specific behavior to be targeted if I'd like to develop the emulator further.

# Usage
## Loading Data
The program is run by invoking an installation of Python3, followed by Monitor.py, followed by
an optional filename for data in the intex HEX format.

>$ python3 Monitor.py testFiles/test1.obj

>$ python3 Monitor.py

Now that we have data loaded, or not, and can run some of the psuedo-command line commands.

## Issuing Commands

### Run
Begin execution starting at a memory location.

Format: {Hex_Memory_Location}R

>\> 300R

### View
View the data stored in a given memory location

Format: {Hex_Memory_Location}

>\> 300
### View Range
View the data stored in a given memory range(inclusive). Creates a newline for every 8 entries.

Format: {Hex_Memory_Location}.{Hex_Memory_Location}

>\> 300.310
### Enter Data
Add data to memory starting at a given location

Format: {Hex_Memory_Location}:{Memory_Value Memory_Value}

>\> 300:A9 85 A5 00 
### Exit
Leave the command line. EOF, keyboard interupt, or any capitalization of "exit" will work.

>\> exit
# Testing

>$ python3 TestFunctions.py

Static methods and conversions were tested to ensure no data was lost going back and forth.

All example runs of the program provided by the documentation were directly translated to tests.

Command line object loading was intended to be added, but the intended implementation would
be operating system specific, and therefore testing accuracy would be ambiguous.