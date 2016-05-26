import csv
from datetime import datetime
import sys
import argparse
from serial import Serial

from .misc import human_readable


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
        except ValueError:
            # The timer's millis() function probably overflowed or something
            print("Laptimer's millis() overflowed.", file=sys.stderr)
            print('You should probably turn it off and turn it on again...', 
                    file=sys.stderr)
            raise RuntimeError from ValueError

