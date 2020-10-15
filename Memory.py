from Helper import Helper
from OpCodeLookup import *


class Memory:
    FULL_BYTE_MASK = 0xFF
    NEGATIVE_BIT_MASK = 1 << 7
    OVERFLOW_BIT_MASK = 1 << 6
    DUMMY_BIT_MASK = 1 << 5
    BREAK_BIT_MASK = 1 << 4
    DECIMAL_BIT_MASK = 1 << 3
    INTERRUPT_BIT_MASK = 1 << 2
    ZERO_BIT_MASK = 1 << 1
    CARRY_BIT_MASK = 1 << 0

    def __init__(self):
        self.registers = dict()
        self.mainMemory = bytearray(2 ** 16)
        self.opCode = 0
        self.operand1 = None
        self.operand2 = None
        self.initialize_registers()

    @staticmethod
    def display_register_header():
        """print the formatted header which labels the content from the
registers"""
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")

    def display_registers(self, past_pc):
        """ prints the contents of the special registers in the format specified by
the project writeup"""
        constructed_string = ""
        pc_display = Helper.get_hex_string_from_decimal_number(past_pc)
        while len(pc_display) < 4:
            pc_display = " " + pc_display
        constructed_string += pc_display

        constructed_string += "  "
        constructed_string += Helper.get_hex_string_from_decimal_number(self.opCode)
        constructed_string += "  "
        constructed_string += str(OpCodeLookup.lookupTable[self.opCode][0].name)
        constructed_string += "  "
        address_spacing = str(OpCodeLookup.lookupTable[self.opCode][1].value[1])
        while len(address_spacing) < 5:
            address_spacing = " " + address_spacing
        constructed_string += address_spacing
        constructed_string += " "
        if self.operand1 is None:
            constructed_string += "--"
        else:
            constructed_string += Helper.get_hex_string_from_decimal_number(self.operand1)
        constructed_string += " "
        if self.operand2 is None:
            constructed_string += "--"
        else:
            constructed_string += Helper.get_hex_string_from_decimal_number(self.operand2)

        constructed_string += "  "
        constructed_string += Helper.get_hex_string_from_decimal_number(self.registers["AC"])
        constructed_string += " "
        constructed_string += Helper.get_hex_string_from_decimal_number(self.registers["X"])
        constructed_string += " "
        constructed_string += Helper.get_hex_string_from_decimal_number(self.registers["Y"])
        constructed_string += " "
        constructed_string += Helper.get_hex_string_from_decimal_number(self.registers["SP"])
        constructed_string += " "
        constructed_string += Helper.get_string_from_signed_byte(self.registers["SR"])
        print(constructed_string)

    def initialize_registers(self):
        """resets all special registers to default values"""
        self.registers["PC"] = 0
        self.registers["AC"] = 0
        self.registers["X"] = 0
        self.registers["Y"] = 0
        self.registers["SR"] = Memory.DUMMY_BIT_MASK
        self.registers["SP"] = 0xFF

    def save_values_to_memory(self, starting_memory_location, values):
        """takes in a starting location and a list of memory values, then
stores those values into memory starting at the starting location"""
        for value in values:
            self.mainMemory[starting_memory_location] = value
            starting_memory_location += 1

    def display_data_from_range(self, starting_address, end_address):
        """display the data in memory from the eight floored starting
value to the ending value. Format with 8 values per line and the memory location as a tag
before the eight values"""
        starting_address -= starting_address % 8

        for i in range(starting_address, end_address + 1):
            if i % 8 == 0:
                print(Helper.get_hex_string_from_decimal_number(i, 3), end="   ")
            print(Helper.get_hex_string_from_decimal_number(self.mainMemory[i]), end=' ')
            if i % 8 == 7 or i == end_address:
                print()

    def display_single_data(self, location):
        """display the data within memory at the given location"""
        print(Helper.get_hex_string_from_decimal_number(self.mainMemory[location]))

    def parse_intel_hex(self, object_file_name):
        """ loads a given file, interprets it as an intex hex file, and then passes
the parsed values to the memory setting function """
        values = []
        with open(object_file_name, 'r') as obj_file:
            line = obj_file.readline()
            while line:
                start_code = line[0:1]
                byte_count = line[1:3]
                address = line[3:7]
                record_type = line[7:9]
                num_bytes = Helper.get_decimal_number_from_hex_string(byte_count)
                curr_start = 9
                for i in range(0, num_bytes):
                    temp = line[curr_start:curr_start+2]
                    curr_start += 2
                    values.append(Helper.get_decimal_number_from_hex_string(temp))
                self.save_values_to_memory(Helper.get_decimal_number_from_hex_string(address), values)
                line = obj_file.readline()

    def push_to_stack(self, val):
        """push a value to the stack and decrement the stack pointer"""
        stack_pointer = self.registers["SP"]
        self.mainMemory[Helper.get_decimal_number_from_hex_string("100") + stack_pointer] = val
        self.registers["SP"] -= 1

    def pop_from_stack(self):
        """pop a value off the stack and increment the stack pointer"""
        self.registers["SP"] += 1
        stack_pointer = self.registers["SP"]
        val = self.mainMemory[Helper.get_decimal_number_from_hex_string("100") + stack_pointer]
        return val
