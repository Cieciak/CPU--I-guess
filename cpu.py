from ram import RAM
import os


class CPU:

    def __init__(self):
        self.ax = 0
        self.bx = 0
        self.ir = 0
        self.dr = 0

    def __repr__(self):
        out =  f'AX: {self.ax}\n'
        out += f'BX: {self.bx}\n'
        out += f'IR: {self.ir}\n'
        out += f'DR: {self.dr}'
        return out

    def get_instruction(self, memory: RAM):
        self.ir = memory.read(self.dr)
        self.dr += 1

    def execute(self, memory: RAM):
        opcode = self.ir // 16
        args = self.ir % 16
        if opcode == 0:
            pass
        elif opcode == 1:
            self.ax = r.read(args)
        elif opcode == 2:
            r.write(args, self.ax)
        elif opcode == 3:
            self.ax += r.read(args)
        elif opcode == 4:
            self.dr = args
        elif opcode == 15:
            print('CPU Halted!')
            quit()


test = CPU()
os.system('cls')

r = RAM(16)
r.write(15, 15 * 16)

r.write(14, 1)
r.write(0, 3*16 + 14)
r.write(2, 4*16)


os.system('cls')
while True:
    input()
    test.get_instruction(r)
    print(test)
    print(r)
    test.execute(r)