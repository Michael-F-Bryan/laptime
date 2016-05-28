import csv
import logging
from datetime import datetime
import sys
import argparse
from collections import deque
from serial import Serial

from .misc import human_readable, get_logger


class Recorder:
    def __init__(self, serial_connection, fp, log_file=None, verbose=True, 
                 write_header=True):
        self.ser = serial_connection
        self.fp = fp
        self.log_file = log_file or 'timer.log'
        self.verbose = verbose
        self.running = False
        self.entries = []
    
        # Make sure the serial connection is in non-blocking mode
        self.ser.timeout = 0

        self.logger = get_logger(__name__, 
                self.log_file,
                log_level=logging.DEBUG if verbose else logging.INFO)

        if not self.ser.is_open:
            self.ser.open()

        # Instantiate the csv writer and write the header (if desired)
        self.writer = csv.writer(self.fp)

        if write_header:
            header = ['Timestamp', 'Millis', 'Laptime', 'Human Readable']
            writer.writerow(header)

    def get_millis(self):
        buff = deque()
        while self.running:
            # Read in up to 8 bytes
            stuff = self.ser.read(8)

            if stuff:
                self.logger.debug('Got: "{}"'.format(stuff))
                buff.extend(stuff)
                
            if b'\n' in stuff:
                next_char = buff.popleft()

                message = bytearray()
                while next_char != b'\n':
                    message.append(next_char)
                    next_char = buff.popleft()

                yield message
                    


def record(serial_connection, fp, verbose=False):
    """
    Read in a line from the serial connection and write a timestamp plus
    the data to a csv file. 
    
    Each line from the serial connection is written as a new row in the csv. 
    If the time outputted by the arduino is 0 at any time, then stop the 
    recording.
    
    Note
    ----
    The recorder assumes that your serial connection will be giving times 
    delimited by a newline character ('\n').     

    Parameters
    ----------
    serial_connection: serial.Serial
        A serial connection created using the pyserial library.
    fp: file-like object
        An object that behaves like a file (i.e. has a read() and write()
        method). Most commonly created with `open(some_filename, 'w')`.
    """
    # Make sure the connection is open
    if not serial_connection.is_open:
        serial_connection.open()
        
    # Create a writer object
    writer = csv.writer(fp)

    row = ['Timestamp', 'Millis', 'Laptime', 'Human Readable']
    writer.writerow(row)

    if verbose:
        print(', '.join(row), file=sys.stderr)
    
    previous_entry = 0
    while True:
        # Wrap it in a try-except that will catch when the user
        # hits <ctrl-C> and break out of the while loop
        try:
            entry = serial_connection.readline()
            entry = int(entry)

            # Let us stop recording when we want (useful for testing)
            if entry == 0:
                break

            duration = entry - previous_entry
            row = [datetime.now(), entry, duration, human_readable(duration)]
            writer.writerow(row)

            if verbose:
                row[0] = row[0].strftime('%x %X')
                print(', '.join(str(cell) for cell in row), file=sys.stderr)

            previous_entry = entry
        except KeyboardInterrupt:
            break

