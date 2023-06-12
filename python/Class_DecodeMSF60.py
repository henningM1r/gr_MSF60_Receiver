# -*- coding: iso-8859-1 -*-

import zmq


class Class_DecodeMSF60():

    def __init__(self):
        self.weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                         "Friday", "Saturday"]

    def decode_BCD(self, bits, length):
        if length != len(bits):
            # lengths missmatch
            return "?"

        list1 = [bits[i] for i in range(0, length)]

        str1 = ''.join(str(e) for e in list1)
        val = int(str1, 2)

        return val

    def decode_year(self, bits, parity):
        b_bit = int(parity[1])
        bits10 = [bits[0][0], bits[1][0], bits[2][0], bits[3][0]]
        bits10 = list(map(int, bits10))
        val10 = self.decode_BCD(bits10, 4)

        bits1 = [bits[4][0], bits[5][0], bits[6][0], bits[7][0]]
        bits1 = list(map(int, bits1))
        val1 = self.decode_BCD(bits1, 4)

        year = f"{val10}{val1}"

        # check validity of digit values
        if val10 > 9 and val1 <= 9:
            return ["Error: 10*digit of year is > 9!", False]
        elif (val10 <= 9 and val1 > 9):
            return ["Error: 1*digit of year is > 9!", False]

        # compute odd parity
        comp_parity = (int(bits[0][0]) ^ int(bits[1][0]) ^ int(bits[2][0]) ^ 
                       int(bits[3][0]) ^ int(bits[4][0]) ^ int(bits[5][0]) ^
                       int(bits[6][0]) ^ int(bits[7][0]))

        year_parity = False

        if comp_parity ^ b_bit == 1:
            year_parity = True

        return [year, year_parity]

    def decode_month(self, bits):
        bits10 = [bits[0][0]]
        bits10 = list(map(int, bits10))
        val10 = self.decode_BCD(bits10, 1)

        bits1 = [bits[1][0], bits[2][0], bits[3][0], bits[4][0]]
        bits1 = list(map(int, bits1))
        val1 = self.decode_BCD(bits1, 4)

        # check validity of digit values
        if val10 == 0 and val1 == 0:
            return "Error, month=00"
        elif val10 == 1 and val1 > 2:
            return "Error: Month is greater than 12!"
        elif (val1 > 9 and val10 <= 1):
            return "Error: 1*digit of hour is > 9!"

        month = f"{val10}{val1}"

        return month

    def decode_day(self, bits, parity):
        b_bit = int(parity[1])

        bits10 = [bits[0][0], bits[1][0]]
        bits10 = list(map(int, bits10))
        val10 = self.decode_BCD(bits10, 2)

        bits1 = [bits[2][0], bits[3][0], bits[4][0], bits[5][0]]
        bits1 = list(map(int, bits1))
        val1 = self.decode_BCD(bits1, 4)

        # check validity of digit values
        if val10 == 0 and val1 == 0:
            return ["Error, day=00", False]
        if val10 == 3 and val1 > 1:
            return ["Error: Hours are greater than 31!", False]
        elif (val1 > 9 and val10 <= 2):
            return ["Error: 1*digit of hour is > 9!", False]

        day = f"{val10}{val1}"

        # compute odd parity
        comp_parity = (int(bits[0][0]) ^ int(bits[1][0]) ^ int(bits[2][0]) ^ 
                       int(bits[3][0]) ^ int(bits[4][0]) ^ int(bits[5][0]))

        day_parity = False

        if comp_parity ^ b_bit == 1:
            day_parity = True

        return [day, day_parity]

    def decode_weekday(self, bits, parity):
        b_bit = int(parity[1])

        bits_w = [bits[0][0], bits[1][0], bits[2][0]]
        bits_w = list(map(int, bits_w))
        val = self.decode_BCD(bits_w, 3)

        if val == 7:
            return ["Error: Weekday does not exist!", False]
        weekday = self.weekdays[val]

        # compute odd parity
        comp_parity = int(bits[0][0]) ^ int(bits[1][0]) ^ int(bits[2][0])

        weekday_parity = False

        if comp_parity ^ b_bit == 1:
            weekday_parity = True

        return [weekday, weekday_parity]

    def decode_time(self, bits, parity):
        b_bit = int(parity[1])

        bits_hour = bits[0:6]
        bits_minute = bits[6:13]

        hour = self.decode_hour(bits_hour)
        minute = self.decode_minute(bits_minute)
        time = f"{hour}:{minute}"

        # compute odd parity
        comp_parity = (int(bits[0][0]) ^ int(bits[1][0]) ^ int(bits[2][0]) ^
                       int(bits[3][0]) ^ int(bits[4][0]) ^ int(bits[5][0]) ^
                       int(bits[6][0]) ^ int(bits[7][0]) ^ int(bits[8][0]) ^
                       int(bits[9][0]) ^ int(bits[10][0]) ^ int(bits[11][0]) ^
                       int(bits[12][0]))

        time_parity = False

        if comp_parity ^ b_bit == 1:
            time_parity = True

        return [time, time_parity]

    def decode_hour(self, bits):
        bits10 = [bits[0][0], bits[1][0]]
        bits10 = list(map(int, bits10))
        val10 = self.decode_BCD(bits10, 2)

        # TBD check if val10>=0 and val10 <=2
        bits1 = [bits[2][0], bits[3][0], bits[4][0], bits[5][0]]
        bits1 = list(map(int, bits1))
        val1 = self.decode_BCD(bits1, 4)

        # TBD check if val1>=0 and val10 <=9
        # TBD check if hour <= 23
        hour = f"{val10}{val1}"

        return hour

    def decode_minute(self, bits):
        bits10 = [bits[0][0], bits[1][0], bits[2][0]]
        bits10 = list(map(int, bits10))
        val10 = self.decode_BCD(bits10, 3)

        # TBD check if val10>=0 and val10 <=5

        bits1 = [bits[3][0], bits[4][0], bits[5][0], bits[6][0]]
        bits1 = list(map(int, bits1))
        val1 = self.decode_BCD(bits1, 4)

        # TBD check if val1>=0 and val10 <=9

        minute = f"{val10}{val1}"

        return minute

    def decode_minute_marker(self, bits):
        bits_mm = list(map(int, [bits[0][0], bits[1][0], bits[2][0],
                   bits[3][0], bits[4][0], bits[5][0],
                   bits[6][0], bits[7][0]]))
        minute_marker = [0,1,1,1,1,1,1,0]

        if bits_mm == minute_marker:
            # Minute marker detected successfully
            return True

        return False

    def decode_summer_time(self, bit):
        b_bit = int(bit[1])

        if b_bit == 1:
            return "Summer time."
        elif b_bit == 0:
            return "Winter time."
        else:
            return "Error: Summer-time!"

    def decode_summer_time_warning(self, bit):
        b_bit = int(bit[1])

        if b_bit == 1:
            return "Upcoming summer time warning active."
        elif b_bit == 0:
            return "No upcoming summer time warning."
        else:
            return "Error: Summer-time warning!"

    def decode_bitstream(self, bitstream):
        output = ""

        count = len(bitstream)

        if count != 59:
            output += "Decoding error\n"
            output += f"#Received bits: {len(bitstream)}\n"
            return output

        if bitstream[0] != "00":
            output += "00: Minute marker is not 11!"
            return  output

        # NOTE first bits 01-16 are ignored here for now...
        [year, year_parity] = self.decode_year(bitstream[16:24],
                                               bitstream[53])
        month = self.decode_month(bitstream[24:29])
        [day, day_parity] = self.decode_day(bitstream[29:35], bitstream[54])
        [weekday, weekday_parity] = self.decode_weekday(bitstream[35:38],
                                                        bitstream[55])
        [time, time_parity] = self.decode_time(bitstream[38:52],
                                               bitstream[56])
        minute_marker = self.decode_minute_marker(bitstream[51:59])
        summer_time_warning = self.decode_summer_time_warning(bitstream[52])
        summer_time = self.decode_summer_time(bitstream[57])
        minute_marker = self.decode_minute_marker(bitstream[51:59])

        output += "\n=== Minute decoded ===\n"
        output += f"00: Start-bit detected {bitstream[0]}.\n"
        output += f"17-35: Date is {day}-{month}-{year}.\n"
        output += f"36-38: Weekday is {weekday}.\n"
        output += f"39-51: Time of day is {time}h.\n"
        output += f"53: {summer_time_warning}\n"
        output += f"54: Parity of year matches: {year_parity}\n"
        output += f"55: Parity of day matches: {day_parity}\n"
        output += f"56: Parity of weekday matches: {weekday_parity}\n"
        output += f"57: Parity of time of day matches: {time_parity}\n"
        output += f"58: {summer_time}\n"
        output += f"52-59: Minute marker 01111110 detected: {minute_marker}\n"
        output += "======================"

        return output

    def consumer(self):
        context = zmq.Context()

        consumer_receiver = context.socket(zmq.PULL)
        consumer_receiver.connect("tcp://127.0.0.1:55555")

        bitstream = []
        count = 0

        while True:
            data = consumer_receiver.recv()
            received_msg = data.decode('ascii')[3:]

            # exit-loop statement: for testing only
            if received_msg == "___EOT":
                consumer_receiver.close()
                context.term()
                break

            print(f"{count:02d}: {received_msg}")

            if received_msg == "00":
                bitstream.append("00")
                count += 1
                continue

            elif received_msg == "10":
                bitstream.append("10")
                count += 1
                continue

            elif received_msg == "11":
                bitstream.append("11")
                count += 1
                continue

            # NOTE, never encountered this codeword yet...
            elif received_msg == "01":
                bitstream.append("01")
                count += 1
                continue

            # derive current time and date from the bitstream
            elif received_msg == "2" and count == 59:
                output = self.decode_bitstream(bitstream)
                print(output)

                bitstream = []

                count = 0
                continue

            # either too few or to many bits have
            # been received during the decoding step
            elif (received_msg == "2" and
                  count > 59):
                print("Error: Received more than 59 bits at new minute")
                print(f"#Bits: {len(bitstream)}")

                bitstream = []
                count = 0
                continue
            # either too few or to many bits have
            # been received during the decoding step
            elif (received_msg == "2" and
                  count < 59):
                print("Error: Received less than 59 bits at new minute")
                print(f"#Bits: {len(bitstream)}")

                bitstream = []
                count = 0
                continue


