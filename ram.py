from utils import uint8

class RAM:

    def __init__(self, size: int) -> None:
        self.size = size
        self.data = [uint8(0) for n in range(size)]

    def __repr__(self) -> str:
        return f'{self.data}'

    def read(self, index: int) -> uint8:
        return self.data[index]

    def write(self, index: int, value: uint8):
        self.data[index] = value

    def load(self, data: list[uint8]):
        for index, value in enumerate(data):
            self.write(index, value)

if __name__ == '__main__':
    ram = RAM(1024)


    data = [123,65,63,66,34,85,964,57,45]

    ram.load([uint8(x) for x in data])

    print(ram)