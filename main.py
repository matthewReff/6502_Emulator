import sys


registers = dict()
mainMemory = bytearray(2 ** 16)


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


def parse_intel_hex(object_file_name):
    values = []
    with open(object_file_name, 'r') as obj_file:
        line = obj_file.readline()
        while line:
            start_code = line[0:1]
            byte_count = line[1:3]
            address = line[3:7]
            record_typr = line[7:9]
            bytes = get_decimal_number_from_hex_string(byte_count)
            currStart = 9;
            for i in range(0, bytes + 1):
                temp = line[currStart:currStart+2]
                currStart += 2
                values.append(get_decimal_number_from_hex_string(temp))
            check_sum = line[currStart:]
            #print(start_code)
            #print(byte_count)
            #print(values)
            #print (check_sum)
            load_values_to_memory(get_decimal_number_from_hex_string(address), values)
            line = obj_file.readline()


def display_registers():
    print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")
    constructed_string = " "
    constructed_string += get_hex_string_from_decimal_number(registers["PC"])
    constructed_string += "  "
    print(constructed_string)


def initialize_registers():
    registers["PC"] = 0
    registers["AC"] = 0
    registers["X"] = 0
    registers["Y"] = 0
    registers["SR"] = 0
    registers["SP"] = 0


def load_values_to_memory(starting_memory_location, values):
    for value in values:
        mainMemory[starting_memory_location] = value
        starting_memory_location += 1


def display_data_from_range(input_string):
    address_pair = input_string.split('.')
    begin_address = get_decimal_number_from_hex_string(address_pair[0])
    end_address = get_decimal_number_from_hex_string(address_pair[1])
    begin_address -= begin_address % 8

    for i in range(begin_address, end_address + 1):
        if i % 8 == 0:
            print(get_hex_string_from_decimal_number(i), end="   ")
        print(get_hex_string_from_decimal_number(mainMemory[i]), end=' ')
        if i % 8 == 7 or i == end_address:
            print()


def get_hex_string_from_decimal_number(number):
    display_number = hex(number)
    display_number = display_number.lstrip("0x")
    display_number = display_number.upper()
    while len(display_number) < 2:
        display_number = '0' + display_number
    return display_number


def get_decimal_number_from_hex_string(hex_string):
    number = int(hex_string, 16)
    return number


def main():
    initialize_registers()
    if len(sys.argv) == 2:
        parse_intel_hex(sys.argv[1])
    succeeded, input_string = prompt_for_input()
    while succeeded:
        if input_string.find('R') != -1:
            location = input_string.find('R')
            outString = input_string[0:location]
            memLoc = get_decimal_number_from_hex_string(outString)
            registers["PC"] = memLoc
            display_registers()
        elif input_string.find(':') != -1:
            location_values_pair = input_string.split(':')
            starting_memory_location = get_decimal_number_from_hex_string(location_values_pair[0])
            values = location_values_pair[1].strip().split(' ')
            converted_values = []
            for value in values:
                converted_values.append(get_decimal_number_from_hex_string(value))
            load_values_to_memory(starting_memory_location, converted_values)
        elif input_string.find('.') != -1:
            display_data_from_range(input_string)
        else:
            num = get_decimal_number_from_hex_string(input_string)
            print(get_hex_string_from_decimal_number(mainMemory[num]))

        succeeded, input_string = prompt_for_input()


NEGATIVE_BIT_MASK = 0x80;
OVERFLOW_BIT_MASK = 0x40;
BREAK_BIT_MASK = 0x10;
DECIMAL_BIT_MASK = 0x8;
INTERRUPT_BIT_MASK = 0x4;
ZERO_BIT_MASK = 0x2;
CARRY_BIT_MASK = 0x1;


if __name__ == "__main__":
    main()

