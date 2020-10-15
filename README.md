# 6502_Emulator

An emulator for the 6502 processor written in Python for a class in computer organization and arcitecture. 

Included in this project are test files that can be run on the pseduo command line, as well as a large suite of sample runs as tests. This was originally meant to ensure functionality for the class but now allows for specific behavior to be targeted if I'd like to develop the emulator further.

Running:

The program is run by invoking an installation of Python3, followed by Monitor.py, followed by
an optional filename for data in the intex HEX format.
EX:
$ python3 Monitor.py testFiles/test1.obj

Testing:

$ python3 TestFunctions.py


Static methods and conversions were tested to ensure no data was lost going back and forth.
All example runs of the program provided by the documentation were directly translated to tests.
Command line object loading was intended to be added, but the intended implementation would
be operating system specific, and therefore testing accuracy would be ambiguous. Manual
testing of all example test cases was performed before submission.