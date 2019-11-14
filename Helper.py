
class Helper:
    @staticmethod
    def get_decimal_number_from_hex_string(hex_string):
        number = int(hex_string, 16)
        return number

    @staticmethod
    def get_hex_string_from_decimal_number(number):
        display_number = hex(number)
        display_number = display_number.lstrip("0x")
        display_number = display_number.upper()
        while len(display_number) < 2:
            display_number = '0' + display_number
        return display_number

    @staticmethod
    def get_twos_compliment(number):
        new_num_string = ""
        sanity_mask_string = ""
        for i in range(0, 8):
            if number & 1 == 1:
                new_num_string += "0"
            else:
                new_num_string += "1"
            number = number >> 1
            sanity_mask_string += "1"
        new_num_string = new_num_string[::-1]
        new_num = int(new_num_string, 2)
        new_num += 1
        sanity_mask = int(sanity_mask_string, 2)
        # TODO new_num &= sanity_mask
        return new_num
