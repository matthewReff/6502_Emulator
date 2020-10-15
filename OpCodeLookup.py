from Helper import Helper
from AddressingEnum import *
from OperationEnum import *


class OpCodeLookup:
    lookupTable = dict()

    # low byte 0
    lookupTable.update({0x00: (OperationEnum.BRK, AddressingEnum.impl),
    0x10: (OperationEnum.BPL, AddressingEnum.rel),
    0x20: (OperationEnum.JSR, AddressingEnum.abs),
    0x30: (OperationEnum.BMI, AddressingEnum.rel),
    0x40: (OperationEnum.RTI, AddressingEnum.impl),
    0x50: (OperationEnum.BVC, AddressingEnum.rel),
    0x60: (OperationEnum.RTS, AddressingEnum.impl),
    0x70: (OperationEnum.BVS, AddressingEnum.rel),
    0x90: (OperationEnum.BCC, AddressingEnum.rel),
    0xA0: (OperationEnum.LDY, AddressingEnum.imm),
    0xB0: (OperationEnum.BCS, AddressingEnum.rel),
    0xC0: (OperationEnum.CPY, AddressingEnum.imm),
    0xD0: (OperationEnum.BNE, AddressingEnum.rel),
    0xE0: (OperationEnum.CPX, AddressingEnum.imm),
    0xF0: (OperationEnum.BEQ, AddressingEnum.rel)})

    # low byte 1
    lookupTable.update({0x01: (OperationEnum.ORA, AddressingEnum.xInd),
    0x11: (OperationEnum.ORA, AddressingEnum.indY),
    0x21: (OperationEnum.AND, AddressingEnum.xInd),
    0x31: (OperationEnum.AND, AddressingEnum.indY),
    0x41: (OperationEnum.EOR, AddressingEnum.xInd),
    0x51: (OperationEnum.EOR, AddressingEnum.indY),
    0x61: (OperationEnum.ADC, AddressingEnum.xInd),
    0x71: (OperationEnum.ADC, AddressingEnum.indY),
    0x81: (OperationEnum.STA, AddressingEnum.xInd),
    0x91: (OperationEnum.STA, AddressingEnum.indY),
    0xA1: (OperationEnum.LDA, AddressingEnum.xInd),
    0xB1: (OperationEnum.LDA, AddressingEnum.indY),
    0xC1: (OperationEnum.CMP, AddressingEnum.xInd),
    0xD1: (OperationEnum.CMP, AddressingEnum.indY),
    0xE1: (OperationEnum.SBC, AddressingEnum.xInd),
    0xF1: (OperationEnum.SBC, AddressingEnum.indY)})

    # low byte 2
    lookupTable.update({0xA2: (OperationEnum.LDX, AddressingEnum.imm)})

    # low byte 4
    lookupTable.update({0x24: (OperationEnum.BIT, AddressingEnum.zpg),

    0x84: (OperationEnum.STY, AddressingEnum.zpg),
    0x94: (OperationEnum.STY, AddressingEnum.zpgX),
    0xA4: (OperationEnum.LDY, AddressingEnum.zpg),
    0xB4: (OperationEnum.LDY, AddressingEnum.zpgX),
    0xC4: (OperationEnum.CPY, AddressingEnum.zpg),
    0xE4: (OperationEnum.CPX, AddressingEnum.zpg)})

    # low byte 5
    lookupTable.update({0x05: (OperationEnum.ORA, AddressingEnum.zpg),
    0x15: (OperationEnum.ORA, AddressingEnum.zpgX),
    0x25: (OperationEnum.AND, AddressingEnum.zpg),
    0x35: (OperationEnum.AND, AddressingEnum.zpgX),
    0x45: (OperationEnum.EOR, AddressingEnum.zpg),
    0x55: (OperationEnum.EOR, AddressingEnum.zpgX),
    0x65: (OperationEnum.ADC, AddressingEnum.zpg),
    0x75: (OperationEnum.ADC, AddressingEnum.zpgX),
    0x85: (OperationEnum.STA, AddressingEnum.zpg),
    0x95: (OperationEnum.STA, AddressingEnum.zpgX),
    0xA5: (OperationEnum.LDA, AddressingEnum.zpg),
    0xB5: (OperationEnum.LDA, AddressingEnum.zpgX),
    0xC5: (OperationEnum.CMP, AddressingEnum.zpg),
    0xD5: (OperationEnum.CMP, AddressingEnum.zpgX),
    0xE5: (OperationEnum.SBC, AddressingEnum.zpg),
    0xF5: (OperationEnum.SBC, AddressingEnum.zpgX)})

    # low byte 6
    lookupTable.update({0x06: (OperationEnum.ASL, AddressingEnum.zpg),
    0x16: (OperationEnum.ASL, AddressingEnum.zpgX),
    0x26: (OperationEnum.ROL, AddressingEnum.zpg),
    0x36: (OperationEnum.ROL, AddressingEnum.zpgX),
    0x46: (OperationEnum.LSR, AddressingEnum.zpg),
    0x56: (OperationEnum.LSR, AddressingEnum.zpgX),
    0x66: (OperationEnum.ROR, AddressingEnum.zpg),
    0x76: (OperationEnum.ROR, AddressingEnum.zpgX),
    0x86: (OperationEnum.STX, AddressingEnum.zpg),
    0x96: (OperationEnum.STX, AddressingEnum.zpgY),
    0xA6: (OperationEnum.LDX, AddressingEnum.zpg),
    0xB6: (OperationEnum.LDX, AddressingEnum.zpgY),
    0xC6: (OperationEnum.DEC, AddressingEnum.zpg),
    0xD6: (OperationEnum.DEC, AddressingEnum.zpgX),
    0xE6: (OperationEnum.INC, AddressingEnum.zpg),
    0xF6: (OperationEnum.INC, AddressingEnum.zpgX)})

    # low byte 8
    lookupTable.update({0x08: (OperationEnum.PHP, AddressingEnum.impl),
    0x18: (OperationEnum.CLC, AddressingEnum.impl),
    0x28: (OperationEnum.PLP, AddressingEnum.impl),
    0x38: (OperationEnum.SEC, AddressingEnum.impl),
    0x48: (OperationEnum.PHA, AddressingEnum.impl),
    0x58: (OperationEnum.CLI, AddressingEnum.impl),
    0x68: (OperationEnum.PLA, AddressingEnum.impl),
    0x78: (OperationEnum.SEI, AddressingEnum.impl),
    0x88: (OperationEnum.DEY, AddressingEnum.impl),
    0x98: (OperationEnum.TYA, AddressingEnum.impl),
    0xA8: (OperationEnum.TAY, AddressingEnum.impl),
    0xB8: (OperationEnum.CLV, AddressingEnum.impl),
    0xC8: (OperationEnum.INY, AddressingEnum.impl),
    0xD8: (OperationEnum.CLD, AddressingEnum.impl),
    0xE8: (OperationEnum.INX, AddressingEnum.impl),
    0xF8: (OperationEnum.SED, AddressingEnum.impl)})

    # low byte 9
    lookupTable.update({0x09: (OperationEnum.ORA, AddressingEnum.imm),
    0x19: (OperationEnum.ORA, AddressingEnum.absY),
    0x29: (OperationEnum.AND, AddressingEnum.imm),
    0x39: (OperationEnum.AND, AddressingEnum.absY),
    0x49: (OperationEnum.EOR, AddressingEnum.imm),
    0x59: (OperationEnum.EOR, AddressingEnum.absY),
    0x69: (OperationEnum.ADC, AddressingEnum.imm),
    0x79: (OperationEnum.ADC, AddressingEnum.absY),
    0x99: (OperationEnum.STA, AddressingEnum.absY),
    0xA9: (OperationEnum.LDA, AddressingEnum.imm),
    0xB9: (OperationEnum.LDA, AddressingEnum.absY),
    0xC9: (OperationEnum.CMP, AddressingEnum.imm),
    0xD9: (OperationEnum.CMP, AddressingEnum.absY),
    0xE9: (OperationEnum.SBC, AddressingEnum.imm),
    0xF9: (OperationEnum.SBC, AddressingEnum.absY)})

    # low byte A
    lookupTable.update({0x0A: (OperationEnum.ASL, AddressingEnum.A),
    0x2A: (OperationEnum.ROL, AddressingEnum.A),
    0x4A: (OperationEnum.LSR, AddressingEnum.A),
    0x6A: (OperationEnum.ROR, AddressingEnum.A),
    0x8A: (OperationEnum.TXA, AddressingEnum.impl),
    0x9A: (OperationEnum.TXS, AddressingEnum.impl),
    0xAA: (OperationEnum.TAX, AddressingEnum.impl),
    0xBA: (OperationEnum.TSX, AddressingEnum.impl),
    0xCA: (OperationEnum.DEX, AddressingEnum.impl),
    0xEA: (OperationEnum.NOP, AddressingEnum.impl)})

    # low byte C
    lookupTable.update({0x2C: (OperationEnum.BIT, AddressingEnum.abs),
    0x4C: (OperationEnum.JMP, AddressingEnum.abs),
    0x6C: (OperationEnum.JMP, AddressingEnum.ind),
    0x8C: (OperationEnum.STY, AddressingEnum.abs),
    0xAC: (OperationEnum.LDY, AddressingEnum.abs),
    0xBC: (OperationEnum.LDY, AddressingEnum.absX),
    0xCC: (OperationEnum.CPY, AddressingEnum.abs),
    0xEC: (OperationEnum.CPX, AddressingEnum.abs)})

    # low byte D
    lookupTable.update({0x0D: (OperationEnum.ORA, AddressingEnum.abs),
    0x1D: (OperationEnum.ORA, AddressingEnum.absX),
    0x2D: (OperationEnum.AND, AddressingEnum.abs),
    0x3D: (OperationEnum.AND, AddressingEnum.absX),
    0x4D: (OperationEnum.EOR, AddressingEnum.abs),
    0x5D: (OperationEnum.EOR, AddressingEnum.absX),
    0x6D: (OperationEnum.ADC, AddressingEnum.abs),
    0x7D: (OperationEnum.ADC, AddressingEnum.absX),
    0x8D: (OperationEnum.STA, AddressingEnum.abs),
    0x9D: (OperationEnum.STA, AddressingEnum.absX),
    0xAD: (OperationEnum.LDA, AddressingEnum.abs),
    0xBD: (OperationEnum.LDA, AddressingEnum.absX),
    0xCD: (OperationEnum.CMP, AddressingEnum.abs),
    0xDD: (OperationEnum.CMP, AddressingEnum.absX),
    0xED: (OperationEnum.SBC, AddressingEnum.abs),
    0xFD: (OperationEnum.SBC, AddressingEnum.absX)})

    # low byte E
    lookupTable.update({0x0E: (OperationEnum.ASL, AddressingEnum.abs),
    0x1E: (OperationEnum.ASL, AddressingEnum.absX),
    0x2E: (OperationEnum.ROL, AddressingEnum.abs),
    0x3E: (OperationEnum.ROL, AddressingEnum.absX),
    0x4E: (OperationEnum.LSR, AddressingEnum.abs),
    0x5E: (OperationEnum.LSR, AddressingEnum.absX),
    0x6E: (OperationEnum.ROR, AddressingEnum.abs),
    0x7E: (OperationEnum.ROR, AddressingEnum.absX),
    0x8E: (OperationEnum.STX, AddressingEnum.abs),
    0xAE: (OperationEnum.LDX, AddressingEnum.abs),
    0xBE: (OperationEnum.LDX, AddressingEnum.absX),
    0xCE: (OperationEnum.DEC, AddressingEnum.abs),
    0xDE: (OperationEnum.DEC, AddressingEnum.absX),
    0xEE: (OperationEnum.INC, AddressingEnum.abs),
    0xFE: (OperationEnum.INC, AddressingEnum.absX)})
