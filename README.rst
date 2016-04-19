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

    usage: laptime_client.py [-h] [-p PORT] [-o OUT]

    optional arguments:
    -h, --help            show this help message and exit
    -p PORT, --port PORT  The serial port to listen on (default: COM1)
    -o OUT, --output-file OUT
                            The basename of your output file (default:
                            "track_times")
    
Often, running the laptime client is as simple as ::

    python laptime_client.py

If you are having problems finding your serial port, then the pyserial library
includes a neat tool::

    python -m serial.tools.list_ports
