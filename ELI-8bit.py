from ram import RAM
from basics import int8
from gpu import GPU
from keyboard import Keyboard
import time
import os
import threading
import time

class CPU:

    def __init__(self):
        self.ar = int8(0)
        self.xr = int8(0)
        self.ir = int8(0)
        self.dr = int(0)

        self.stack = []
        self.address_stack = 0
        self.halted = False

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
            if arg == 0b1000:
                self.xr = self.ar
            elif arg == 0b0000:
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
        elif opcode == 0b0101:
            self.ar -= self.xr

        # NOR
        elif opcode == 0b0110:
            self.ar |= self.xr

        # PUSH
        elif opcode == 0b0111:
            if arg == 0b0000:
                self.stack.append(self.ar)
            elif arg == 0b1000:
                self.stack.append(self.xr)
        # POP
        elif opcode == 0b1000:
            if arg == 0b0000:
                self.ar = self.stack.pop()
            elif arg == 0b1000:
                self.xr = self.stack.pop()

        # JMP
        elif opcode == 0b1001:
            self.fetch(ram, 0)
            self.fetch(ram, 0)
            self.dr = self.address_stack
            self.address_stack = 0

        # JZ
        elif opcode == 0b1010 and self.ar.zero:
            self.fetch(ram, 0)
            self.fetch(ram, 0)
            self.dr = self.address_stack
            self.address_stack = 0

        # MOI
        elif opcode == 0b1011:
            if arg < 8:
                self.ar = int8(arg)
            else: self.xr = int8(arg - 8)

        # TEST
        elif opcode == 0b1100:
            if self.ar == 0:
                self.ar.zero = True
            else:
                self.ar.zero = False

        # JO
        elif opcode == 0b1101 and self.ar.overflow:
            self.fetch(ram, 0)
            self.fetch(ram, 0)
            self.dr = self.address_stack
            self.address_stack = 0

        elif opcode == 0b1111:
            # HLT
            if arg == 0b1111:
                self.halted = True
                print('CPU halted')
                quit()
            elif arg == 0:
                pass

file = open('a.out', 'r')
data = [int(x) for x in file.read().split(' ') if x != '']

ram = RAM(2**16)
ram.load(data)

cpu = CPU()
gpu = GPU((256, 356))
key = Keyboard(255, ram)

def gpu_loop():
    while True:
        gpu.render_frame(ram)
        time.sleep(0.01)
        if cpu.halted:
            print(cpu.ar)
            gpu.render_frame(ram)
            break
        os.system('cls')
        
def cpu_loop():
    start = time.time()
    counter = 0
    while True:
        counter += 1
        cpu.fetch(ram)
        cpu.execute(ram)
        if (time.time() - start) > 2:
            start = time.time()
            os.system(f'title {int(counter / 2)} cycles per second')
            counter = 0


gpu_thread = threading.Thread(target=gpu_loop)
gpu_thread.daemon = True
gpu_thread.start()

cpu_thread = threading.Thread(target=cpu_loop)
cpu_thread.daemon = True
cpu_thread.start()

input()
print(ram.content[:30])
input()