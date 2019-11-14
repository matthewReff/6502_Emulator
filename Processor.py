from AddressingEnum import *
from OperationEnum import *
from OpCodeLookup import *
from Memory import *


class Processor:
    def ALU(self, op_code, memory):
        operation = OpCodeLookup.lookupTable[op_code][0]
        addressing_mode = OpCodeLookup.lookupTable[op_code][1]

        if operation == OperationEnum.ASL:
            updated_bits = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            self.clear_status_bits(memory, updated_bits)

            carry_bit = memory.registers["AC"] >> 7
            memory.registers["AC"] = memory.registers["AC"] << 1

            Processor.is_negative(memory, memory.registers["AC"])
            Processor.is_zero(memory, memory.registers["AC"])

            if carry_bit == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

        elif operation == OperationEnum.BRK:
            memory.registers["SR"] = memory.INTERRUPT_BIT_MASK | memory.registers["SR"]
            memory.push_to_stack(memory.registers["SP"] + 2)
            memory.push_to_stack(memory.registers["SR"])

        elif operation == OperationEnum.CLC:
            update_mask = memory.CARRY_BIT_MASK
            self.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.CLD:
            update_mask = memory.DECIMAL_BIT_MASK
            self.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.CLI:
            update_mask = memory.INTERRUPT_BIT_MASK
            self.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.CLV:
            update_mask = memory.OVERFLOW_BIT_MASK
            self.clear_status_bits(memory, update_mask)

        elif operation == OperationEnum.DEX:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            self.clear_status_bits(memory, update_mask)
            value = memory.registers["X"]
            if self.is_negative(memory, memory.registers["X"]):
                value = Helper.get_twos_compliment(value)
                value += 1
                value = Helper.get_twos_compliment(value)
            else:
                value -= 1
            self.is_negative(memory, value)
            self.is_zero(memory, value)
            memory.registers["X"] = value

        elif operation == OperationEnum.DEY:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            self.clear_status_bits(memory, update_mask)
            value = memory.registers["Y"]
            if self.is_negative(memory, memory.registers["Y"]):
                value = Helper.get_twos_compliment(value)
                value += 1
                value = Helper.get_twos_compliment(value)
            else:
                value -= 1
            self.is_negative(memory, value)
            self.is_zero(memory, value)
            memory.registers["Y"] = value

        elif operation == OperationEnum.INX:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            self.clear_status_bits(memory, update_mask)
            value = memory.registers["X"]
            if self.is_negative(memory, memory.registers["X"]):
                value = Helper.get_twos_compliment(value)
                value -= 1
                value = Helper.get_twos_compliment(value)
            else:
                value += 1
            self.is_negative(memory, value)
            self.is_zero(memory, value)
            memory.registers["X"] = value

        elif operation == OperationEnum.INY:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            self.clear_status_bits(memory, update_mask)
            value = memory.registers["Y"]
            if self.is_negative(memory, memory.registers["Y"]):
                value = Helper.get_twos_compliment(value)
                value -= 1
                value = Helper.get_twos_compliment(value)
            else:
                value += 1
            self.is_negative(memory, value)
            self.is_zero(memory, value)
            memory.registers["Y"] = value

        elif operation == OperationEnum.LSR:
            update_mask = memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            self.clear_status_bits(update_mask)
            carry_bit = memory.registers["AC"] & 1
            if carry_bit == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK
            memory.registers["AC"] = memory.registers["AC"] >> 1
            self.is_zero(memory.registers["AC"])

        elif operation == OperationEnum.NOP:
            pass

        elif operation == OperationEnum.PHA:
            memory.push_to_stack(memory.registers["AC"])

        elif operation == OperationEnum.PHP:
            memory.push_to_stack(memory.registers["SR"])

        elif operation == OperationEnum.PLA:
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK
            self.clear_status_bits(memory, update_mask)
            value = memory.pop_from_stack()
            memory.registers["AC"] = value
            self.is_zero(memory, value)
            self.is_negative(memory, value)

        elif operation == OperationEnum.PHP:
            value = memory.pop_from_stack()
            memory.registers["SR"] = value

        elif operation == OperationEnum.ROL:
            # change to be a ASL including carry bit
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            self.clear_status_bits(memory, update_mask)
            value = memory.registers["AC"]
            old_carry = memory.registers["SR"] & memory.CARRY_BIT_MASK
            new_carry = value >> 7
            if new_carry == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

            value = value << 1
            lowest_bit_mask = memory.FULL_BIT_MASK ^ 1
            value &= lowest_bit_mask
            if old_carry != 0:
                value |= 1

            self.is_negative(value)
            self.is_zero(value)

    @staticmethod
    def clear_status_bits(memory, mask_to_clear):
        clear_mask = Memory.FULL_BIT_MASK ^ mask_to_clear
        memory.registers["SR"] &= clear_mask

    @staticmethod
    def is_negative(memory, value):
        if value >> 7 & 1 == 1:
            memory.registers["SR"] |= memory.NEGATIVE_BIT_MASK
            return True
        else:
            return False

    @staticmethod
    def is_zero(memory, value):
        if value == 0:
            memory.registers["SR"] |= memory.ZERO_BIT_MASK
            return True
        else:
            return False
