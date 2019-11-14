from Helper import Helper
from OpCodeLookup import *


class Memory:
    registers = dict()

    mainMemory = bytearray(2 ** 16)
    opCode = 0
    operand1 = -1
    operand2 = -1
    FULL_BIT_MASK = 0xFF
    NEGATIVE_BIT_MASK = 0x80
    OVERFLOW_BIT_MASK = 0x40
    BREAK_BIT_MASK = 0x10
    DECIMAL_BIT_MASK = 0x8
    INTERRUPT_BIT_MASK = 0x4
    ZERO_BIT_MASK = 0x2
    CARRY_BIT_MASK = 0x1

    def display_registers(self):
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")
        constructed_string = " "
        constructed_string += Helper.get_hex_string_from_decimal_number(self.registers["PC"])
        constructed_string += "  "
        constructed_string += Helper.get_hex_string_from_decimal_number(self.opCode)
        constructed_string += "  "
        constructed_string += str(OpCodeLookup.lookupTable[self.opCode][0].name)
        constructed_string += "   "
        address_spacing = str(OpCodeLookup.lookupTable[self.opCode][1].name)
        while len(address_spacing) < 5:
            address_spacing += " "
        constructed_string += address_spacing
        address_spacing += " "
        if self.operand1 == -1:
            constructed_string += "--"
        else:
            constructed_string += Helper.get_hex_string_from_decimal_number(self.operand1)
        constructed_string += " "
        if self.operand2 == -1:
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
        shifting_val = self.registers["SR"]
        for i in range(0, 8):
            if i == 2:
                constructed_string += "1"
            else:
                constructed_string += str(shifting_val & 1)
            shifting_val = shifting_val >> 1
        print(constructed_string)

    def initialize_registers(self):
        self.registers["PC"] = 0
        self.registers["AC"] = 0
        self.registers["X"] = 0
        self.registers["Y"] = 0
        self.registers["SR"] = 0
        self.registers["SP"] = Helper.get_decimal_number_from_hex_string("FF")

    def save_values_to_memory(self, starting_memory_location, values):
        for value in values:
            self.mainMemory[starting_memory_location] = value
            starting_memory_location += 1

    def execute_at_location(self, starting_location):
        self.initialize_registers()
        self.registers["PC"] = starting_location
        self.display_registers()

    def display_data_from_range(self, starting_address, end_address):
        starting_address -= starting_address % 8

        for i in range(starting_address, end_address + 1):
            if i % 8 == 0:
                print(Helper.get_hex_string_from_decimal_number(i), end="   ")
            print(Helper.get_hex_string_from_decimal_number(self.mainMemory[i]), end=' ')
            if i % 8 == 7 or i == end_address:
                print()

    def display_single_data(self, location):
        print(Helper.get_hex_string_from_decimal_number(self.mainMemory[location]))

    def parse_intel_hex(self, object_file_name):
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
                for i in range(0, num_bytes + 1):
                    temp = line[curr_start:curr_start+2]
                    curr_start += 2
                    values.append(Helper.get_decimal_number_from_hex_string(temp))
                self.save_values_to_memory(Helper.get_decimal_number_from_hex_string(address), values)
                line = obj_file.readline()

    def push_to_stack(self, val):
        stack_pointer = self.registers["SP"]
        self.mainMemory[stack_pointer] = val
        self.registers["SP"] -= 1

    def pop_from_stack(self):
        self.registers["SP"] += 1
        stack_pointer = self.registers["SP"]
        val = self.mainMemory[stack_pointer]
        return val
