
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


