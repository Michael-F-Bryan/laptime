import pytest
from collections import deque
import random

from laptime.reader import Recorder


class DummySerial:
    def __init__(self, *args, **kwargs):
        self.current_millis = 10000
        self.buff = None

        # Seed our random number generator
        self.random = random.Random(42)

    def read(self, num_bytes=1):
        # Check if there's anything in the buffer, if not then fill it
        if not self.buff:
            # There's a 1 in 8 chance that the serial port will
            # have bytes for us
            if self.random.randrange(0, 8) == 0:
                self.current_millis += self.random.randrange(10*1000, 80*1000)
                self.buff = str(self.current_millis).encode('ascii') + b'\n'
            else:
                return b''

        stuff = self.buff[:num_bytes]
        self.buff = self.buff[num_bytes:]
        return stuff



    @property
    def is_open(self):
        return True

    def close(self):
        pass

    @property
    def timeout(self):
        return 0

    @timeout.setter
    def timeout(self, value):
        pass


@pytest.fixture
def serial(request):
    return DummySerial()


class TestDummySerial:
    def test_read_default(self, serial):
        should_be = [
                b'',
                b'5',
                b'6',
                b'0',
                b'4',
                b'8',
                b'\n',
                b'',
                b'',
                b'']

        for some_byte, _ in zip(should_be, range(10)):
            assert some_byte == serial.read()

    def test_read_4_bytes(self, serial):
        should_be = [ 
                b'',
                b'5604',
                b'8\n',
                b'',
                b'',
                b'',
                b'',
                b'',
                b'',
                b'6995']

        for some_byte, _ in zip(should_be, range(10)):
            assert some_byte == serial.read(4)


class TestRecorder:
    pass

