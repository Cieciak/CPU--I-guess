import sys

def create_instruction(instruction_code: int, reg_b: int, reg_a: int, arg: int):
    return (((instruction_code << 8) + (reg_b << 4) + reg_a) << 32) + arg

# Registers
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
    'ov' : 0b1111
}

# Labels
labels = {}

# Variables
variables = {}
variables_localization = {}

# Load opcodes
with open('ops.dat') as f:
    opcodes = tuple([x.strip() for x in f.readlines()])
    f.close()
#print(opcodes)

# Get file to compile
file = open(sys.argv[1]).read().splitlines()

class Opcode:

    def __init__(self, name: str ):
        if name in opcodes:
            self.name = name
        elif name == '':
            self.name = None
        else:
            raise NameError()

    def __repr__(self):
        return f'{self.name}'

class Arg:

    def __init__(self, value: str):
        if value.isdigit():
            self.type = 'number'
            self.value = int(value)
        
        elif value in cpu_regs:
            self.type = 'reg'
            self.value = cpu_regs[value]

        elif value[0] == '[' and value[-1] == ']':
            try:
                self.value = int(value[1:-1])
                self.type = 'address'
                self.numeric = True
            except:
                self.value = value[1:-1]
                self.type = 'address'
                self.numeric = False

        else:
            self.type = 'name'
            self.value = value
        
    def __repr__(self):
        out = f'|{self.type}: {self.value}|'
        return out    

class Line:
    def __init__(self, element: str):
        line = element.strip()

        # Empty line 
        if line.isspace() or line == '':
            self.type = 'empty_line'
            self.opcode = Opcode('')
            self.args = None
            self.name = ''

        # Figure out if it is a label or instruction 
        elif line.startswith(opcodes):
            self.type = 'instruction'
            opcode, *args = line.split(' ', 1)

            self.args = None
            if args:
                self.args = [Arg(i.strip()) for i in args[0].split(',')]
            self.opcode = Opcode(opcode)
            self.name = ''

        elif line.endswith(':'):
            self.type = 'label'
            self.name = line[:-1]
            self.opcode = None
            self.args = None

    def __repr__(self) -> str:
        out = self.type
        if self.opcode: out += f'\n   {self.opcode}'
        if self.args: out += f': {self.args}'
        if self.name: out += f'{self.name}'
        return out

lines = [Line(i.strip()) for i in file]


# Scan
free_space = len(lines) * 1
for index, line in enumerate(lines):
    print(f'{index}: {line}')
    if line.type == 'label':
        labels[line.name] = index * 8
    if line.type == 'instruction' and line.opcode.name in ['db', 'dw', 'dd', 'dq']:
        variables[line.args[0].value] = line.args[1].value
        variables_localization[line.args[0].value] = free_space
        free_space += 1

out = [0] * 16
u = 0
for line in lines:
    if line.opcode.name in ['dq']:
        print(line.args)
        out[variables_localization[line.args[0].value]] = line.args[1].value   


    if line.opcode.name == 'mov':
        if line.args[0].type == 'reg' and line.args[1].type == 'name':
            i = create_instruction(0b1, 0, line.args[0].value, 8*variables_localization[line.args[1].value])
            out[u] = i

        if line.args[0].type == 'reg' and line.args[1].type == 'reg':
            i = create_instruction(0b11111, line.args[0].value, line.args[1].value, 0)
            out[u] = i

        if line.args[0].type == 'reg' and line.args[1].type == 'number':
            i = create_instruction(0b111111, line.args[0].value, line.args[0].value, line.args[1].value)
            out[u] = i

        if line.args[0].type == 'name' and line.args[1].type == 'reg':
            i = create_instruction(0b10, 0, line.args[1].value, 8*variables_localization[line.args[0].value])
            out[u] = i

        if line.args[0].type == 'reg' and line.args[1].type == 'address':
            if line.args[1].numeric:
                i = create_instruction(0b10, 0, line.args[0].value, line.args[1].value)
            out[u] = i

        if line.args[0].type == 'address' and line.args[1].type == 'reg':
            i = create_instruction(0b10, 0, line.args[1].value, line.args[0].value)
            out[u] = i

    if line.opcode.name == 'add':
        if line.args[0].type == 'reg' and line.args[1].type == 'reg':
            i = create_instruction(0b11, line.args[1].value, line.args[0].value, 0)
            out[u] = i

        if line.args[0].type == 'reg' and line.args[1].type == 'number':
            i = create_instruction(0b100011, 0, line.args[0].value, line.args[1].value)
            out[u] = i

    if line.opcode.name == 'sub':
        if line.args[0].type == 'reg' and line.args[1].type == 'reg':
            i = create_instruction(0b100, line.args[1].value, line.args[0].value, 0)
            out[u] = i

        if line.args[0].type == 'reg' and line.args[1].type == 'number':
            i = create_instruction(0b100100, 0, line.args[0].value, line.args[1].value)
            out[u] = i

    if line.opcode.name == 'mul':
        if line.args[0].type == 'reg' and line.args[1].type == 'reg':
            i = create_instruction(0b101, line.args[1].value, line.args[0].value, 0)
            out[u] = i

        if line.args[0].type == 'reg' and line.args[1].type == 'number':
            i = create_instruction(0b100101, 0, line.args[0].value, line.args[1].value)
            out[u] = i

    if line.opcode.name == 'div':
        if line.args[0].type == 'reg' and line.args[1].type == 'reg':
            i = create_instruction(0b110, line.args[1].value, line.args[0].value, 0)
            out[u] = i

        if line.args[0].type == 'reg' and line.args[1].type == 'number':
            i = create_instruction(0b100110, 0, line.args[0].value, line.args[1].value)
            out[u] = i

    if line.opcode.name == 'jmp':
        i = create_instruction(0b111, 0, 0, labels[line.args[0].value])
        out[u] = i

    u += 1
    
f = open('r.out', 'w')
for j in out:
    f.write(str(j) + ' ')

f.close()


print(variables)
print(variables_localization)
print(labels)