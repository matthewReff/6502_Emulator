
class Helper:
    @staticmethod
    def get_decimal_number_from_hex_string(hex_string):
        """Get the decimal values of a string interpreted as
hexadecimal"""
        number = int(hex_string, 16)
        return number

    @staticmethod
    def get_hex_string_from_decimal_number(number, length=2):
        """Convert a base 10 value to an appropriately
formatted hex string"""
        display_number = hex(number)
        display_number = display_number.lstrip("0x")
        display_number = display_number.upper()
        while len(display_number) < length:
            display_number = '0' + display_number
        return display_number

    @staticmethod
    def get_signed_byte_from_decimal_int(decimal_int):
        """Convert a base 10 integer to a signed byte"""
        is_overflow = False
        if decimal_int > 127 or decimal_int < -128:
            is_overflow = True
        decimal_int &= 0b11111111

        was_negative = False
        if decimal_int < 0:
            was_negative = True
            decimal_int *= -1
        construct_string = "0"
        for i in range(7, -1, -1):
            if decimal_int - (1 << i) >= 0:
                construct_string += "1"
                decimal_int -= (1 << i)
            else:
                construct_string += "0"
        new_byte = int(construct_string, 2)
        if was_negative:
            new_byte = Helper.get_twos_compliment(new_byte)
        return new_byte, is_overflow

    @staticmethod
    def get_string_from_signed_byte(byte):
        """Convert the binary of a signed byte into a string"""
        construct_string = ""
        for i in range(7, -1, -1):
            if byte - (1 << i) >= 0:
                construct_string += "1"
                byte -= (1 << i)
            else:
                construct_string += "0"
        return construct_string

    @staticmethod
    def get_decimal_int_from_signed_byte(signed_byte):
        """Convert a signed byte to a base 10 int"""
        new_val = 0
        if signed_byte >> 7 == 1:
            new_val = Helper.get_twos_compliment(signed_byte)
            new_val *= -1
        else:
            new_val = signed_byte
        return new_val

    @staticmethod
    def get_twos_compliment(number):
        """Converts a signed byte to its opposite signed value"""
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
        #sanity_mask = int(sanity_mask_string, 2)
        #new_num &= sanity_mask
        return new_num

    @staticmethod
    def get_ones_compliment(number):
        """Converts a signed byte’s bits to be used with compares"""
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
        sanity_mask = int(sanity_mask_string, 2)
        new_num &= sanity_mask
        return new_num

    @staticmethod
    def combine_bytes(lo_byte, hi_byte):
        """Turn a lo_byte and hi_byte in a decimal int"""
        hi_string = Helper.get_string_from_signed_byte(hi_byte)
        lo_string = Helper.get_string_from_signed_byte(lo_byte)

        return int(hi_string + lo_string, 2)