from enum import Enum, unique


@unique
class OperationEnum(Enum):
    ADC = 0
    AND = 1
    ASL = 2
    BCC = 3
    BCS = 4
    BEQ = 5
    BIT = 6
    BMI = 7
    BNE = 8
    BPL = 9
    BRK = 10
    BVC = 11
    BVS = 12
    CLC = 13
    CLD = 14
    CLI = 15
    CLV = 16
    CMP = 17
    CPX = 18
    CPY = 19
    DEC = 20
    DEX = 21
    DEY = 22
    EOR = 23
    INC = 24
    INX = 25
    JMP = 26
    JSR = 27
    LDA = 28
    LDX = 29
    LDY = 30
    LSR = 31
    NOP = 32
    ORA = 33
    PHA = 34
    PHP = 35
    PLA = 36
    PLP = 37
    ROL = 38
    ROR = 39
    RTI = 40
    RTS = 41
    SBC = 42
    SEC = 43
    SED = 44
    SEI = 45
    STA = 46
    STX = 47
    STY = 48
    TAX = 49
    TAY = 50
    TSX = 51
    TXA = 52
    TXS = 53
    TYA = 54

