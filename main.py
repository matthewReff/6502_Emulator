import sys
from Emulator import *


def main():
    thing = T34Emulator()
    thing.initialize_registers()
    if len(sys.argv) == 2:
        thing.parse_intel_hex(sys.argv[1])
    succeeded, input_string = thing.prompt_for_input()
    while succeeded:
        if input_string.find('R') != -1:
            location = input_string.find('R')
            outString = input_string[0:location]
            memLoc = T34Emulator.get_decimal_number_from_hex_string(outString)
            thing.registers["PC"] = memLoc
            thing.display_registers()
        elif input_string.find(':') != -1:
            location_values_pair = input_string.split(':')
            starting_memory_location = T34Emulator.get_decimal_number_from_hex_string(location_values_pair[0])
            values = location_values_pair[1].strip().split(' ')
            converted_values = []
            for value in values:
                converted_values.append(T34Emulator.get_decimal_number_from_hex_string(value))
            thing.load_values_to_memory(starting_memory_location, converted_values)
        elif input_string.find('.') != -1:
           thing.display_data_from_range(input_string)
        else:
            num = T34Emulator.get_decimal_number_from_hex_string(input_string)
            print(T34Emulator.get_hex_string_from_decimal_number(thing.mainMemory[num]))

        succeeded, input_string = thing.prompt_for_input()


if __name__ == "__main__":
    main()

