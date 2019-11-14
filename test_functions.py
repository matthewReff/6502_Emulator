import unittest
from unittest import mock
from Helper import *
from Memory import *
from Monitor import *
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
        string_zero = Helper.get_hex_string_from_decimal_number(0)
        self.assertEqual(string_zero, "00")

        string_small_num = Helper.get_hex_string_from_decimal_number(16)
        self.assertEqual(string_small_num, "10")

        string_max = Helper.get_hex_string_from_decimal_number(255)
        self.assertEqual(string_max, "FF")

    def test_cyclical_string_to_int(self):
        """
        test that conversion doesn't lose information when making a full loop
        """
        num = Helper.get_decimal_number_from_hex_string(Helper.get_hex_string_from_decimal_number(10))
        self.assertEqual(num, 10)

    def test_twos_compliment(self):
        hex_num_string = "FF"
        hex_num = Helper.get_decimal_number_from_hex_string(hex_num_string)
        twos_comp = Helper.get_twos_compliment(hex_num)
        self.assertEqual(1, twos_comp)

        hex_num_string = "80"
        hex_num = Helper.get_decimal_number_from_hex_string(hex_num_string)
        twos_comp = Helper.get_twos_compliment(hex_num)
        self.assertEqual(128, twos_comp)


class DisplayMemoryLocationsTest(unittest.TestCase):
    def test_edit_memory_locations(self):
        """
        300: A9 04 85 07 A0 00 84 06 A9 A0 91 06 C8 D0 FB E6 07
        """
        SUT = Memory()
        starting = Helper.get_decimal_number_from_hex_string("300")
        test_values = []
        for i in "A9 04 85 07 A0 00 84 06 A9 A0 91 06 C8 D0 FB E6 07".split(" "):
            test_values.append(Helper.get_decimal_number_from_hex_string(i))
        SUT.save_values_to_memory(starting, test_values)

        # 300.310
        display_start = Helper.get_decimal_number_from_hex_string("300")
        display_end = Helper.get_decimal_number_from_hex_string("310")
        f = io.StringIO()
        with redirect_stdout(f):
            SUT.display_data_from_range(display_start, display_end)

        correct_output = "300   A9 04 85 07 A0 00 84 06 \n" \
                         + "308   A9 A0 91 06 C8 D0 FB E6 \n" \
                         + "310   07 \n"
        self.assertEqual(correct_output, f.getvalue())


class RunProgram(unittest.TestCase):
    def test_run_program(self):
        SUT = Memory()

        f = io.StringIO()
        with redirect_stdout(f):
            SUT.execute_at_location(Helper.get_decimal_number_from_hex_string("200"))
            "123456789012345678901234567890123456789012345690"
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC"
        correct_output = " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
                        +" 200  00  BRK   impl -- --  00 00 00 FC 00100000\n"
        self.assertEqual(correct_output, f.getvalue())


class TestInput(unittest.TestCase):
    def test_exit(self):
        with mock.patch('builtins.input', return_value="exit"):
            valid, grabbed_string = Monitor.prompt_for_input()
        self.assertFalse(valid)

        with mock.patch('builtins.input', return_value="EXIT"):
            valid, grabbed_string = Monitor.prompt_for_input()
        self.assertFalse(valid)


class TestStackOps(unittest.TestCase):
    def test_push(self):
        SUT = Memory()
        SUT.push_to_stack(10)

        self.assertEqual(SUT.mainMemory[SUT.registers["SP"]+1], 10)
        self.assertEqual(SUT.registers["SP"], Helper.get_decimal_number_from_hex_string("FF")-1)

    def test_cyclic(self):
        SUT = Memory()
        SUT.push_to_stack(10)
        val = SUT.pop_from_stack()

        self.assertEqual(10, val)
        self.assertEqual(Helper.get_decimal_number_from_hex_string("FF"), SUT.registers["SP"])

"""
#windows specific attempt at running the program and testing the output aginst the documented intended output
class TestInput(unittest.TestCase):
    def test_exit(self):
        command_string = " more test1.in > 'python Monitor.py test1.obj' > test1result.out"
        temp = os.system(command_string)

"""
if __name__ == '__main__':
    unittest.main()
