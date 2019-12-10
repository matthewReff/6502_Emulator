from enum import Enum, unique

@unique
class AddressingEnum(Enum):
    A = (0, "A")
    abs = (1, "abs")
    absX = (2, "abs,x")
    absY = (3, "abs,y")
    imm = (4, "#")
    impl = (5, "impl")
    ind = (6, "ind")
    xInd = (7, "x,ind")
    indY = (8, "ind,y")
    rel = (9, "rel")
    zpg = (10, "zpg")
    zpgX = (11, "zpg,x")
    zpgY = (12, "zpg,y")