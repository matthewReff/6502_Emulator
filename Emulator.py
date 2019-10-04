class T34Emulator:
    registers = dict()
    mainMemory = bytearray(2 ** 16)
    NEGATIVE_BIT_MASK = 0x80;
    OVERFLOW_BIT_MASK = 0x40;
    BREAK_BIT_MASK = 0x10;
    DECIMAL_BIT_MASK = 0x8;
    INTERRUPT_BIT_MASK = 0x4;
    ZERO_BIT_MASK = 0x2;
    CARRY_BIT_MASK = 0x1;

    @staticmethod
    def prompt_for_input():
        try:
            temp = input("> ")
        except EOFError:
            return False, None
        except KeyboardInterrupt:
            return False, None

        if temp.upper() == "EXIT":
            return False, None

        return True, temp

    def parse_intel_hex(self, object_file_name):
        values = []
        with open(object_file_name, 'r') as obj_file:
            line = obj_file.readline()
            while line:
                start_code = line[0:1]
                byte_count = line[1:3]
                address = line[3:7]
                record_typr = line[7:9]
                bytes = self.get_decimal_number_from_hex_string(byte_count)
                currStart = 9;
                for i in range(0, bytes + 1):
                    temp = line[currStart:currStart+2]
                    currStart += 2
                    values.append(self.get_decimal_number_from_hex_string(temp))
                check_sum = line[currStart:]
                #print(start_code)
                #print(byte_count)
                #print(values)
                #print (check_sum)
                self.load_values_to_memory(self.get_decimal_number_from_hex_string(address), values)
                line = obj_file.readline()

    def display_registers(self):
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")
        constructed_string = " "
        constructed_string += self.get_hex_string_from_decimal_number(self.registers["PC"])
        constructed_string += "  "
        print(constructed_string)

    def initialize_registers(self):
        self.registers["PC"] = 0
        self.registers["AC"] = 0
        self.registers["X"] = 0
        self.registers["Y"] = 0
        self.registers["SR"] = 0
        self.registers["SP"] = 0

    def load_values_to_memory(self, starting_memory_location, values):
        for value in values:
            self.mainMemory[starting_memory_location] = value
            starting_memory_location += 1

    def display_data_from_range(self, starting_address, end_address):
        starting_address -= starting_address % 8

        for i in range(starting_address, end_address + 1):
            if i % 8 == 0:
                print(self.get_hex_string_from_decimal_number(i), end="   ")
            print(self.get_hex_string_from_decimal_number(self.mainMemory[i]), end=' ')
            if i % 8 == 7 or i == end_address:
                print()

    def display_single_data(self, location):
        print(T34Emulator.get_hex_string_from_decimal_number(self.mainMemory[location]))

    @staticmethod
    def get_hex_string_from_decimal_number(number):
        display_number = hex(number)
        display_number = display_number.lstrip("0x")
        display_number = display_number.upper()
        while len(display_number) < 2:
            display_number = '0' + display_number
        return display_number

    @staticmethod
    def get_decimal_number_from_hex_string(hex_string):
        number = int(hex_string, 16)
        return number
