
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list) or isinstance(item, tuple):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def MOV(dst: int, src: int):
    return 0b0001_0000 + (dst << 2) + (src)

def LD(dst: int, address: int):
    return 0b0010_0000 + (dst << 2), address // 256, address % 256

def ST(src: int, address: int):
    return 0b0011_0000 + (src << 2), address // 256, address % 256

def NOT(reg: int):
    return 0b0100_0000 + (reg << 2)

def ADD(dst: int, src: int):
    return 0b0101_0000 + (dst << 2) + src

def JMP(address: int):
    return 0b0110_0000, address // 256, address % 256

def JO(address: int):
    return 0b0111_0000, address // 256, address % 256

def OUT(port: int, reg: int):
    return 0b1000_0000 + (port << 2) + reg

def IN(port: int, reg: int):
    return 0b1001_0000 + (reg << 2) + port

def MOI(reg: int, imm: int):
    return 0b1010_0000 + (reg << 2) + imm

def PUSH(reg: int):
    return 0b1011_0000 + (reg << 2)

def POP(reg: int):
    return 0b1100_0000 + (reg << 2)

def SET(imm: int, address: int):
    return 0b1101_0000 + imm, address // 256, address % 256

def HLT():
    return 0b1111_0000

if __name__ == '__main__':
    program = [
        SET(1, 0x100),
        MOI(0, 1),
        PUSH(0),
        PUSH(0),
        POP(1),
        HLT(),
    ]

    print(flatten(program))