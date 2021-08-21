class RAM:

    def __init__(self, size: int):
        '''RAM Instance'''
        self.size = size
        self.content = [0] * size

    def __repr__(self) -> str:
        out = ''
        for i in self.content:
            out += f' {i}'
        return out

    def read(self, address: int) -> int:
        return self.content[address]

    def write(self, address: int, value: int) -> int:
        self.content[address] = value

    def load(self, data: list[int]):
        for  index, i in enumerate(data):
            self.content[index] = i

    def loads(self, data: str):
        i = 0
        for word in data.split(' '):
            if word.isdigit():
                self.content[i] = int(word)
                i += 1
            elif word.startswith('0x'):
                self.content[i] = int(word, 0)
                i += 1
            elif word.startswith('0b'):
                self.content[i] = int(word, 0)
                i +- 1

if __name__ == "__main__":
    ram = RAM(1024)

    ram.load([1,2,3,5,6,9,9,9,6,5,4,8])

    ram.write(1, 23)

    print(ram)