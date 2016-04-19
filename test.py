from io import StringIO
from unittest import TestCase
import re
import random
import time

from laptime_client import generate_filename, record, human_readable


class DummyArduino:
    def __init__(self, count=5, is_open=True, delay=0.01):
        self.is_open = is_open
        self.counter = 0
        self.max_count = count
        self.delay = delay
        self.current_num = random.randint(1, 20000)

    def readline(self):
        random_wait = self.delay + random.uniform(-1, 1)*self.delay/10
        time.sleep(random_wait)

        if self.counter < self.max_count:
            self.counter += 1
            self.current_num += random.randint(30*1000, 250*1000)
            output = b'%d\n' % (self.current_num,)
            return output
        else:
            return b'%d\n' % (0,)


class FilenameGeneratorTest(TestCase):
    def test_defaults(self):
        pattern = r'track_times_\d{4}-\d{2}-\d{2}_\d{4}.csv'
        some_filename = generate_filename()

        self.assertRegex(some_filename, pattern)

    def test_change_base_name(self):
        new_base = 'foo'
        pattern = r'%s_\d{4}-\d{2}-\d{2}_\d{4}.csv' % (new_base,)
        some_filename = generate_filename(new_base)

        self.assertRegex(some_filename, pattern)

    def test_invalid_date_format(self):
        # We're using a dodgy pattern here, forward slashes shouldn't
        # be allowed in filenames. %x gives the date as 19/04/2016
        date_format = '%x %X'

        with self.assertRaises(ValueError):
            some_filename = generate_filename(timestamp_format=date_format)


class RecordTest(TestCase):
    def setUp(self):
        self.ser = DummyArduino(delay=0.01)
        self.fp = StringIO()

    def test_record(self):
        record(self.ser, self.fp)

        print()
        print(self.fp.getvalue())


class HumanReadableTest(TestCase):
    def test_a_couple_ms(self):
        num_ms = 124
        stuff = human_readable(num_ms)
        self.assertEqual(stuff, '0:0.124')

    def test_a_couple_seconds(self):
        num_ms = 1234
        stuff = human_readable(num_ms)
        self.assertEqual(stuff, '0:1.234')

    def test_a_couple_minutes(self):
        num_ms = 1000*60*5 + 5*1000 + 657
        stuff = human_readable(num_ms)
        self.assertEqual(stuff, '5:5.657')

    def test_invalid_number(self):
        num_ms = -3
        
        with self.assertRaises(ValueError):
            stuff = human_readable(num_ms)

    def test_invalid_type(self):
        num_ms = 'stuff'
        
        with self.assertRaises(TypeError):
            stuff = human_readable(num_ms)
