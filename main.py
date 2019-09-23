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

def display_registers():
    print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BSIZC")
    constructedString = " "
    constructedString += get_hex_string_from_decimal_number(registers["PC"])
    constructedString += "  "
    print(constructedString)


def clear_memory():
    registers["PC"] = 0
    registers["AC"] = 0
    registers["X"] = 0
    registers["Y"] = 0
    registers["SR"] = 0
    registers["SP"] = 0


def load_values_to_memory(input_string):
    location_values_pair = input_string.split(':')
    starting_memory_location = get_decimal_number_from_hex_string(location_values_pair[0])
    values = location_values_pair[1].strip().split(' ')
    for value in values:
        mainMemory[starting_memory_location] = get_decimal_number_from_hex_string(value)
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
    clear_memory()
    succeeded, input_string = prompt_for_input()
    while succeeded:
        if input_string.find('R') != -1:
            location = input_string.find('R')
            outString = input_string[0:location]
            memLoc = get_decimal_number_from_hex_string(outString)
            registers["PC"] = memLoc
            display_registers()
        elif input_string.find(':') != -1:
            load_values_to_memory(input_string)
        elif input_string.find('.') != -1:
            display_data_from_range(input_string)
        else:
            num = int(input_string, 16)
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

