Laptime Client README
=====================

A program for recording laptimes from an arduino and then saving them to a 
csv file.

Installing
==========
To use this program, you will need to first clone the git repository::
    git clone https://github.com/Michael-F-Bryan/laptime_client.git

Then install the dependencies using pip::
    pip install pyserial


Usage
=====

.. note::
    This program was designed for using Python 3. It should still work on
    Python 2.x, but considering Python 2.7.0 was released over 6 years ago you
    should probably consider upgrading anyway...

By running `python laptime_client.py -h`, you are shown the following output::

    usage: laptime_client.py [-h] [-p PORT] [-o OUT] [-v]

    optional arguments:
    -h, --help            show this help message and exit
    -p PORT, --port PORT  The serial port to listen on (default: COM1)
    -o OUT, --output-file OUT
                            The basename of your output file (default:
                            "track_times")
    -v, --verbose         Print recorded results to stderr as they are received
    
Often, running the laptime client is as simple as ::

    python laptime_client.py

If you are having problems finding your serial port, then the pyserial library
includes a neat tool::

    python -m serial.tools.list_ports


Assumptions
===========
The laptime client assumes that it will be reading bytes over a serial port. In
particular, it expects that the bytes provided will be integers, delimited by a
newline character ("\n"). 

If no newline character is passed over the serial port then the program will 
seem to hang forever, never writing anything to file or producing any output.
