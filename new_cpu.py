from better_ram import RAM


class CPU:

    def __init__(self):
        self.ax = 0
        self.bx = 0
        self.dx = 0
        self.cx = 0

        self.lr = 0
        
        self.ir = 0
        self.dr = 0

    def __repr__(self) -> str:
        out =  f'AX: {self.ax}\n'
        out += f'BX: {self.bx}\n'
        out += f'CX: {self.cx}\n'
        out += f'DX: {self.dx}\n'
        out += f'IR: {self.ir}\n'
        out += f'DR: {self.dr}'

        return out

    def get_instruction(self, ram: RAM):
        self.ir = ram.read_quad_word(self.dr)
        self.dr += 8

    def execute(self, ram: RAM):
        opcode = self.ir // (2**32)
        args = self.ir % (2**32)

        if opcode == 0:
            pass
        elif opcode == 1:
            self.ax = ram.read_quad_word(args)
        elif opcode == 2:
            self.bx = ram.read_quad_word(args)
        elif opcode == 3:
            self.cx = ram.read_quad_word(args)
        elif opcode == 4:
            self.dx = ram.read_quad_word(args)
        elif opcode == 5:
            self.ax = self.ax - self.bx
        elif opcode == 6:
            self.ax += self.bx
        elif opcode == 7:
            self.dr = args
        elif opcode == 15:
            print('CPU Halted!')
            quit()


proc = CPU()
ram = RAM(1024)

# Halt 
ram.write_quad_word(1016, 15 << 32)

# Vars
ram.write_quad_word(1008, 0)
ram.write_quad_word(1000, 1)

# Program starts here
ram.write_quad_word(8, (1 << 32) + 1008)
ram.write_quad_word(16, (2 << 32) + 1000)
ram.write_quad_word(24, (6 << 32))
ram.write_quad_word(32, (7 << 32) + 24)

while True:
    input()
    proc.get_instruction(ram)
    proc.execute(ram)
    print(ram)
    print(proc)
    
