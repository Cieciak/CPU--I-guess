
def make_entry(labels, code, arg):
    return (labels, code, arg)

def to_int(x: str):
    if x.startswith('0x'):
        return int(x, 16)
    if x.startswith('0b'):
        return int(x, 2)
    return int(x)

def parse_line(l: str):
    opcode, *raw_arg = l.split(' ', 1)
    args = []
    if raw_arg:
        args = [to_int(a.strip()) for a in raw_arg[0].split(',')]
    return opcode, args

with open('test.asm') as file:
    data = file.readlines()

data = [line.strip() for line in data]

ent = []
labels = []
for line in data:
    if line.endswith(':'):
        labels.append(line[:-1])
    else:
        c, a = parse_line(line)

        ent.append(make_entry(labels, c, a))
        labels = []