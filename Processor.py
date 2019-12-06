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
    def ALU(memory, operation, addressing_mode, param1=None, param2=None):
        #modify addresses to fit with addressing mode
        if addressing_mode == AddressingEnum.zpg:
            param1 &= Memory.FULL_BIT_MASK





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
            value, is_overflow = Helper.get_signed_byte_from_decimal_int(value)
            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)
            memory.registers["X"] = value

        elif operation == OperationEnum.DEY:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            value = memory.registers["Y"]
            value = Helper.get_decimal_int_from_signed_byte(value)
            value -= 1
            value, is_overflow = Helper.get_signed_byte_from_decimal_int(value)
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

        elif operation == OperationEnum.ADC:
            carry_bit = memory.registers["SR"] & Memory.CARRY_BIT_MASK
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK | Memory.CARRY_BIT_MASK | Memory.OVERFLOW_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            new_val = Helper.get_decimal_int_from_signed_byte( memory.registers["AC"]) + param1
            if carry_bit != 0:
                new_val += 1

            byte_val, is_overflow = Helper.get_signed_byte_from_decimal_int(new_val)
            byte_val = int(byte_val)
            Processor.is_negative(memory, byte_val)
            Processor.is_zero(memory, byte_val)
            if is_overflow:
                memory.registers["SR"] |= Memory.OVERFLOW_BIT_MASK
            memory.registers["AC"] = byte_val

        elif operation == OperationEnum.LDX:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = 0
            if addressing_mode == AddressingEnum.imm:
                val = param1
            else:
                val = memory.mainMemory[param1]

            memory.registers["X"] = val
            Processor.is_zero(memory, memory.registers["X"])
            Processor.is_negative(memory, memory.registers["X"])

        elif operation == OperationEnum.LDA:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = 0
            if addressing_mode == AddressingEnum.imm:
                val = param1
            else:
                val = memory.mainMemory[param1]
            memory.registers["AC"] = val
            Processor.is_zero(memory, memory.registers["AC"])
            Processor.is_negative(memory, memory.registers["AC"])

        elif operation == OperationEnum.STA:
            memory.mainMemory[param1] = memory.registers["AC"]

        elif operation == OperationEnum.INC:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            mem_val = Helper.get_decimal_int_from_signed_byte(memory.mainMemory[param1])
            mem_val += 1
            mem_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(mem_val)
            Processor.is_negative(memory, mem_byte)
            Processor.is_zero(memory, mem_byte)

            memory.mainMemory[param1] = mem_byte

        elif operation == OperationEnum.EOR:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = 0
            if addressing_mode == AddressingEnum.imm:
                val = param1
            else:
                val = memory.mainMemory[param1]

            val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)
            memory.registers["AC"] ^= val_byte
            Processor.is_negative(memory, memory.registers["AC"])
            Processor.is_zero(memory, memory.registers["AC"])

        elif operation == OperationEnum.CMP:
            Processor.generic_compare(memory, addressing_mode, "AC", param1, param2)

        elif operation == OperationEnum.CPX:
            Processor.generic_compare(memory, addressing_mode, "X", param1, param2)

        elif operation == OperationEnum.CPY:
            Processor.generic_compare(memory, addressing_mode, "Y", param1, param2)

    @staticmethod
    def generic_compare(memory, addressing_mode, register, param1, param2):
    # add two's comp to register
        new_val = Processor.add(memory, memory.registers[register], Helper.get_twos_compliment(param1))
        Processor.is_zero(memory, new_val)
        Processor.is_negative(memory, new_val)

    @staticmethod
    def add(memory, num1, num2):
        val1, is_overflow = Helper.get_signed_byte_from_decimal_int(num1)
        val2, is_overflow = Helper.get_signed_byte_from_decimal_int(num2)

        val1_string = Helper.get_string_from_signed_byte(val1)
        val2_string = Helper.get_string_from_signed_byte(val2)

        carry = 0
        finished_string = ""
        for i in range(7, -1, -1):
            val = int(val1_string[i], 2) + int(val2_string[i], 2) + carry
            if val >= 2:
                carry = 1
                val -= 2
            else:
                carry = 0
            finished_string = str(val) + finished_string
        if carry == 1:
            memory.registers["SR"] |= Memory.CARRY_BIT_MASK
        return int(finished_string, 2)

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

            num_args, arg1, arg2 = Processor.get_additional_args(memory, addressing_mode)
            memory.operand1 = arg1
            memory.operand2 = arg2
            Processor.ALU(memory, current_instruction, addressing_mode, arg1, arg2)
            memory.display_registers()
            memory.registers["PC"] += (1 + num_args)

    @staticmethod
    def get_additional_args(memory, addressing_mode):
        base_PC = memory.registers["PC"]
        additional_args = 0
        arg1 = None
        arg2 = None

        if addressing_mode == AddressingEnum.imm:
            additional_args += 1
            arg1 = memory.mainMemory[base_PC + 1]
        elif addressing_mode == AddressingEnum.impl:
            additional_args = 0

        elif addressing_mode == AddressingEnum.zpg:
            additional_args += 1
            arg1 = memory.mainMemory[base_PC +1]
        return additional_args, arg1, arg2
