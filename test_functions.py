import unittest
from unittest import mock
from Emulator import *
from contextlib import redirect_stdout
import io
import sys
import os
from Monitor import main as testingMain


class StaticMethodTests(unittest.TestCase):
    def test_static_string_to_hex(self):
        """
        get_hex_string
        Test that minimum length is 2, and that letters are capitalized
        """
        string_zero = T34Emulator.get_hex_string_from_decimal_number(0)
        self.assertEqual(string_zero, "00")

        string_small_num = T34Emulator.get_hex_string_from_decimal_number(16)
        self.assertEqual(string_small_num, "10")

        string_max = T34Emulator.get_hex_string_from_decimal_number(255)
        self.assertEqual(string_max, "FF")

    def test_cyclical_conversions(self):
        """
        test that conversion doesn't lose information when making a full loop
        """
        num = T34Emulator.get_decimal_number_from_hex_string(T34Emulator.get_hex_string_from_decimal_number(10))
        self.assertEqual(num, 10)


class DisplayMemoryLocationsTest(unittest.TestCase):
    def test_edit_memory_locations(self):
        """
        300: A9 04 85 07 A0 00 84 06 A9 A0 91 06 C8 D0 FB E6 07
        """
        SUT = T34Emulator()
        starting = T34Emulator.get_decimal_number_from_hex_string("300")
        test_values = []
        for i in "A9 04 85 07 A0 00 84 06 A9 A0 91 06 C8 D0 FB E6 07".split(" "):
            test_values.append(T34Emulator.get_decimal_number_from_hex_string(i))
        SUT.save_values_to_memory(starting, test_values)

        # 300.310
        display_start = T34Emulator.get_decimal_number_from_hex_string("300")
        display_end = T34Emulator.get_decimal_number_from_hex_string("310")
        f = io.StringIO()
        with redirect_stdout(f):
            SUT.display_data_from_range(display_start, display_end)

        correct_output = "300   A9 04 85 07 A0 00 84 06 \n" \
                         + "308   A9 A0 91 06 C8 D0 FB E6 \n" \
                         + "310   07 \n"
        self.assertEqual(correct_output, f.getvalue())


class RunProgram(unittest.TestCase):
    def test_run_program(self):
        SUT = T34Emulator()

        f = io.StringIO()
        with redirect_stdout(f):
            SUT.begin_executation(T34Emulator.get_decimal_number_from_hex_string("200"))
            "123456789012345678901234567890123456789012345690"
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC"
        correct_output = " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
                         + " 200\n"
        self.assertEqual(correct_output, f.getvalue())


class TestInput(unittest.TestCase):
    def test_exit(self):
        with mock.patch('builtins.input', return_value="exit"):
            valid, grabbed_string = T34Emulator.prompt_for_input()
        self.assertFalse(valid)

        with mock.patch('builtins.input', return_value="EXIT"):
            valid, grabbed_string = T34Emulator.prompt_for_input()
        self.assertFalse(valid)


"""
#windows specific attempt at running the program and testing the output aginst the documented intended output
class TestInput(unittest.TestCase):
    def test_exit(self):
        command_string = " more test1.in > 'python Monitor.py test1.obj' > test1result.out"
        temp = os.system(command_string)

"""
if __name__ == '__main__':
    unittest.main()
