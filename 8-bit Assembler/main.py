import sys
file = open(sys.argv[1], 'r')
text = [x.strip() for x in file.read().splitlines() if x != '']
label = [x.strip() for x in text if x.strip().endswith(':')]
file.close()

index = 0
labels = {}

for i in text:
    print(index, i)
    if i.endswith(':'):
        labels[label.pop(0)] = index
    elif i.startswith(tuple(['ldf', 'ldt', 'jmp', 'jz', 'jo'])):
        index += 3
    else: index += 1


print(labels)

def isbinary(i: str):
    if len(i) < 3: return 
    return True if i[1] == 'b' and i[2:].isdecimal() else False

def ishex(i: str):
    if len(i) < 3: return 
    return True if i[1] == 'x' and i[2:].isdecimal() else False

def parse_arg(arg: str, labels: dict):
    one, *two = arg.split(',', 1)

    one = one.strip()
    if two: two = two[0].strip()

    if isbinary(one):
        one = int(one, 2)
    elif ishex(one):
        one = int(one, 16)
    elif one.isdigit():
        one = int(one)
    elif one + ':' in labels:
        one = labels[one + ':']

    if two:
        if isbinary(two):
            two = int(two, 2)
        elif ishex(two):
            two = int(two, 16)
        elif two.isdecimal():
            two = int(two)      

    return one, two if two else one

class Line:

    def __init__(self, text: str):
        self.opcode, *arg = text.split(' ', 1)
        self.args = parse_arg(arg[0], labels) if arg else None

        #print(self.opcode, self.args)


lines = [Line(x) for x in text]

machine_code_output = []
for l in lines:

    if l.opcode == 'mov':
        if l.args[0] == 'a':
            machine_code_output.append(0b0001_0000)
        elif l.args[0] == 'x':
            machine_code_output.append(0b0001_1000)
    
    elif l.opcode == 'ldf':
        if l.args[0] == 'a':
            machine_code_output.append(0b0010_0000)
            machine_code_output.append(l.args[1] // 256)
            machine_code_output.append(l.args[1] % 256)
        elif l.args[0] == 'x':
            machine_code_output.append(0b0010_1000)
            machine_code_output.append(l.args[1] // 256)
            machine_code_output.append(l.args[1] % 256)

    elif l.opcode == 'ldt':
        if l.args[0] == 'a':
            machine_code_output.append(0b0011_0000)
            machine_code_output.append(l.args[1] // 256)
            machine_code_output.append(l.args[1] % 256)
        elif l.args[0] == 'x':
            machine_code_output.append(0b0011_1000)
            machine_code_output.append(l.args[1] // 256)
            machine_code_output.append(l.args[1] % 256)

    elif l.opcode == 'add':
       machine_code_output.append(0b0100_0000)

    elif l.opcode == 'sub':
       machine_code_output.append(0b0101_0000)

    elif l.opcode == 'nor':
       machine_code_output.append(0b0110_0000)

    elif l.opcode == 'push':
        if l.args[0] == 'a':
            machine_code_output.append(0b0111_0000)
        elif l.args[0] == 'x':
            machine_code_output.append(0b0111_1000)

    elif l.opcode == 'pop':
        if l.args[0] == 'a':
            machine_code_output.append(0b1000_0000)
        elif l.args[0] == 'x':
            machine_code_output.append(0b1000_1000)

    elif l.opcode == 'jmp':
        machine_code_output.append(0b1001_0000)
        machine_code_output.append(l.args[0] // 256)
        machine_code_output.append(l.args[0] % 256)

    elif l.opcode == 'jz':
        machine_code_output.append(0b1010_0000)
        machine_code_output.append(l.args[0] // 256)
        machine_code_output.append(l.args[0] % 256)
    
    elif l.opcode == 'moi':
        if l.args[0] == 'a':
            machine_code_output.append(0b1011_0000 + l.args[1])
        elif l.args[0] == 'x':
            machine_code_output.append(0b1011_1000 + l.args[1])

    elif l.opcode == 'test':
        machine_code_output.append(0b1100_0000)

    elif l.opcode == 'jo':
        machine_code_output.append(0b1101_0000)
        machine_code_output.append(l.args[0] // 256)
        machine_code_output.append(l.args[0] % 256)

    elif l.opcode == 'hlt':
        machine_code_output.append(0b1111_1111)

    elif l.opcode == 'nop':
        machine_code_output.append(0b1111_0000)

file = open('a.out', 'w')
for i in machine_code_output:
    file.write(str(i) + ' ')

file.close()