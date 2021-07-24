class RAM:

    def __init__(self, size: int):
        self.size = size
        self.content = [0] * size

    def __repr__(self):
        out = ''
        for i in self.content:
            out += str(i) + ' '
        return out

    def read(self, address: int):
        return self.content[address]

    def write(self, address: int, value: int):
        self.content[address] = value % 256

    def load(self, data):
        for index, i in enumerate(data):
            self.write(index, i)