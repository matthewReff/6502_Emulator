import sys
from Emulator import *


def main():
    emulator = T34Emulator()
    emulator.initialize_registers()
    if len(sys.argv) == 2:
        emulator.parse_intel_hex(sys.argv[1])
    succeeded, input_string = emulator.prompt_for_input()
    while succeeded:
        if input_string.find('R') != -1:
            location = input_string.find('R')
            out_string = input_string[0:location]
            mem_loc = T34Emulator.get_decimal_number_from_hex_string(out_string)
            emulator.begin_executation(mem_loc)

        elif input_string.find(':') != -1:
            location_values_pair = input_string.split(':')
            starting_memory_location = T34Emulator.get_decimal_number_from_hex_string(location_values_pair[0])
            values = location_values_pair[1].strip().split(' ')

            converted_values = []
            for value in values:
                converted_values.append(T34Emulator.get_decimal_number_from_hex_string(value))
            emulator.save_values_to_memory(starting_memory_location, converted_values)

        elif input_string.find('.') != -1:
            address_pair = input_string.split('.')
            begin_address = T34Emulator.get_decimal_number_from_hex_string(address_pair[0])
            end_address = T34Emulator.get_decimal_number_from_hex_string(address_pair[1])
            emulator.display_data_from_range(begin_address, end_address)

        else:
            num = T34Emulator.get_decimal_number_from_hex_string(input_string)
            emulator.display_single_data(num)

        succeeded, input_string = emulator.prompt_for_input()


if __name__ == "__main__":
    main()
