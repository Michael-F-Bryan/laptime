=======
laptime
=======


Add a short description here!


Description
===========

A LONGER DESCRIPTION OF YOUR PROJECT GOES HERE...


Note
====

Assumptions
===========
The laptime client assumes that it will be reading bytes over a serial port. In
particular, it expects that the bytes provided will be integers, delimited by a
newline character ("\n"). 

If no newline character is passed over the serial port then the program will 
seem to hang forever, never writing anything to file or producing any output.
