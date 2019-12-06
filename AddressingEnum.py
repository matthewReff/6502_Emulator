from enum import Enum, unique

@unique
class AddressingEnum(Enum):
    A = (0, "A")
    abs = (1, "abs")
    absX = (2, "abs,X")
    absY = (3, "abs,Y")
    imm = (4, "#")
    impl = (5, "impl")
    ind = (6, "ind")
    xInd = (7, "X,ind")
    indY = (8, "ind,Y")
    rel = (9, "rel")
    zpg = (10, "zpg")
    zpgX = (11, "zpg,X")
    zpgY = (12, "zpg,Y")