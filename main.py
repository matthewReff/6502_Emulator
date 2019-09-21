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


registers = dict()
mainMemory = bytearray(2 ** 16)

def clearMemory():
    registers["PC"] = 0
    registers["AC"] = 0
    registers["X"] = 0
    registers["Y"] = 0
    registers["SR"] = 0
    registers["SP"] = 0


def getHexStringFromDecimalNumber(number):
    display_number = hex(number)
    display_number = display_number.lstrip("0x")
    display_number = display_number.upper()
    while len(display_number) < 2:
        display_number = '0' + display_number
    return display_number


def main():
    clearMemory()
    succeeded, input_string = prompt_for_input()
    while succeeded:
        if input_string.find(':') != -1:
            locationValuesPair = input_string.split(':')
            memoryLoc = int(locationValuesPair[0], 16)
            values = locationValuesPair[1].strip().split(' ')
            for value in values:
                mainMemory[memoryLoc] = int(value, 16)
                memoryLoc += 1
        elif input_string.find('.') != -1:
            addressPair = input_string.split('.')
            beginAddress = int(addressPair[0], 16)
            endaddress = int(addressPair[1], 16)
            beginAddress -= beginAddress % 8

            for i in range(beginAddress, endaddress + 1):
                if i % 8 == 0:
                    print(getHexStringFromDecimalNumber(i), end="   ")
                print(getHexStringFromDecimalNumber(mainMemory[i]), end=' ')
                if i % 8 == 7 or i == endaddress:
                    print()
        else:
            num = int(input_string, 16)
            print(getHexStringFromDecimalNumber(mainMemory[num]))

        succeeded, input_string = prompt_for_input()


NEGATIVEBITMASK = 0x80;
OVERFLOWBITMASK = 0x40;
BREAKEBITMASK = 0x10;
DECIMALBITMASK = 0x8;
INTERUPTBITMASK = 0x4;
ZEROBITMASK = 0x2;
CARRYBITMASK = 0x1;



if __name__ == "__main__":
    main()

