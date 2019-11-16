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

        memory = Memory()
        f = io.StringIO()
        with redirect_stdout(f):
            Processor.execute_at_location(memory, Helper.get_decimal_number_from_hex_string("200"))
            "123456789012345678901234567890123456789012345690"
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC"
        correct_output = " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
                        +" 200  00  BRK   impl -- --  00 00 00 FC 00110100\n"
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


class TestPhaseII(unittest.TestCase):
    def test_example_run_1(self):
        #"300: EA C8 98 48 E8 E8 8A 68 00"
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "EA C8 98 48 E8 E8 8A 68 00".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" \
            " 301  C8  INY   impl -- --  00 00 01 FF 00100000\n" \
            " 302  98  TYA   impl -- --  01 00 01 FF 00100000\n" \
            " 303  48  PHA   impl -- --  01 00 01 FE 00100000\n" \
            " 304  E8  INX   impl -- --  01 01 01 FE 00100000\n" \
            " 305  E8  INX   impl -- --  01 02 01 FE 00100000\n" \
            " 306  8A  TXA   impl -- --  02 02 01 FE 00100000\n" \
            " 307  68  PLA   impl -- --  01 02 01 FF 00100000\n" \
            " 308  00  BRK   impl -- --  01 02 01 FC 00110100\n"
        self.assertEqual(correct_output, f.getvalue())

    def test_example_run_2(self):
        #"300: 88 E8 98 0A 2A 48 8A 6A A8 68 AA 00"
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "88 E8 98 0A 2A 48 8A 6A A8 68 AA 00".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  88  DEY   impl -- --  00 00 FF FF 10100000\n" \
            " 301  E8  INX   impl -- --  00 01 FF FF 00100000\n" \
            " 302  98  TYA   impl -- --  FF 01 FF FF 10100000\n" \
            " 303  0A  ASL      A -- --  FE 01 FF FF 10100001\n" \
            " 304  2A  ROL      A -- --  FD 01 FF FF 10100001\n" \
            " 305  48  PHA   impl -- --  FD 01 FF FE 10100001\n" \
            " 306  8A  TXA   impl -- --  01 01 FF FE 00100001\n" \
            " 307  6A  ROR      A -- --  80 01 FF FE 10100001\n" \
            " 308  A8  TAY   impl -- --  80 01 80 FE 10100001\n" \
            " 309  68  PLA   impl -- --  FD 01 80 FF 10100001\n" \
            " 30A  AA  TAX   impl -- --  FD FD 80 FF 10100001\n" \
            " 30B  00  BRK   impl -- --  FD FD 80 FC 10110101\n"
        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_sets_and_clears(self):

        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "38 18 F8 D8 78 58".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
            correct_output = \
                " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
                " 300  38  SEC   impl -- --  00 00 00 FF 00100001\n" \
                " 301  18  CLC   impl -- --  00 00 00 FF 00100000\n" \
                " 302  F8  SED   impl -- --  00 00 00 FF 00101000\n" \
                " 303  D8  CLD   impl -- --  00 00 00 FF 00100000\n" \
                " 304  78  SEI   impl -- --  00 00 00 FF 00100100\n" \
                " 305  58  CLI   impl -- --  00 00 00 FF 00100000\n" \
                " 306  00  BRK   impl -- --  00 00 00 FC 00110100\n"

            self.assertEqual(correct_output, f.getvalue())

            #windows specific attempt at running the program and testing the output aginst the documented intended output
            class TestInput(unittest.TestCase):
                def test_exit(self):
                    command_string = " more test1.in > 'python Monitor.py test1.obj' > test1result.out"
                    temp = os.system(command_string)

    def test_misc_implied_ops(self):
        # "300: CA CA 9A CA BA 08 C8 28 E8 8A 4A B8 00"
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "CA CA 9A CA BA 08 C8 28 E8 8A 4A B8 00".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)
            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
            correct_output = \
                " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
                " 300  CA  DEX   impl -- --  00 FF 00 FF 10100000\n" \
                " 301  CA  DEX   impl -- --  00 FE 00 FF 10100000\n" \
                " 302  9A  TXS   impl -- --  00 FE 00 FE 10100000\n" \
                " 303  CA  DEX   impl -- --  00 FD 00 FE 10100000\n" \
                " 304  BA  TSX   impl -- --  00 FE 00 FE 10100000\n" \
                " 305  08  PHP   impl -- --  00 FE 00 FD 10100000\n" \
                " 306  C8  INY   impl -- --  00 FE 01 FD 00100000\n" \
                " 307  28  PLP   impl -- --  00 FE 01 FE 10100000\n" \
                " 308  E8  INX   impl -- --  00 FF 01 FE 10100000\n" \
                " 309  8A  TXA   impl -- --  FF FF 01 FE 10100000\n" \
                " 30A  4A  LSR      A -- --  7F FF 01 FE 10100001\n" \
                " 30B  B8  CLV   impl -- --  7F FF 01 FE 10100001\n" \
                " 30C  00  BRK   impl -- --  7F FF 01 FB 10110101\n"
            self.maxDiff = None
            self.assertEqual(correct_output, f.getvalue())


if __name__ == '__main__':
    unittest.main()
