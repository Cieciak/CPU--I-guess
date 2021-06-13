from ram import RAM
from disk import Disk
import os


class CPU:

    def __init__(self):
        self.ax = 0
        self.ir = 0
        self.dr = 0

    def __repr__(self):
        out =  f'AX: {self.ax}\n'
        out += f'IR: {self.ir}\n'
        out += f'DR: {self.dr}'
        return out

    def get_instruction(self, memory: RAM):
        self.ir = memory.read(self.dr)
        self.dr += 1

    def execute(self, memory: RAM):
        opcode = self.ir // 16
        args = self.ir % 16

        # Do nothing
        if opcode == 0:
            pass

        # Move value to reg ax
        elif opcode == 1:
            self.ax = r.read(args)
        
        # Move value from reg ax to ram
        elif opcode == 2:
            r.write(args, self.ax)

        # Add
        elif opcode == 3:
            self.ax += r.read(args)
        
        # Jump
        elif opcode == 4:
            self.dr = args
        
        # Jump if zero
        elif opcode == 5:
            if self.ax == 0:
                self.dr = args

        # Subtract
        elif opcode == 6:
            self.ax -= r.read(args)

        # 

        # Halt
        elif opcode == 15:
            print('CPU Halted!')
            quit()


test = CPU()
os.system('cls')

r = RAM(16)
r.write(15, 15 * 16)

r.write(14, 1)
r.write(0, 3*16 + 14)
r.write(2, 5*16)


os.system('cls')
while True:
    input()
    os.system('cls')
    test.get_instruction(r)
    print(test)
    print(r)
    test.execute(r)
