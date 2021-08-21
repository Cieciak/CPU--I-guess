import ram, time
import Utils.basics as basics

class CPU:

    def __init__(self, ram: ram.RAM):
        # GP registers
        self.ar = basics.int8(0)
        self.xr = basics.int8(0)

        self.ir = basics.int8(0)
        self.dr = 0

        self.stack = []
        self.ram = ram

        self.address_stack = 0
        self.halted = False

    def fetch(self, place = 'ir'):
        if place == "ir":
            self.ir = basics.int8(self.ram.read(self.dr))
        else:
            # Put int8 to addres stack
            self.address_stack = self.address_stack * 256 + self.ram.read(self.dr)
        self.dr += 1

    def execute(self):
        opcode, args = self.ir.split()

        # MOV
        if opcode == 0b0001:
            if args == 0b1000:
                self.xr = self.ar
            elif args == 0b0000:
                self.ar = self.xr
        # LDF
        elif opcode == 0b0010:
            if args == 0b0000:
                self.fetch(0)
                self.fetch(0)
                self.ar = basics.int8(self.ram.read(self.address_stack))
            elif args == 0b1000:
                self.fetch(0)
                self.fetch(0)
                self.xr = basics.int8(self.ram.read(self.address_stack))
            self.address_stack = 0
        # LDT
        elif opcode == 0b0011:
            if args == 0b0000:
                self.fetch(0)
                self.fetch( 0)
                self.ram.write(self.address_stack, int(self.ar))
            elif args == 0b1000:
                self.fetch(0)
                self.fetch(0)
                self.ram.write(self.address_stack, int(self.xr))
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
            if args == 0b0000:
                self.stack.append(self.ar)
            elif args == 0b1000:
                self.stack.append(self.xr)
        # POP
        elif opcode == 0b1000:
            if args == 0b0000:
                self.ar = self.stack.pop()
            elif args == 0b1000:
                self.xr = self.stack.pop()
        # JMP
        elif opcode == 0b1001:
            self.fetch(0)
            self.fetch(0)
            self.dr = self.address_stack
            self.address_stack = 0
        # JZ
        elif opcode == 0b1010 and self.ar.zero:
            self.fetch(0)
            self.fetch(0)
            self.dr = self.address_stack
            self.address_stack = 0
        # MOI
        elif opcode == 0b1011:
            if args < 8:
                self.ar = basics.int8(args)
            else: self.xr = basics.int8(args - 8)
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
            if args == 0b1111:
                self.halted = True
                print('CPU halted')
                quit()
            elif args == 0:
                pass  

if __name__ == '__main__':
    memory = ram.RAM(1024)

    memory.load([0, 0b1011_1111, 0b0011_1000, 0,0])
    cpu = CPU(memory)

    while True:
        time.sleep(1)
        cpu.fetch()
        cpu.execute()
        print(cpu.ar, cpu.xr)
        print(memory)