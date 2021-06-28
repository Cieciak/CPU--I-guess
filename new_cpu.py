from better_ram import RAM
import os

## AX  - 0
## BX  - 1
## CX  - 2
## DX  - 3
## IR  - 4
## DR  - 5
## FL  - 6
## LR  - 7
## R9  - 8
## R10 - 9
## R11 -10
## R12 -11
## R13 -12
## R14 -13
## R15 -14
## OV  -15

class CPU:

    def __init__(self):

        self.reg = [0] * 15
        self.stack = []
    
    def __repr__(self):
        out = ''
        for i in self.reg:
            out += str(i) + '\n'
        out += f'{self.stack}'
        return out

    def _get_instruction(self, ram: RAM):
        self.reg[4] = ram.read_quad_word(self.reg[5])
        self.reg[5] += 8

    def _execute(self, ram: RAM):
        A_reg = self.reg[4] % 2**35 // 2**32
        B_reg = self.reg[4] % 2**39 // 2**36
        opcode = self.reg[4] // (2**40)
        args = self.reg[4] % (2**32)

        if opcode == (2**24) - 1:
            print('CPU halted!')
            quit()

        # Read from RAM
        elif opcode == 0b1:
            self.reg[A_reg] = ram.read_quad_word(args)
        # Write to RAM
        elif opcode == 0b10:
            ram.write_quad_word(args, self.reg[A_reg]) 
        # Add
        elif opcode == 0b11:
            self.reg[A_reg] += self.reg[B_reg]
        # Sub
        elif opcode == 0b100:
            self.reg[A_reg] -= self.reg[B_reg]
        # Mul
        elif opcode == 0b101:
            self.reg[A_reg] *= self.reg[B_reg]
        # Div
        elif opcode == 0b110:
            self.reg[A_reg] = self.reg[A_reg] // self.reg[B_reg]
            self.reg[A_reg + 1] = self.reg[A_reg] % self.reg[B_reg]
        # Jump
        elif opcode == 0b111:
            self.reg[5] = args - 8
        # Test
        elif opcode == 0b1000:
            if self.reg[A_reg] == 0:
                self.reg[6] = 1 << 64        
        # Compare
        elif opcode == 0b1001:
            self.reg[6] = 0
            if self.reg[A_reg] == 0:
                self.reg[6] += 1 << 64
            if self.reg[A_reg] < self.reg[B_reg]:
                self.reg[6] += 1 << 63
            if self.reg[A_reg] == self.reg[B_reg]:
                self.reg[6] += 1 << 62
            if self.reg[A_reg] > self.reg[B_reg]:
                self.reg[6] += 1 << 61
        # Jump if zero
        elif opcode == 0b1010:
            if (self.reg[6] >> 64) % 2:
                self.reg[5] = args - 8
        # Jump if smaller
        elif opcode == 0b1011:
            if (self.reg[6] >> 63) % 2:
                self.reg[5] = args - 8
        # Jump if equal
        elif opcode == 0b1100:
            if (self.reg[6] >> 62) % 2:
                self.reg[5] = args - 8
        # Jump if greater
        elif opcode == 0b1101:
            if (self.reg[6] >> 61) % 2:
                self.reg[5] = args - 8
        # NOT
        elif opcode == 0b1110:
            self.reg[A_reg] = ~self.reg[A_reg]

        elif opcode == 0b1111:
            self.reg[A_reg] = self.reg[A_reg] & self.reg[B_reg]
            
        elif opcode == 0b10000:
            self.reg[A_reg] = self.reg[A_reg] | self.reg[B_reg]

        elif opcode == 0b10001:
            self.reg[A_reg] = ~(self.reg[A_reg] & self.reg[B_reg])

        elif opcode == 0b10010:
            self.reg[A_reg] = ~(self.reg[A_reg] | self.reg[B_reg])

        elif opcode == 0b10011:
            self.reg[A_reg] = self.reg[A_reg] ^ self.reg[B_reg]

        elif opcode == 0b10100:
            self.reg[A_reg] = ~(self.reg[A_reg] ^ self.reg[B_reg])

        elif opcode == 0b10101:
            self.stack.append(self.reg[A_reg])

        elif opcode == 0b10110:
            self.reg[A_reg] = self.stack.pop(-1)
        
        elif opcode == 0b10111:
            self.stack = []

        elif opcode == 0b11000:
            self.reg[A_reg] = len(self.stack)

        elif opcode == 0b11001:
            self.reg[A_reg] = ram.read_byte(args)
        
        elif opcode == 0b11010:
            self.reg[A_reg] = ram.read_word(args)
        
        elif opcode == 0b11011:
            self.reg[A_reg] = ram.read_double_word(args)

        elif opcode == 0b11100:
            ram.write_byte(args, self.reg[A_reg] % 256)

        elif opcode == 0b11101:
            ram.write_word(args, self.reg[A_reg] % (256 * 256))

        elif opcode == 0b11110:
            ram.write_double_word(args, self.reg[A_reg] % (256 * 256 * 256 * 256))

        elif opcode == 0b11111:
            self.reg[B_reg] = self.reg[A_reg]
        
        # Interrupt
        elif opcode == 0b100000:
            pass

        elif opcode == 0b100001:
            self.reg[A_reg] = args

        elif opcode == 0b100011:
            self.reg[A_reg] += args

        elif opcode == 0b100100:
            self.reg[A_reg] += args

        elif opcode == 0b100101:
            self.reg[A_reg] *= args

        elif opcode == 0b100110:
            self.reg[A_reg] = self.reg[A_reg] // args
            self.reg[A_reg + 1] = self.reg[A_reg] % args

        elif opcode == 0b100111:

            self.reg[6] = 0
            if self.reg[A_reg] == 0:
                self.reg[6] += 1 << 64
            if self.reg[A_reg] < args:
                self.reg[6] += 1 << 63
            if self.reg[A_reg] == args:
                self.reg[6] += 1 << 62
            if self.reg[A_reg] > args:
                self.reg[6] += 1 << 61
            
        elif opcode == 0b101111:
            self.reg[A_reg] = self.reg[A_reg] & args

        elif opcode == 0b110000:
            self.reg[A_reg] = self.reg[A_reg] | args

        elif opcode == 0b110001:
            self.reg[A_reg] = ~(self.reg[A_reg] & args)

        elif opcode == 0b110010:
            self.reg[A_reg] = ~(self.reg[A_reg] | args)

        elif opcode == 0b110011:
            self.reg[A_reg] = self.reg[A_reg] ^ args

        elif opcode == 0b110100:
            self.reg[A_reg] = ~(self.reg[A_reg] ^ args)

        elif opcode == 0b111111:
            self.reg[A_reg] = args

ram = RAM(128)



# Code

ram._load(open('./Assembler/r.out'), 8)

# Vars

# Halt
ram.write_quad_word(120, ((2**24)-1) << 40)

cpu = CPU()

while True:
    input()
    os.system('cls')
    cpu._get_instruction(ram)
    print(ram)
    print(cpu)
    cpu._execute(ram)
