import csv
from datetime import datetime
import sys
import argparse

try:
    from serial import Serial
except ImportError:
    print('Please install the pyserial package')
    print('(pip install pyserial)')
    sys.exit(1)



def generate_filename(base='track_times', timestamp_format=None):
    """
    Create a unique filename that incorporates a timestamp. 
    
    For example if the filename were generated on the 19th of April 2016
    at 12:16:47, then the default output would be: "track_times_2016-04-19_1216.csv"
    
    Parameters
    ----------
    base: str
        The base name for the filename, a timestamp is appended to this.
    timestamp_format: str
        A strftime formatting string. See "http://strfti.me/" for more
        details.
        
    Returns
    -------
    str
        A unique filename.
    """
    if timestamp_format is None:
        timestamp_format = '%Y-%m-%d_%H%M'
    time_stamp = datetime.now().strftime(timestamp_format)

    name = '{}_{}.csv'.format(base, time_stamp)
    if '/' in name:
        raise ValueError('Invalid filename: {}'.format(name))

    return name

def human_readable(millis): 
    """ 
    Take a number of milliseconds and turn it into a string with the format
    "min:sec.millis".
    """
    if not isinstance(millis, int):
        raise TypeError('millis must be a positive integer')

    if millis < 0:
        raise ValueError('millis must be a positive integer')

    seconds, ms = divmod(millis, 1000)
    minutes, seconds = divmod(seconds, 60)

    return '{}:{}.{}'.format(minutes, seconds, int(ms))
    

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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', dest='port', type=str,
            help='The serial port to listen on (default: COM1)')
    parser.add_argument('-o', '--output-file', dest='out', type=str,
            help='The basename of your output file (default: "track_times")')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            help='Print recorded results to stderr as they are received')

    args = parser.parse_args()

    if args.port:
        serial_port = args.port
    else:
        serial_port = 'COM1'  
        
    if args.out:
        output_file = generate_filename(base=args.out)
    else:
        output_file = generate_filename()

    # Set the timeout to be some stupidly huge number so the program will
    # Just block until it receives another entry from the arduino
    ser = Serial(serial_port, baudrate=19600, timeout=100000)

    # Start the actual recording
    with open(output_file, 'w') as fp:
        record(ser, fp, verbose=args.verbose)
    

if __name__ == '__main__':
    # This line is here so that you can import the file without
    # executing it.
    main()

