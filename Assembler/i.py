file = 'Assembler/t.asm'

# CPU registers
cpu_regs = {
    'rax': 0b0000,
    'rbx': 0b0001,
    'rcx': 0b0010,
    'rdx': 0b0011,
    'ir' : 0b0100,
    'dr' : 0b0101,
    'fl' : 0b0110,
    'lr' : 0b0111,
    'r9' : 0b1000,
    'r10': 0b1001,
    'r11': 0b1010,
    'r12': 0b1011,
    'r13': 0b1100,
    'r14': 0b1101,
    'r15': 0b1110,
    'ov' : 0b1111}

# Get list of opcodes
with open('Assembler/ops.dat', 'r') as f:
    opcodes = [x.strip() for x in f.readlines()]
    f.close()
print('Opcodes:', opcodes)

# Get content of assembly file
with open(file, 'r') as f:
    data = [x.strip() for x in f.readlines()]
    f.close()
print('Lines:', data)

# System constants
INSTRUCTION_LENGTH = 8
DEFINE_OPS = ['db', 'dw', 'dd', 'dq']

# Compilation variables
ORIGIN = 0x00
MEMORY_SIZE = 1024
NUMBER_OF_POSSIBLE_INSTRUCTIONS = int(MEMORY_SIZE / INSTRUCTION_LENGTH)


def create_instruction(instruction_code: int, reg_b: int, reg_a: int, arg: int):
    return (((instruction_code << 8) + (reg_b << 4) + reg_a) << 32) + arg


class Argument:

    def __init__(self, data: str):
        # If register, transtate register name to register number
        if data in cpu_regs:
            self.type = 'register'
            self.value = cpu_regs[data]
        # If it is a number then do stuff
        elif data.isnumeric():
            self.type = 'number'
            self.value = int(data)
        # If it is an address then ...
        elif data.startswith('[') and data.endswith(']'):
            self.type = 'address'
            number = data[1:-1]
            # If it is not a number let it be
            if number.isnumeric():
                self.value = int(number)
            else:
                self.value = number
        # Now it is probably a variable name or something
        else:
            self.type = 'name'
            self.value = data

    def __repr__(self):
        out = f'{self.type}: {self.value}'
        return out

class Line:

    def __init__(self, line: str):
        opcode, *args = line.split(' ', 1)
        self.name = ''
        
        # If line doesn't have arguments and ends with ':' it's probably a label
        if not args and line.endswith(':'):
            # Set type to 'label' and name to opcode
            self.type = 'label'
            self.name = opcode[:-1]
            self.args = None

        # Ignore empty line
        elif not line:
            self.type = 'empty'
            self.name = 'none'
            self.args = None

        else:
            # Set type to 'instruction' and parse the line
            self.type = 'instruction'
            self.name = opcode
            args = args[0]
            args = [x.strip() for x in args.split(',')]
            self.args = [Argument(x) for x in args]

    def __repr__(self):
        return f'{self.name}: {self.args}'

# Parse lines 
assembly_lines = [Line(x) for x in data]
# Purify lines
pure_assembly = [x for x in assembly_lines if x.type != 'empty']

# Compilation time variables
number_of_instructions = 0
current_address = ORIGIN
code_space = number_of_instructions

# Code variables
assembly_variables = {}
labels_localization = {}
out = [0] * NUMBER_OF_POSSIBLE_INSTRUCTIONS

# Find all of the variables and lades for later use, also define where does the
# machine code begin in memory
for line in pure_assembly:

    # Place variable
    if line.name in DEFINE_OPS:
        assembly_variables[line.args[0].value] = current_address
        code_space += 1

    # Save label localization
    elif line.type == 'label':
        labels_localization[line.name] = current_address

    number_of_instructions += 1
    current_address += 8


# Compile
for line in pure_assembly:
    if line.type == 'label':
        code_space += 1
        continue

    elif line.name == 'mov':
        if line.args[0].type == 'register':
            if line.args[1].type == 'number':
                i = create_instruction(0b111111, 
                                       0, 
                                       line.args[0].value, 
                                       line.args[1].value)
                out[code_space] = i
                code_space += 1
            elif line.args[1].type == 'register':
                i = create_instruction(0b11111, 
                                       line.args[0].value, 
                                       line.args[1].value, 
                                       0)
                out[code_space] = i
                code_space += 1
            elif line.args[1].type == 'address':
                i = create_instruction(0b001, 
                                       0, 
                                       line.args[0].value, 
                                       line.args[1].value)
                out[code_space] = i
                code_space += 1

print('Pure assembly: ', pure_assembly)
print('Output: ', out)
print('Variables: ', assembly_variables)
print('Labels: ', labels_localization)

with open('Assembler/r.out', 'w') as file:
    for i in out:
        file.write(str(i) + ' ')
