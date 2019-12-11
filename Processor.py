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
        branched = False
        arg1, data_context = Processor.resolve_params(memory, addressing_mode, param1, param2)

        if operation == OperationEnum.ASL:
            updated_bits = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, updated_bits)

            val = 0
            if data_context == DataContext.Value:
                val = memory.registers["AC"]
            else:
                val = memory.mainMemory[arg1]

            carry_bit = val >> 7
            value = val << 1
            value &= Memory.FULL_BYTE_MASK

            if addressing_mode == AddressingEnum.A:
                memory.registers["AC"] = value
            else:
                memory.mainMemory[arg1] = value

            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)

            if carry_bit == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

        elif operation == OperationEnum.BRK:
            value = memory.registers["PC"]
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
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = memory.registers["X"]
            val = Processor.add(memory, val, 1, subtract=True, update_status=False)
            val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)

            Processor.is_negative(memory, val_byte)
            Processor.is_zero(memory, val_byte)
            memory.registers["X"] = val_byte

        elif operation == OperationEnum.DEY:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = memory.registers["Y"]
            val = Processor.add(memory, val, 1, subtract=True, update_status=False)
            val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)

            Processor.is_negative(memory, val_byte)
            Processor.is_zero(memory, val_byte)
            memory.registers["Y"] = val_byte

        elif operation == OperationEnum.INX:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = memory.registers["X"]
            val = Processor.add(memory, val, 1, subtract=False, update_status=False)
            val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)

            Processor.is_negative(memory, val_byte)
            Processor.is_zero(memory, val_byte)
            memory.registers["X"] = val_byte

        elif operation == OperationEnum.INY:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = memory.registers["Y"]
            val = Processor.add(memory, val, 1, subtract=False, update_status=False)
            val_byte , is_overflow = Helper.get_signed_byte_from_decimal_int(val)

            Processor.is_negative(memory, val_byte)
            Processor.is_zero(memory, val_byte)
            memory.registers["Y"] = val_byte

        elif operation == OperationEnum.LSR:
            update_mask = memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            if addressing_mode == AddressingEnum.A:
                carry_bit = memory.registers["AC"] & 1
                if carry_bit == 1:
                    memory.registers["SR"] |= memory.CARRY_BIT_MASK
                memory.registers["AC"] = memory.registers["AC"] >> 1
                Processor.is_zero(memory, memory.registers["AC"])
            else:
                carry_bit = memory.mainMemory[arg1] & 1
                if carry_bit == 1:
                    memory.registers["SR"] |= memory.CARRY_BIT_MASK
                memory.mainMemory[arg1] = memory.mainMemory[arg1] >> 1
                Processor.is_zero(memory, memory.mainMemory[arg1])

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

            value = 0
            if data_context == DataContext.Value:
                value = memory.registers["AC"]
            else:
                value = memory.mainMemory[arg1]

            new_carry = value >> 7
            if new_carry == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

            value = value << 1
            lowest_bit_mask = Memory.FULL_BYTE_MASK ^ 1
            value &= lowest_bit_mask
            if old_carry != 0:
                value |= 1

            if data_context == DataContext.Value:
                memory.registers["AC"] = value
            else:
                memory.mainMemory[arg1] = value

            Processor.is_negative(memory, value)
            Processor.is_zero(memory, value)

        elif operation == OperationEnum.ROR:
            old_carry = memory.registers["SR"] & memory.CARRY_BIT_MASK
            update_mask = memory.NEGATIVE_BIT_MASK | memory.ZERO_BIT_MASK | memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            value = 0
            if data_context == DataContext.Value:
                value = memory.registers["AC"]
            else:
                value = memory.mainMemory[arg1]

            new_carry = value & 1
            if new_carry == 1:
                memory.registers["SR"] |= memory.CARRY_BIT_MASK

            value = value >> 1
            highest_bit_mask = Memory.FULL_BYTE_MASK ^ (1 << 8)
            value &= highest_bit_mask
            if old_carry != 0:
                value |= (1 << 7)

            if addressing_mode == AddressingEnum.A:
                memory.registers["AC"] = value
            else:
                memory.mainMemory[arg1] = value

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
            # Specifically don't reset the carry flag to mimic bug in hardware implementation
            carry_bit = memory.registers["SR"] & Memory.CARRY_BIT_MASK
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK  | Memory.OVERFLOW_BIT_MASK # | Memory.CARRY_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = 0
            if data_context == DataContext.Value:
                val = arg1
            else:
                val = memory.mainMemory[arg1]

            new_val = Helper.get_decimal_int_from_signed_byte(memory.registers["AC"]) + val
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
            if data_context == DataContext.Value:
                val = arg1
            else:
                val = memory.mainMemory[arg1]

            memory.registers["X"] = val
            Processor.is_zero(memory, memory.registers["X"])
            Processor.is_negative(memory, memory.registers["X"])

        elif operation == OperationEnum.LDA:
            Processor.generic_load(memory, "AC", arg1, data_context)

        elif operation == OperationEnum.INC:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = memory.mainMemory[arg1]
            val = Processor.add(memory, val, 1, subtract=False, update_status=False)
            mem_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)
            Processor.is_negative(memory, mem_byte)
            Processor.is_zero(memory, mem_byte)

            memory.mainMemory[arg1] = mem_byte

        elif operation == OperationEnum.EOR:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = 0
            if data_context == DataContext.Value:
                val = arg1
            else:
                val = memory.mainMemory[arg1]

            val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)
            memory.registers["AC"] ^= val_byte
            Processor.is_negative(memory, memory.registers["AC"])
            Processor.is_zero(memory, memory.registers["AC"])

        elif operation == OperationEnum.CMP:
            Processor.generic_compare(memory, "AC", arg1, data_context)

        elif operation == OperationEnum.CPX:
            Processor.generic_compare(memory, "X", arg1, data_context)

        elif operation == OperationEnum.CPY:
            Processor.generic_compare(memory, "Y", arg1, data_context)

        elif operation == OperationEnum.AND:
            update_mask = Memory.ZERO_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = 0
            if data_context == DataContext.Value:
                val = arg1
            else:
                val = memory.mainMemory[arg1]

            memory.registers["AC"] &= val
            Processor.is_negative(memory, memory.registers["AC"])
            Processor.is_zero(memory, memory.registers["AC"])

        elif operation == OperationEnum.LDX:
            Processor.generic_load(memory, "X", arg1, data_context)

        elif operation == OperationEnum.LDY:
            Processor.generic_load(memory, "Y", arg1, data_context)

        elif operation == OperationEnum.STX:
            Processor.generic_store(memory, "X", arg1)

        elif operation == OperationEnum.STY:
            Processor.generic_store(memory, "Y", arg1)

        elif operation == OperationEnum.STA:
            Processor.generic_store(memory, "AC", arg1)

        elif operation == OperationEnum.INC:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = memory.mainMemory[arg1]
            val_byte = Helper.get_signed_byte_from_decimal_int(val)
            one_byte = Helper.get_signed_byte_from_decimal_int(1)
            new_val = Processor.add(memory, val_byte, one_byte)
            memory.mainMemory[arg1] = new_val

        elif operation == OperationEnum.ORA:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)

            val = 0
            if data_context == DataContext.Value:
                val = arg1
            else:
                val = memory.mainMemory[arg1]

            val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)
            memory.registers["AC"] |= val_byte
            Processor.is_negative(memory, memory.registers["AC"])
            Processor.is_zero(memory, memory.registers["AC"])

        elif operation == OperationEnum.SBC:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK | Memory.CARRY_BIT_MASK | Memory.OVERFLOW_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            carry_bit = memory.registers["SR"] & Memory.CARRY_BIT_MASK

            val = 0
            if data_context == DataContext.Value:
                val = arg1
            else:
                val = memory.mainMemory[arg1]
            if carry_bit != 0:
                val -= 1

            new_val = Processor.add(memory, memory.registers["AC"], val, subtract=True, update_status=True)
            memory.registers["AC"], is_overflow = Helper.get_signed_byte_from_decimal_int(new_val)

        elif operation == OperationEnum.BIT:
            update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK | Memory.OVERFLOW_BIT_MASK
            Processor.clear_status_bits(memory, update_mask)
            val = memory.mainMemory[arg1]
            val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(val)

            new_overflow = (val_byte >> 6) & 1
            new_negative = (val_byte >> 7) & 1

            if new_negative != 0:
                memory.registers["SR"] |= Memory.NEGATIVE_BIT_MASK

            if new_overflow != 0:
                memory.registers["SR"] |= Memory.OVERFLOW_BIT_MASK

            accumulator_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(memory.registers["AC"])
            if accumulator_byte & val_byte == 0:
                memory.registers["SR"] |= Memory.ZERO_BIT_MASK

        elif operation == OperationEnum.DEC:
            val = memory.mainMemory[arg1]
            one_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(1)
            val = Processor.add(memory, val, one_byte, subtract=True, update_status=False)
            memory.mainMemory[arg1] = val

        elif operation == OperationEnum.RTS:
            branched = True
            hi = memory.pop_from_stack()
            lo = memory.pop_from_stack()
            lo_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(lo)
            hi_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(hi)
            val = Helper.combine_bytes(lo_byte=lo_byte, hi_byte=hi_byte)
            memory.registers["PC"] = val

        elif operation == OperationEnum.JMP:
            branched = True
            val = arg1
            if addressing_mode == AddressingEnum.ind:
                lo = memory.mainMemory[val]
                hi = memory.mainMemory[val+1]
                lo_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(lo)
                hi_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(hi)
                val = Helper.combine_bytes(lo_byte=lo_byte, hi_byte=hi_byte)

            memory.registers["PC"] = val

        elif operation == OperationEnum.BEQ:
            branched = Processor.generic_branch(memory, param1, mask=Memory.ZERO_BIT_MASK, is_set=True)

        elif operation == OperationEnum.BNE:
            branched = Processor.generic_branch(memory, param1, mask=Memory.ZERO_BIT_MASK, is_set=False)

        elif operation == OperationEnum.BCS:
            branched = Processor.generic_branch(memory, param1, mask=Memory.CARRY_BIT_MASK, is_set=True)

        elif operation == OperationEnum.BCC:
            branched = Processor.generic_branch(memory, param1, mask=Memory.CARRY_BIT_MASK, is_set=False)

        elif operation == OperationEnum.BMI:
            branched = Processor.generic_branch(memory, param1, mask=Memory.NEGATIVE_BIT_MASK, is_set=True)

        elif operation == OperationEnum.BPL:
            branched = Processor.generic_branch(memory, param1, mask=Memory.NEGATIVE_BIT_MASK, is_set=False)

        elif operation == OperationEnum.BVS:
            branched = Processor.generic_branch(memory, param1, mask=Memory.OVERFLOW_BIT_MASK, is_set=True)

        elif operation == OperationEnum.BVC:
            branched = Processor.generic_branch(memory, param1, mask=Memory.OVERFLOW_BIT_MASK, is_set=False)

        elif operation == OperationEnum.JSR:
            value = memory.registers["PC"]
            low_byte = value & Helper.get_decimal_number_from_hex_string("FF")
            high_byte = value & Helper.get_decimal_number_from_hex_string("FF00")
            high_byte = high_byte >> 8
            memory.push_to_stack(low_byte)
            memory.push_to_stack(high_byte)

            memory.registers["PC"] = arg1

        return branched

    @staticmethod
    def generic_store(memory, register, param1):
        memory.mainMemory[param1] = memory.registers[register]

    @staticmethod
    def generic_load(memory, register, param1, data_context):
        update_mask = Memory.NEGATIVE_BIT_MASK | Memory.ZERO_BIT_MASK
        Processor.clear_status_bits(memory, update_mask)

        val = 0
        if data_context == DataContext.Value:
            val = param1
        else:
            val = memory.mainMemory[param1]

        memory.registers[register] = val
        Processor.is_zero(memory, memory.registers[register])
        Processor.is_negative(memory, memory.registers[register])

    @staticmethod
    def generic_compare(memory, register, param1, data_context):
        carry_bit = memory.registers["SR"] & Memory.CARRY_BIT_MASK
        update_mask = Memory.ZERO_BIT_MASK | Memory.NEGATIVE_BIT_MASK | Memory.CARRY_BIT_MASK
        Processor.clear_status_bits(memory, update_mask)

        val = 0
        if data_context == DataContext.Value:
            val = param1
        else:
            val = memory.mainMemory[param1]

        val_num = Helper.get_decimal_int_from_signed_byte(val)

        temp = Processor.add(memory, memory.registers[register], val, True)

        # TODO rip off bandaid
        #if carry_bit == 0:
        #    Processor.clear_status_bits(memory, Memory.NEGATIVE_BIT_MASK)

    @staticmethod
    def add(memory, num1, num2, subtract=False, update_status=True):

        first_negative = Processor.is_negative(memory, num1)
        second_negative = Processor.is_negative(memory, num2)

        val1_string = Helper.get_string_from_signed_byte(num1)
        if subtract:
            num2 = Helper.get_twos_compliment(num2)
        val2_string = Helper.get_string_from_signed_byte(num2)

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

        if update_status:
            if carry == 1:
                memory.registers["SR"] |= Memory.CARRY_BIT_MASK

        new_val = Helper.get_decimal_int_from_signed_byte(int(finished_string, 2))
        new_val_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(new_val)
        Processor.is_zero(memory, new_val_byte)
        Processor.is_negative(memory, new_val_byte)

        return new_val

    @staticmethod
    def clear_status_bits(memory, mask_to_clear):
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
            prev_pc = memory.registers["PC"]

            num_args, arg1, arg2 = Processor.get_additional_args(memory, addressing_mode)
            memory.operand1 = arg1
            memory.operand2 = arg2
            memory.registers["PC"] += (1 + num_args)

            branched = Processor.ALU(memory, current_instruction, addressing_mode, arg1, arg2)
            memory.display_registers(prev_pc)

    @staticmethod
    def get_additional_args(memory, addressing_mode):
        base_PC = memory.registers["PC"]
        additional_args = 0
        arg1 = None
        arg2 = None

        if addressing_mode == AddressingEnum.imm:
            additional_args += 1

        elif addressing_mode == AddressingEnum.impl:
            additional_args = 0

        elif addressing_mode == AddressingEnum.zpg:
            additional_args += 1

        elif addressing_mode == AddressingEnum.zpgX:
            additional_args += 1

        elif addressing_mode == AddressingEnum.zpgY:
            additional_args += 1

        elif addressing_mode == AddressingEnum.ind:
            additional_args += 2

        elif addressing_mode == AddressingEnum.indY:
            additional_args += 1

        elif addressing_mode == AddressingEnum.xInd:
            additional_args += 1

        elif addressing_mode == AddressingEnum.rel:
            additional_args += 1

        elif addressing_mode == AddressingEnum.abs:
            additional_args += 2

        elif addressing_mode == AddressingEnum.absX:
            additional_args += 2

        elif addressing_mode == AddressingEnum.absY:
            additional_args += 2

        if additional_args > 0:
            arg1 = memory.mainMemory[base_PC + 1]
        if additional_args > 1:
            arg2 = memory.mainMemory[base_PC + 2]

        return additional_args, arg1, arg2

    @staticmethod
    def resolve_params(memory, addressing_mode, param1, param2):
        # params are bytes
        arg1 = param1
        context = DataContext.Index

        modify_val = 0
        if addressing_mode == AddressingEnum.abs or addressing_mode == AddressingEnum.absX or addressing_mode == AddressingEnum.absY:
            arg1 = Helper.combine_bytes(param1, param2)
            if addressing_mode == AddressingEnum.absX:
                modify_val = memory.registers["X"]
            elif addressing_mode == AddressingEnum.absY:
                modify_val = memory.registers["Y"]
            arg1 += modify_val

        elif addressing_mode == AddressingEnum.zpg or addressing_mode == AddressingEnum.zpgX or addressing_mode == AddressingEnum.zpgY:
            val = param1
            if addressing_mode == AddressingEnum.zpgX:
                val += memory.registers["X"]
            elif addressing_mode == AddressingEnum.zpgY:
                val += memory.registers["Y"]
            val &= Memory.FULL_BYTE_MASK
            arg1 = val

        elif addressing_mode == AddressingEnum.ind:
            param1_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(param1)
            param2_byte, is_overflow = Helper.get_signed_byte_from_decimal_int(param2)
            arg1 = Helper.combine_bytes(param1_byte, param2_byte)

        elif addressing_mode == AddressingEnum.indY:
            val = param1
            lo_byte = memory.mainMemory[val]
            hi_byte = memory.mainMemory[val + 1]
            val = Helper.combine_bytes(lo_byte, hi_byte)
            val += memory.registers["Y"]
            arg1 = val

        elif addressing_mode == AddressingEnum.xInd:
            val = param1
            val += memory.registers["X"]
            val &= Memory.FULL_BYTE_MASK
            lo_byte = memory.mainMemory[val]
            hi_byte = memory.mainMemory[val + 1]
            arg1 = Helper.combine_bytes(lo_byte, hi_byte)

        else:
            context = DataContext.Value

        return arg1, context

    @staticmethod
    def generic_branch(memory, location_byte, mask, is_set):
        branched = False
        location = Helper.get_decimal_int_from_signed_byte(location_byte)
        if (memory.registers["SR"] & mask != 0) == is_set:
            memory.registers["PC"] += location
            branched = True
        return branched
