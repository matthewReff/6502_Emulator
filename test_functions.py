import unittest
from unittest import mock
from Helper import *
from Memory import *
from Monitor import *
from contextlib import redirect_stdout
import io
import sys
import os
from multiprocessing import Process
import time
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

    def test_add(self):
        thing1 = 0b00000001
        thing2 = 0b00000001
        tempMem = Memory()
        result = Processor.add(tempMem, thing1, thing2)

        self.assertEqual(2, result)
        self.assertEqual(Memory.DUMMY_BIT_MASK, tempMem.registers["SR"])


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

        correct_output =  \
                           "300   A9 04 85 07 A0 00 84 06 \n" \
                           "308   A9 A0 91 06 C8 D0 FB E6 \n" \
                           "310   07 \n"
        self.assertEqual(correct_output, f.getvalue())


class RunProgram(unittest.TestCase):
    def test_run_program(self):

        memory = Memory()
        f = io.StringIO()
        with redirect_stdout(f):
            Processor.execute_at_location(memory, Helper.get_decimal_number_from_hex_string("300"))
            "123456789012345678901234567890123456789012345690"
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC"
        correct_output = " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
                         " 300  00  BRK   impl -- --  00 00 00 FC 00110100\n"
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

        self.assertEqual(SUT.mainMemory[Helper.get_decimal_number_from_hex_string("100") + SUT.registers["SP"]+1], 10)
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

    def test_example_run_3(self):
        # "300: 69 10 A2 02 85 02 E6 02 A50200"
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "69 10 A2 02 85 02 E6 02 A5 02 00".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  69  ADC      # 10 --  10 00 00 FF 00100000\n" \
            " 302  A2  LDX      # 02 --  10 02 00 FF 00100000\n" \
            " 304  85  STA    zpg 02 --  10 02 00 FF 00100000\n" \
            " 306  E6  INC    zpg 02 --  10 02 00 FF 00100000\n" \
            " 308  A5  LDA    zpg 02 --  11 02 00 FF 00100000\n" \
            " 30A  00  BRK   impl -- --  11 02 00 FC 00110100\n"
        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_example_run_4(self):
        # "300: A9 AA 49 55 C9 00 69 01 C9 01"
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "A9 AA 49 55 C9 00 69 01 C9 01".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  A9  LDA      # AA --  AA 00 00 FF 10100000\n" \
            " 302  49  EOR      # 55 --  FF 00 00 FF 10100000\n" \
            " 304  C9  CMP      # 00 --  FF 00 00 FF 00100001\n" \
            " 306  69  ADC      # 01 --  01 00 00 FF 00100001\n" \
            " 308  C9  CMP      # 01 --  01 00 00 FF 00100011\n" \
            " 30A  00  BRK   impl -- --  01 00 00 FC 00110111\n"
        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_example_run_5(self):
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("000")
            test_values = []
            for i in "01 03 05 07 09 0B 0D 0F".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "A5 02 25 07 A6 03 86 08 E6 08 46 00".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
            SUT.display_data_from_range(Helper.get_decimal_number_from_hex_string("000"), Helper.get_decimal_number_from_hex_string("00F"))
        correct_output = \
           " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
           " 300  A5  LDA    zpg 02 --  05 00 00 FF 00100000\n" \
           " 302  25  AND    zpg 07 --  05 00 00 FF 00100000\n" \
           " 304  A6  LDX    zpg 03 --  05 07 00 FF 00100000\n" \
           " 306  86  STX    zpg 08 --  05 07 00 FF 00100000\n" \
           " 308  E6  INC    zpg 08 --  05 07 00 FF 00100000\n" \
           " 30A  46  LSR    zpg 00 --  05 07 00 FF 00100011\n" \
           " 30C  00  BRK   impl -- --  05 07 00 FC 00110111\n" \
           "000   00 03 05 07 09 0B 0D 0F \n" \
           "008   08 00 00 00 00 00 00 00 \n"

        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_remaining_immediate_and_zero_page(self):
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()

            starting = Helper.get_decimal_number_from_hex_string("000")
            test_values = []
            for i in "01 01 01 01 01 01 01 01 "\
                     "01 01 01 01 01 01 01 01".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "09 01 A0 03 A2 03 38 E9 01 65 00 06 01 A0 FF 84 07 24 07 C6 02 45 03 A4 04 A6 05 46 06 05 07 " \
                     "26 08 66 09 E5 0A 00".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
            SUT.display_data_from_range(Helper.get_decimal_number_from_hex_string("000"), Helper.get_decimal_number_from_hex_string("00F"))

        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  09  ORA      # 01 --  01 00 00 FF 00100000\n" \
            " 302  A0  LDY      # 03 --  01 00 03 FF 00100000\n" \
            " 304  A2  LDX      # 03 --  01 03 03 FF 00100000\n" \
            " 306  38  SEC   impl -- --  01 03 03 FF 00100001\n" \
            " 307  E9  SBC      # 01 --  00 03 03 FF 00100011\n" \
            " 309  65  ADC    zpg 00 --  02 03 03 FF 00100001\n" \
            " 30B  06  ASL    zpg 01 --  02 03 03 FF 00100000\n" \
            " 30D  A0  LDY      # FF --  02 03 FF FF 10100000\n" \
            " 30F  84  STY    zpg 07 --  02 03 FF FF 10100000\n" \
            " 311  24  BIT    zpg 07 --  02 03 FF FF 11100000\n" \
            " 313  C6  DEC    zpg 02 --  02 03 FF FF 01100010\n" \
            " 315  45  EOR    zpg 03 --  03 03 FF FF 01100000\n" \
            " 317  A4  LDY    zpg 04 --  03 03 01 FF 01100000\n" \
            " 319  A6  LDX    zpg 05 --  03 01 01 FF 01100000\n" \
            " 31B  46  LSR    zpg 06 --  03 01 01 FF 01100011\n" \
            " 31D  05  ORA    zpg 07 --  FF 01 01 FF 11100001\n" \
            " 31F  26  ROL    zpg 08 --  FF 01 01 FF 01100000\n" \
            " 321  66  ROR    zpg 09 --  FF 01 01 FF 01100011\n" \
            " 323  E5  SBC    zpg 0A --  FE 01 01 FF 10100001\n" \
            " 325  00  BRK   impl -- --  FE 01 01 FC 10110101\n" \
            "000   01 02 00 01 01 01 00 FF \n" \
            "008   03 00 01 01 01 01 01 01 \n"

        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_example_run_6(self):
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "AD 09 03 6D 13 03 D0 02 00 05 6C 16 03 20 14 03 00 90 FA 05 60 00 11 03".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
        correct_output = \
           " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
           " 300  AD  LDA    abs 09 03  05 00 00 FF 00100000\n" \
           " 303  6D  ADC    abs 13 03  0A 00 00 FF 00100000\n" \
           " 306  D0  BNE    rel 02 --  0A 00 00 FF 00100000\n" \
           " 30A  6C  JMP    ind 16 03  0A 00 00 FF 00100000\n" \
           " 311  90  BCC    rel FA --  0A 00 00 FF 00100000\n" \
           " 30D  20  JSR    abs 14 03  0A 00 00 FD 00100000\n" \
           " 314  60  RTS   impl -- --  0A 00 00 FF 00100000\n" \
           " 310  00  BRK   impl -- --  0A 00 00 FC 00110100\n"
        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_example_run_7(self):
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()

            starting = Helper.get_decimal_number_from_hex_string("1000")
            test_values = []
            for i in "01 03 05 07 09 0B 0D 0F 00 02 04 06 08 0A 0C 0E 10 30 50 70 90 B0 D0 F0 00 20 40 60 80 A0 C0 E0".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "AD 00 10 0D 13 10 8D 20 10 6D 06 10 6D 10 10 2C 20 10 0E 1D 10 6E 09 10".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
            SUT.display_data_from_range(Helper.get_decimal_number_from_hex_string("1000"), Helper.get_decimal_number_from_hex_string("1027"))

        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" \
            " 303  0D  ORA    abs 13 10  71 00 00 FF 00100000\n" \
            " 306  8D  STA    abs 20 10  71 00 00 FF 00100000\n" \
            " 309  6D  ADC    abs 06 10  7E 00 00 FF 00100000\n" \
            " 30C  6D  ADC    abs 10 10  8E 00 00 FF 11100000\n" \
            " 30F  2C  BIT    abs 20 10  8E 00 00 FF 01100010\n" \
            " 312  0E  ASL    abs 1D 10  8E 00 00 FF 01100001\n" \
            " 315  6E  ROR    abs 09 10  8E 00 00 FF 11100000\n" \
            " 318  00  BRK   impl -- --  8E 00 00 FC 11110100\n" \
            "1000   01 03 05 07 09 0B 0D 0F \n" \
            "1008   00 81 04 06 08 0A 0C 0E \n" \
            "1010   10 30 50 70 90 B0 D0 F0 \n" \
            "1018   00 20 40 60 80 40 C0 E0 \n" \
            "1020   71 00 00 00 00 00 00 00 \n"

        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_inf_run(self):
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "A9 01 85 00 18 2A A5 00 8D 00 80 A2 03 A0 03 88 D0 FD CA D0 F8 4C 05 03".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            action_process = Process(target=Processor.execute_at_location, args=(SUT, Helper.get_decimal_number_from_hex_string("300")))
            action_process.start()
            action_process.join(timeout=1)
            #assert still alive after a full second
            self.assertTrue(action_process.is_alive())
            action_process.terminate()

        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  A9  LDA      # 01 --  01 00 00 FF 00100000\n" \
            " 302  85  STA    zpg 00 --  01 00 00 FF 00100000\n" \
            " 304  18  CLC   impl -- --  01 00 00 FF 00100000\n" \
            " 305  2A  ROL      A -- --  02 00 00 FF 00100000\n" \
            " 306  A5  LDA    zpg 00 --  01 00 00 FF 00100000\n" \
            " 308  8D  STA    abs 00 80  01 00 00 FF 00100000\n" \
            " 30B  A2  LDX      # 03 --  01 03 00 FF 00100000\n" \
            " 30D  A0  LDY      # 03 --  01 03 03 FF 00100000\n" \
            " 30F  88  DEY   impl -- --  01 03 02 FF 00100000\n" \
            " 310  D0  BNE    rel FD --  01 03 02 FF 00100000\n" \
            " 30F  88  DEY   impl -- --  01 03 01 FF 00100000\n" \
            " 310  D0  BNE    rel FD --  01 03 01 FF 00100000\n" \
            " 30F  88  DEY   impl -- --  01 03 00 FF 00100010\n" \
            " 310  D0  BNE    rel FD --  01 03 01 FF 00100010\n" \
            " 312  CA  DEX   impl -- --  01 02 00 FF 00100000\n" \
            " 313  D0  BNE    rel F8 --  01 02 00 FF 00100000\n" \
            " 30D  A0  LDY      # 03 --  01 02 03 FF 00100000\n" \
            " 310  D0  BNE    rel FD --  01 02 02 FF 00100000\n" \
            " 30F  88  DEY   impl -- --  01 02 01 FF 00100000\n" \
            " 310  D0  BNE    rel FD --  01 02 01 FF 00100000\n" \
            " 30F  88  DEY   impl -- --  01 02 00 FF 00100010\n" \
            " 310  D0  BNE    rel FD --  01 02 01 FF 00100010\n" \
            " 312  CA  DEX   impl -- --  01 01 00 FF 00100000\n" \
            " 313  D0  BNE    rel F8 --  01 01 00 FF 00100000\n" \
            " 30D  A0  LDY      # 03 --  01 01 03 FF 00100000\n" \
            " 310  D0  BNE    rel FD --  01 01 02 FF 00100000\n" \
            " 30F  88  DEY   impl -- --  01 01 01 FF 00100000\n" \
            " 310  D0  BNE    rel FD --  01 01 01 FF 00100000\n" \
            " 30F  88  DEY   impl -- --  01 01 00 FF 00100010\n" \
            " 310  D0  BNE    rel FD --  01 01 01 FF 00100010\n" \
            " 312  CA  DEX   impl -- --  01 00 00 FF 00100010\n" \
            " 313  D0  BNE    rel F8 --  01 00 00 FF 00100010\n" \
            " 315  4C  JMP    abs 05 03  01 00 00 FF 00100010\n" \
            " 305  2A  ROL      A -- --  02 00 00 FF 00100000\n" \
            " 306  A5  LDA    zpg 00 --  01 00 00 FF 00100000\n"

    def test_example_run_8(self):
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()

            starting = Helper.get_decimal_number_from_hex_string("000")
            test_values = []
            for i in "00 00 00 00 00 FF 00 00".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            starting = Helper.get_decimal_number_from_hex_string("100")
            test_values = []
            for i in "00 11 22 33 44 55 66 77".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "A2 01 A0 01 A9 05 85 01 8C 05 07 A1 00 86 02 A2 0A 8E 04 07 B1 01".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
            SUT.display_data_from_range(Helper.get_decimal_number_from_hex_string("0000"), Helper.get_decimal_number_from_hex_string("007"))
            SUT.display_data_from_range(Helper.get_decimal_number_from_hex_string("0100"), Helper.get_decimal_number_from_hex_string("0107"))
            SUT.display_data_from_range(Helper.get_decimal_number_from_hex_string("0700"), Helper.get_decimal_number_from_hex_string("0707"))

        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  A2  LDX      # 01 --  00 01 00 FF 00100000\n" \
            " 302  A0  LDY      # 01 --  00 01 01 FF 00100000\n" \
            " 304  A9  LDA      # 05 --  05 01 01 FF 00100000\n" \
            " 306  85  STA    zpg 01 --  05 01 01 FF 00100000\n" \
            " 308  8C  STY    abs 05 07  05 01 01 FF 00100000\n" \
            " 30B  A1  LDA  x,ind 00 --  FF 01 01 FF 10100000\n" \
            " 30D  86  STX    zpg 02 --  FF 01 01 FF 10100000\n" \
            " 30F  A2  LDX      # 0A --  FF 0A 01 FF 00100000\n" \
            " 311  8E  STX    abs 04 07  FF 0A 01 FF 00100000\n" \
            " 314  B1  LDA  ind,y 01 --  66 0A 01 FF 00100000\n" \
            " 316  00  BRK   impl -- --  66 0A 01 FC 00110100\n" \
            "000   00 05 01 00 00 FF 00 00 \n" \
            "100   00 11 22 33 44 55 66 77 \n" \
            "700   00 00 00 00 0A 01 00 00 \n" \

        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

    def test_example_run_9(self):
        f = io.StringIO()
        with redirect_stdout(f):
            SUT = Memory()
            starting = Helper.get_decimal_number_from_hex_string("300")
            test_values = []
            for i in "A9 60 8D ED FD A2 00 BD 18 03 20 ED FD E8 E0 03 90 F5 A9 8D 20 ED FD 00 1A 2B 3C".split(" "):
                test_values.append(Helper.get_decimal_number_from_hex_string(i))
            SUT.save_values_to_memory(starting, test_values)

            Processor.execute_at_location(SUT, Helper.get_decimal_number_from_hex_string("300"))
        correct_output = \
            " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" \
            " 300  A9  LDA      # 60 --  60 00 00 FF 00100000\n" \
            " 302  8D  STA    abs ED FD  60 00 00 FF 00100000\n" \
            " 305  A2  LDX      # 00 --  60 00 00 FF 00100010\n" \
            " 307  BD  LDA  abs,x 18 03  1A 00 00 FF 00100000\n" \
            " 30A  20  JSR    abs ED FD  1A 00 00 FD 00100000\n" \
            "FDED  60  RTS   impl -- --  1A 00 00 FF 00100000\n" \
            " 30D  E8  INX   impl -- --  1A 01 00 FF 00100000\n" \
            " 30E  E0  CPX      # 03 --  1A 01 00 FF 10100000\n" \
            " 310  90  BCC    rel F5 --  1A 01 00 FF 10100000\n" \
            " 307  BD  LDA  abs,x 18 03  2B 01 00 FF 00100000\n" \
            " 30A  20  JSR    abs ED FD  2B 01 00 FD 00100000\n" \
            "FDED  60  RTS   impl -- --  2B 01 00 FF 00100000\n" \
            " 30D  E8  INX   impl -- --  2B 02 00 FF 00100000\n" \
            " 30E  E0  CPX      # 03 --  2B 02 00 FF 10100000\n" \
            " 310  90  BCC    rel F5 --  2B 02 00 FF 10100000\n" \
            " 307  BD  LDA  abs,x 18 03  3C 02 00 FF 00100000\n" \
            " 30A  20  JSR    abs ED FD  3C 02 00 FD 00100000\n" \
            "FDED  60  RTS   impl -- --  3C 02 00 FF 00100000\n" \
            " 30D  E8  INX   impl -- --  3C 03 00 FF 00100000\n" \
            " 30E  E0  CPX      # 03 --  3C 03 00 FF 00100011\n" \
            " 310  90  BCC    rel F5 --  3C 03 00 FF 00100011\n" \
            " 312  A9  LDA      # 8D --  8D 03 00 FF 10100001\n" \
            " 314  20  JSR    abs ED FD  8D 03 00 FD 10100001\n" \
            "FDED  60  RTS   impl -- --  8D 03 00 FF 10100001\n" \
            " 317  00  BRK   impl -- --  8D 03 00 FC 10110101\n"
        self.maxDiff = None
        self.assertEqual(correct_output, f.getvalue())

if __name__ == '__main__':
    unittest.main()
