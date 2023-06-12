
import sys
sys.path.append('..')
from python import Class_DecodeMSF60 as MSF60
import unittest
from io import StringIO
import zmq
import pmt
import threading
import sys


class Test_Class_DecodeMSF60(unittest.TestCase):

    def setUp(self):
        self.my_decoder = MSF60.Class_DecodeMSF60()
        self.maxDiff = None

    def test_decode_BCD(self):
        # positive test
        bits = [0, 0, 0, 0]
        result = self.my_decoder.decode_BCD(bits, 4)
        objective = 0
        self.assertEqual(objective, result)

        # positive test
        bits = [0, 0, 0, 1]
        result = self.my_decoder.decode_BCD(bits, 4)
        objective = 1
        self.assertEqual(objective, result)

        # positive test
        bits = [1, 0, 0, 0]
        result = self.my_decoder.decode_BCD(bits, 4)
        objective = 8
        self.assertEqual(objective, result)

        # positive test
        bits = [1, 1, 1, 1]
        result = self.my_decoder.decode_BCD(bits, 4)
        objective = 15
        self.assertEqual(objective, result)

        # positive test
        bits = [1, 1, 1]
        result = self.my_decoder.decode_BCD(bits, 3)
        objective = 7
        self.assertEqual(objective, result)

        # negative test - too many bits
        bits = [1, 1, 1]
        result = self.my_decoder.decode_BCD(bits, 2)
        objective = "?"
        self.assertEqual(objective, result)

        # negative test - too few bits
        bits = [1, 1, 1]
        result = self.my_decoder.decode_BCD(bits, 4)
        objective = "?"
        self.assertEqual(objective, result)
    def test_decode_year(self):
        # positive test - year == 23
        bits = ["00", "00", "10", "00", "00", "00", "10", "10"]
        parity = "00"
        result = self.my_decoder.decode_year(bits, parity)
        objective = ["23", True]
        self.assertEqual(objective, result)

        # positive test - year, 10*digit > 9
        bits = ["10", "00", "10", "00", "00", "00", "00", "00"]
        parity = "10"
        result = self.my_decoder.decode_year(bits, parity)
        objective = ["Error: 10*digit of year is > 9!", False]
        self.assertEqual(objective, result)

        # positive test - year, 1*digit > 9
        bits = ["00", "00", "00", "00", "10", "00", "10", "00"]
        parity = "10"
        result = self.my_decoder.decode_year(bits, parity)
        objective = ["Error: 1*digit of year is > 9!", False]
        self.assertEqual(objective, result)

    def test_decode_summer_time(self):
        # positive test - Winter time (although first bit is zero)
        bit = "00"
        result = self.my_decoder.decode_summer_time(bit)
        objective = "Winter time."
        self.assertEqual(objective, result)

        # positive test - Winter time
        bit = "10"
        result = self.my_decoder.decode_summer_time(bit)
        objective = "Winter time."
        self.assertEqual(objective, result)

        # positive test - Summer time (although first bit is zero)
        bit = "01"
        result = self.my_decoder.decode_summer_time(bit)
        objective = "Summer time."
        self.assertEqual(objective, result)

        # positive test - Summer time
        bit = "11"
        result = self.my_decoder.decode_summer_time(bit)
        objective = "Summer time."
        self.assertEqual(objective, result)

        # positive test - erroneous input numbers
        bit = "23"
        result = self.my_decoder.decode_summer_time(bit)
        objective = "Error: Summer-time!"
        self.assertEqual(objective, result)

    def test_decode_summer_time_warning(self):
        # positive test - No Warning (although first bit is zero)
        bit = "00"
        result = self.my_decoder.decode_summer_time_warning(bit)
        objective = "No upcoming summer time warning."
        self.assertEqual(objective, result)

        # positive test - No Warning
        bit = "10"
        result = self.my_decoder.decode_summer_time_warning(bit)
        objective = "No upcoming summer time warning."
        self.assertEqual(objective, result)

        # positive test - Warning (although first bit is zero)
        bit = "01"
        result = self.my_decoder.decode_summer_time_warning(bit)
        objective = "Upcoming summer time warning active."
        self.assertEqual(objective, result)

        # positive test - Warning
        bit = "11"
        result = self.my_decoder.decode_summer_time_warning(bit)
        objective = "Upcoming summer time warning active."
        self.assertEqual(objective, result)

        # positive test - erroneous input numbers
        bit = "23"
        result = self.my_decoder.decode_summer_time_warning(bit)
        objective = "Error: Summer-time warning!"
        self.assertEqual(objective, result)

    def test_decode_weekday(self):
        # positive test - weekday == Sunday
        bits = ["00", "00", "00"]
        parity = "01"
        result = self.my_decoder.decode_weekday(bits, parity)
        objective = ["Sunday", True]

        # positive test - weekday == Saturday, wrong parity
        bits = ["10", "10", "00"]
        parity = "00"
        result = self.my_decoder.decode_weekday(bits, parity)
        objective = ["Saturday", False]

        # positive test - weekday == Saturday, wrong parity
        bits = ["10", "10", "10"]
        parity = "00"
        result = self.my_decoder.decode_weekday(bits, parity)
        objective = ["Error: Weekday does not exist!", False]

        self.assertEqual(objective, result)

    def test_decode_day(self):
        # positive test - day == 00
        bits = ["00", "00", "00", "00", "00", "00"]
        parity = "01"
        [result, _] = self.my_decoder.decode_day(bits, parity)
        objective = "Error, day=00"
        self.assertEqual(objective, result)

        # positive test - day == 15
        bits = ["00", "10", "00", "10", "00", "10"]
        parity = "00"
        [result, _] = self.my_decoder.decode_day(bits, parity)
        objective = "15"
        self.assertEqual(objective, result)

        # positive test - day == 31
        bits = ["10", "10", "00", "00", "00", "10"]
        parity = "00"
        [result, _] = self.my_decoder.decode_day(bits, parity)
        objective = "31"
        self.assertEqual(objective, result)

        # positive test - day == 32
        bits = ["10", "10", "00", "00", "10", "00"]
        parity = "00"
        [result, _] = self.my_decoder.decode_day(bits, parity)
        objective = "Error: Hours are greater than 31!"
        self.assertEqual(objective, result)

        # positive test - day - 1 digit > 9
        bits = ["00", "00", "10", "00", "10", "00"]
        parity = "00"
        [result, _] = self.my_decoder.decode_day(bits, parity)
        objective = "Error: 1*digit of hour is > 9!"
        self.assertEqual(objective, result)

        # TBD test parity

    def test_decode_month(self):
        # positive test - month == 11
        bits = ["10", "00", "00", "00", "10"]
        result = self.my_decoder.decode_month(bits)
        objective = "11"
        self.assertEqual(objective, result)

        # positive test - month == 00
        bits = ["00", "00", "00", "00", "00"]
        result = self.my_decoder.decode_month(bits)
        objective = "Error, month=00"
        self.assertEqual(objective, result)

        # positive test - month > 12
        bits = ["10", "00", "00", "10", "10"]
        result = self.my_decoder.decode_month(bits)
        objective = "Error: Month is greater than 12!"
        self.assertEqual(objective, result)

        # positive test - month 1*digit > 9
        bits = ["00", "10", "00", "10", "00"]
        result = self.my_decoder.decode_month(bits)
        objective = "Error: 1*digit of hour is > 9!"
        self.assertEqual(objective, result)
        # TBD test parity

    def test_decode_minute_marker(self):
        # positive test - correct minute marker
        bits = ["00", "10", "10", "10", "10", "10", "10", "00"]
        result = self.my_decoder.decode_minute_marker(bits)
        objective = True
        self.assertEqual(objective, result)

        # positive test - wrong minute marker
        bits = ["00", "10", "10", "00", "10", "10", "10", "00"]
        result = self.my_decoder.decode_minute_marker(bits)
        objective = False
        self.assertEqual(objective, result)

    def test_decode_bitstream(self):
        # negative test - too many bits
        bitstream = [0]*60
        result = self.my_decoder.decode_bitstream(bitstream)
        objective = "Decoding error\n#Received bits: 60\n"
        self.assertEqual(objective, result)

        # negative test - too few bits
        bitstream = [0]*58
        result = self.my_decoder.decode_bitstream(bitstream)
        objective = "Decoding error\n#Received bits: 58\n"
        self.assertEqual(objective, result)

    def _mock_send_msg(self, msg):
        context = zmq.Context()
        self.socket_sender = context.socket(zmq.PUSH)
        self.socket_sender.bind("tcp://127.0.0.1:55555")
        output = pmt.serialize_str(pmt.to_pmt(msg))
        self.socket_sender.send(output)
        self.socket_sender.close()
        context.term()

    def _mock_send_stream(self, stream, offset=0):
        for i in range(1, len(stream)):
            out_msg = f"{stream[i]}, {i + offset:02d}"
            self._mock_send_msg(out_msg)

    def test_consumer(self):
        # positive test - ordinary 0 and 1 at beginning
        # Create StringIO object to capture any print-outputs on stdout
        result = StringIO()
        sys.stdout = result

        # run MSF60 decoder in a separate thread and start it
        t_decoder = threading.Thread(target=self.my_decoder.consumer,
                                     name='Thread-consumer')
        t_decoder.start()

        # send desired messages and exit-signal
        self._mock_send_msg("00")
        self._mock_send_msg("10")
        self._mock_send_msg("11")
        self._mock_send_msg("01")
        self._mock_send_msg("___EOT")

        # wait for decoder-thread to be completed
        t_decoder.join()

        objective = "00: 00\n" + \
                    "01: 10\n" + \
                    "02: 11\n" + \
                    "03: 01\n"
        self.assertEqual(objective, result.getvalue())

        # full clean-up of decoder
        del t_decoder

if __name__ == '__main__':
    testInstance = Test_Class_DecodeMSF60()
    unittest.main()