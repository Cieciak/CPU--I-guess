from utils import uint8
import ram

class CPU:

    def __init__(self) -> None:
        self.AX = uint8(0)
        self.BX = uint8(0)
        self.CX = uint8(0)
        self.DX = uint8(0)

        self.OV = 0

        self.ports = [0,0,0,0]

        # Address of next instruction
        self.PC = int(0)
        # Current instruction
        self.IR = uint8(0)
        # Address register
        self.AD = int(0)
        # Stack pointer
        self.SP = int(0)

        self.halt = False
        self.ram = ram.RAM(2 ** 16)
        self.reg_table = {
            0: self.AX,
            1: self.BX,
            2: self.CX,
            3: self.DX,
        }

    def __repr__(self):
        return f'AX {self.AX}\nBX {self.BX}\nCX {self.CX}\nDX {self.DX}\n OV {self.OV}'

    def fetch(self, dest = 'IR'):
        if dest == 'IR':
                self.IR = self.ram.read(self.PC)
        else:
            self.AD = self.AD * 256 + self.ram.read(self.PC).value
        self.PC += 1

    def execute(self):
        opcode, args = self.IR.split()

        # MOV
        if   opcode == 0b0001:
            DR, SR = args // 4, args % 4
            self.reg_table[DR].set(self.reg_table[SR])
        # LD
        elif opcode == 0b0010:
            self.fetch('AD')
            self.fetch('AD')
            DR = args // 4
            self.reg_table[DR].set(self.ram.read(self.AD))
            self.AD = 0
        # ST
        elif opcode == 0b0011:
            self.fetch('AD')
            self.fetch('AD')
            SR = args // 4
            self.ram.write(self.AD, self.reg_table[SR])
            self.AD = 0
        # NOT
        elif opcode == 0b0100:
            SR = args // 4
            self.reg_table[SR].set(~self.reg_table[SR])
        # ADD
        elif opcode == 0b0101:
            DR, SR = args // 4, args % 4
            self.reg_table[DR].set(self.reg_table[DR] + self.reg_table[SR])
            self.OV = int(self.reg_table[DR].overflow)
        # JMP
        elif opcode == 0b0110:
            self.fetch('AD')
            self.fetch('AD')
            self.PC = self.AD
            self.AD = 0
        # JO
        elif opcode == 0b0111:
            self.fetch('AD')
            self.fetch('AD')
            if self.OV:
                self.PC = self.AD
            self.AD = 0
        # OUT
        elif opcode == 0b1000:
            DP, SR = args // 4, args % 4
            self.ports[DP] = self.reg_table[SR]
        # IN
        elif opcode == 0b1001:
            DR, SP = args // 4, args % 4
            self.reg_table[DR].set(self.ports[SP])
        # MOI
        elif opcode == 0b1010:
            DR, IM = args // 4, args % 4
            self.reg_table[DR].set(uint8(IM))
        # PUSH
        elif opcode == 0b1011:
            SR = args // 4
            self.SP += 1
            self.ram.write(self.SP, self.reg_table[SR])
        # POP
        elif opcode == 0b1100:
            DR = args // 4
            self.reg_table[DR].set(self.ram.read(self.SP))
            self.SP -= 1
        # SET
        elif opcode == 0b1101:
            self.fetch('AD')
            self.fetch('AD')
            if args == 1: self.SP = self.AD
            self.AD = 0

        # HLT
        elif opcode == 0b1111:
            self.halt = True

if __name__ == '__main__':
    cpu = CPU()

    data = [209, 1, 0, 161, 176, 176, 196, 240]
    cpu.ram.load([uint8(x) for x in data])

    cpu.ram.write(0x20, uint8(0x5A))

    while not cpu.halt:
        cpu.fetch()
        cpu.execute()
        print(cpu, '\n')

    print(cpu.ram.data[0xF0:0x110])