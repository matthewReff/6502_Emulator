import Memory
from AddressingEnum import *
from OperationEnum import *
from OpCodeLookup import *
from Memory import *


class Processor:
    # TODO pass in memory on processor load
    def __init__(self, memory):
        self._memory = memory

    @staticmethod
    def ALU(memory, op_code):
        operation = OpCodeLookup.lookupTable[op_code][0]
        addressing_mode = OpCodeLookup.lookupTable[op_code][1]

        if operation == OperationEnum.ASL:
            updated_bits = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, updated_bits)

            carry_bit = memory.registers["AC"] >> 7
            value = memory.registers["AC"] << 1
            value &= memory.FULL_BIT_MASK
            memory.registers["AC"] = value

            Processor.is_negative(memory, memory.registers["AC"])
            Processor.is_zero(memory, memory.registers["AC"])

            if carry_bit == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

        elif operation == OperationEnum.BRK:
            value = memory.registers["PC"] + 2
            low_byte = value & Helper.get_decimal_number_from_hex_string("FF")
            high_byte = value & Helper.get_decimal_number_from_hex_string("FF00")
            high_byte = high_byte >> 8
            memory.push_to_stack(high_byte)
            memory.push_to_stack(low_byte)
            memory.push_to_stack(memory.registers["SR"])
            memory.registers["SR"] = memory.INTERRUPT_BIT_MASK | memory.BREAK_BIT_MASK | memory.registers["SR"]

        elif operation == OperationEnum.CLC:
            update_mask = memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.CLD:
            update_mask = memory.DECIMAL_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.CLI:
            update_mask = memory.INTERRUPT_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.CLV:
            update_mask = memory.OVERFLOW_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.DEX:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.registers["X"]
            value = Helper.get_decimal_int_from_signed_byte(value)
            value -= 1
            value = Helper.get_signed_byte_from_decimal_int(value)
            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)
            memory.registers["X"] = value

        elif operation == OperationEnum.DEY:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.registers["Y"]
            value = Helper.get_decimal_int_from_signed_byte(value)
            value -= 1
            value = Helper.get_signed_byte_from_decimal_int(value)
            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)
            memory.registers["Y"] = value

        elif operation == OperationEnum.INX:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.registers["X"]
            if Processor.is_negative(memory, memory.registers["X"]):
                value = Helper.get_twos_compliment(value)
                value -= 1
                value = Helper.get_twos_compliment(value)
            else:
                value += 1
            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)
            memory.registers["X"] = value

        elif operation == OperationEnum.INY:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.registers["Y"]
            if Processor.is_negative(memory, memory.registers["Y"]):
                value = Helper.get_twos_compliment(value)
                value -= 1
                value = Helper.get_twos_compliment(value)
            else:
                value += 1
            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)
            memory.registers["Y"] = value

        elif operation == OperationEnum.LSR:
            update_mask = memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            carry_bit = memory.registers["AC"] & 1
            if carry_bit == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK
            memory.registers["AC"] = memory.registers["AC"] >> 1
            Processor.is_zero(memory, memory.registers["AC"])

        elif operation == OperationEnum.NOP:
            pass

        elif operation == OperationEnum.PHA:
            memory.push_to_stack(memory.registers["AC"])

        elif operation == OperationEnum.PHP:
            memory.push_to_stack(memory.registers["SR"])

        elif operation == OperationEnum.PLA:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.pop_from_stack()
            memory.registers["AC"] = value
            Processor.is_zero(memory, value)
            Processor.is_negative(memory, value)

        elif operation == OperationEnum.PLP:
            value = memory.pop_from_stack()
            memory.registers["SR"] = value

        elif operation == OperationEnum.ROL:
            # change to be a ASL including carry bit
            old_carry = memory.registers["SR"] & memory.CARRY_BIT_MASK
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.registers["AC"]
            new_carry = value >> 7
            if new_carry == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

            value = value << 1
            lowest_bit_mask = memory.FULL_BIT_MASK ^ 1
            value &= lowest_bit_mask
            if old_carry != 0:
                value |= 1

            memory.registers["AC"] = value
            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)

        elif operation == OperationEnum.ROR:
            old_carry = memory.registers["SR"] & memory.CARRY_BIT_MASK
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.registers["AC"]
            new_carry = value & 1
            if new_carry == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

            value = value >> 1
            highest_bit_mask = memory.FULL_BIT_MASK ^ (1 << 8)
            value &= highest_bit_mask
            if old_carry != 0:
                value |= (1 << 7)

            memory.registers["AC"] = value
            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)

        elif operation == OperationEnum.SEC:
            memory.registers["SR"] |= memory.CARRY_BIT_MASK

        elif operation == OperationEnum.SED:
            memory.registers["SR"] |= memory.DECIMAL_BIT_MASK

        elif operation == OperationEnum.SEI:
            memory.registers["SR"] |= memory.INTERRUPT_BIT_MASK

        elif operation == OperationEnum.TAX:
            memory.registers["X"] = memory.registers["AC"]
            Processor.is_zero(memory, memory.registers["X"])
            Processor.is_negative(memory, memory.registers["X"])

        elif operation == OperationEnum.TAY:
            memory.registers["Y"] = memory.registers["AC"]
            Processor.is_zero(memory, memory.registers["Y"])
            Processor.is_negative(memory, memory.registers["Y"])

        elif operation == OperationEnum.TSX:
            memory.registers["X"] = memory.registers["SP"]
            Processor.is_negative(memory, memory.registers["X"])
            Processor.is_zero(memory, memory.registers["X"])

        elif operation == OperationEnum.TXA:
            memory.registers["AC"] = memory.registers["X"]
            Processor.is_zero(memory, memory.registers["AC"])
            Processor.is_negative(memory, memory.registers["AC"])

        elif operation == OperationEnum.TYA:
            memory.registers["AC"] = memory.registers["Y"]
            Processor.is_zero(memory, memory.registers["AC"])
            Processor.is_negative(memory, memory.registers["AC"])

        elif operation == OperationEnum.TXS:
            memory.registers["SP"] = memory.registers["X"]

    @staticmethod
    def clear_status_bits(memory, mask_to_clear):
#        clear_mask = Memory.FULL_BIT_MASK ^ mask_to_clear
        clear_mask = 0xFF ^ mask_to_clear
        memory.registers["SR"] &= clear_mask

    @staticmethod
    def is_negative(memory, value):
        if value >> 7 & 1 == 1:
            memory.registers["SR"] |= memory.NEGATIVE_BIT_MASK
            return True
        else:
            Processor.clear_status_bits(memory, Memory.NEGATIVE_BIT_MASK)
            return False

    @staticmethod
    def is_zero(memory, value):
        if value == 0:
            memory.registers["SR"] |= memory.ZERO_BIT_MASK
            return True
        else:
            Processor.clear_status_bits(memory, Memory.ZERO_BIT_MASK)
            return False

    @staticmethod
    def execute_at_location(memory, starting_location):
        memory.initialize_registers()
        memory.registers["PC"] = starting_location
        current_instruction = OperationEnum.NONE
        memory.display_register_header()
        while current_instruction != OperationEnum.BRK:
            op_code = memory.mainMemory[memory.registers["PC"]]
            memory.opCode = op_code
            decode_tuple = OpCodeLookup.lookupTable[op_code]
            current_instruction = decode_tuple[0]
            addressing_mode = decode_tuple[1]
            Processor.ALU(memory, op_code)
            memory.display_registers()
            memory.registers["PC"] += 1

