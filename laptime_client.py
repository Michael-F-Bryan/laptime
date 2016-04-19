import csv
from datetime import datetime
import sys

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
    return '{}_{}.csv'.format(base, time_stamp)


def record(serial_connection, fp):
    """
    Read in a line from the serial connection and write a timestamp plus
    the data to a csv file. Each line from the serial connection is 
    written as a new row in the csv.
    
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
    
    while True:
        # Wrap it in a try-except that will catch when the user
        # hits <ctrl-C> and break out of the while loop
        try:
            entry = serial_connection.readline()
            writer.write(datetime.now(), entry)
        except KeyboardInterrupt:
            break


def main():
    # Set up the serial connection
    serial_port = '/dev/ttyUSB0'  # 'COM1' for Windows
    output_file = generate_filename()

    ser = Serial(serial_port, baudrate=19600, timeout=1)

    write(ser, 'stuff.csv')
    

if __name__ == '__main__':
    # This line is here so that you can import the file without
    # executing it.
    main()
