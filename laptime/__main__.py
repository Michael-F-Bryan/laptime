import argparse
from serial import Serial

from .reader import record
from .misc import generate_filename, human_readable



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

