from ram import RAM
from basics import int8
from gpu import GPU
import time
import os

class CPU:

    def __init__(self):
        self.ar = int8(0)
        self.xr = int8(0)
        self.ir = int8(0)
        self.dr = int(0)

        self.stack = []
        self.address_stack = 0

    def fetch(self, ram: RAM, place = 'ir'):
        if place == 'ir':
            self.ir = int8(ram.read(self.dr))
        else:
            self.address_stack = self.address_stack * 256 + ram.read(self.dr)
        self.dr += 1

    def execute(self, ram: RAM):
        opcode, arg = self.ir.split()

        # MOV
        if opcode == 0b0001:
            if arg == 0b0000:
                self.xr = self.ar
            elif arg == 0b1000:
                self.ar = self.xr

        # LDF  
        elif opcode == 0b0010:
            if arg == 0b0000:
                self.fetch(ram, 0)
                self.fetch(ram, 0)
                self.ar = int8(ram.read(self.address_stack))
                self.address_stack = 0
            elif arg == 0b1000:
                self.fetch(ram, 0)
                self.fetch(ram, 0)
                self.xr = int8(ram.read(self.address_stack))
                self.address_stack = 0

        # LDT
        elif opcode == 0b0011:
            if arg == 0b0000:
                self.fetch(ram, 0)
                self.fetch(ram, 0)
                ram.write(self.address_stack, int(self.ar))
                self.address_stack = 0
            elif arg == 0b1000:
                self.fetch(ram, 0)
                self.fetch(ram, 0)
                ram.write(self.address_stack, int(self.xr))
                self.address_stack = 0

        # ADD
        elif opcode == 0b0100:
            self.ar += self.xr

        # SUB
        elif opcode == 0b0100:
            self.ar += self.xr

        # NOR
        elif opcode == 0b0100:
            self.ar |= self.xr

        # PUSH
        elif opcode == 0b0101:
            if arg == 0b0000:
                self.stack.append(self.ar)
            elif arg == 0b1000:
                self.stack.append(self.xr)

        # POP
        elif opcode == 0b0110:
            if arg == 0b0000:
                self.ar = self.stack.pop()
            elif arg == 0b1000:
                self.xr = self.stack.pop()

        # JMP
        elif opcode == 0b0111:
            self.fetch(ram, 0)
            self.fetch(ram, 0)
            self.dr = self.address_stack
            self.address_stack = 0

        # JZ
        elif opcode == 0b1000 and self.ar.zero:
            self.fetch(ram, 0)
            self.fetch(ram, 0)
            self.dr = self.address_stack
            self.address_stack = 0

        # MOI
        elif opcode == 0b1001:
            if arg < 8:
                self.ar = int8(arg)
            else: self.xr = int8(arg - 8)

        # CMP
        elif opcode == 0b1010:
            pass

        # JO
        elif opcode == 0b1011 and self.ar.overflow:
            self.fetch(ram, 0)
            self.fetch(ram, 0)
            self.dr = self.address_stack
            self.address_stack = 0

        elif opcode == 0b1111:
            if arg == 0b1111:
                print('CPU halted')
                quit()
            elif arg == 0:
                pass

ram = RAM(2**10)
ram.write(0, 0b1001_1011)
ram.write(1, 0b0011_1000)
ram.write(2, 0)
ram.write(3, 100)
ram.write(4, 0b0010_0000)
ram.write(5, 0)
ram.write(6, 3)
ram.write(7, 0b0100_0000)
ram.write(8, 0b0011_0000)
ram.write(9, 0)
ram.write(10, 3)
ram.write(11, 0b0111_0000)
ram.write(12, 0)
ram.write(13, 1)

cpu = CPU()
gpu = GPU((100, 200))




while True:
    cpu.fetch(ram)
    cpu.execute(ram)
    #print('AR: ',cpu.ar)
    #print('XR: ',cpu.xr)
    #print('IR: ',cpu.ir)
    #print('DR: ',cpu.dr)
    #print()
    #print(ram.content[:200])
    os.system('cls')
    gpu.render_frame(ram)
    time.sleep(0.2)