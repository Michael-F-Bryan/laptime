=======
Laptime
=======

.. The travis.ci shield
.. image:: https://travis-ci.org/Michael-F-Bryan/laptime.svg?branch=master
    :target: https://travis-ci.org/Michael-F-Bryan/laptime

.. Tag number
.. image:: https://img.shields.io/github/tag/Michael-F-Bryan/mfb_utils.svg?maxAge=2592000

.. License
.. image:: https://img.shields.io/github/license/Michael-F-Bryan/mfb_utils.svg?maxAge=2592000


A client for CMT's laptimer.


Description
===========

This application will receive a "millis" time from an arduino via a serial
port, calculate the corresponding laptime, and then write it to a file.


Note
====

The laptime client assumes that it will be reading bytes over a serial port. In
particular, it expects that the bytes provided will be integers, delimited by a
newline character ("\\n"). 

If no newline character is passed over the serial port then the program will 
seem to hang forever, never writing anything to file or producing any output.
