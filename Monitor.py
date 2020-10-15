import sys
from Memory import *
from Processor import *


class Monitor:
    @staticmethod
    def main():
        """ Gets user input, translates to values actually usable to call functions, then calls
            those functions on the emulator"""
        emulator = Memory()
        emulator.initialize_registers()
        if len(sys.argv) == 2:
            emulator.parse_intel_hex(sys.argv[1])
        succeeded, input_string = Monitor.prompt_for_input()
        while succeeded:
            if input_string.find('R') != -1:
                location = input_string.find('R')
                out_string = input_string[0:location]
                mem_loc = Helper.get_decimal_number_from_hex_string(out_string)
                Processor.execute_at_location(emulator, mem_loc)

            elif input_string.find(':') != -1:
                location_values_pair = input_string.split(':')
                starting_memory_location = Helper.get_decimal_number_from_hex_string(location_values_pair[0])
                values = location_values_pair[1].strip().split(' ')

                converted_values = []
                for value in values:
                    converted_values.append(Helper.get_decimal_number_from_hex_string(value))
                emulator.save_values_to_memory(starting_memory_location, converted_values)

            elif input_string.find('.') != -1:
                address_pair = input_string.split('.')
                begin_address = Helper.get_decimal_number_from_hex_string(address_pair[0])
                end_address = Helper.get_decimal_number_from_hex_string(address_pair[1])
                emulator.display_data_from_range(begin_address, end_address)

            else:
                num = Helper.get_decimal_number_from_hex_string(input_string)
                emulator.display_single_data(num)

            succeeded, input_string = Monitor.prompt_for_input()

    @staticmethod
    def prompt_for_input():
        """ get a normal value from user and return true, or get an exit code and
return false"""
        try:
            entered_string = input("> ")
        except EOFError:
            return False, None
        except KeyboardInterrupt:
            return False, None

        if entered_string.upper() == "EXIT":
            return False, None

        return True, entered_string


def main():
    Monitor.main()


if __name__ == "__main__":
    main()
