from typing import IO


class RAM:

    def __init__(self, size: int):
        self.content = [0] * size

    def __repr__(self):
        out = ''
        for index, val in enumerate(self.content):
            if index % 8 == 0:
                out += '\n'
            out += str(hex(val))[2:] if len(str(hex(val))[2:]) == 2 else '0' + str(hex(val))[2:]
            out += ' '
        return out

    def _read(self, address: int, length: int):
        out = 0
        for i, v in enumerate(self.content[address:(address + length)][::-1]):
            out += v * 256 ** i
        return out

    def _write(self, address: int, length: int, data: int):
        for i in range(length):
            to_write = (data % 256)
            self.content[address + length - i - 1] = to_write
            data = data >> 8

    def _load(self, file: IO, _type: int):
        for index, value in enumerate(file.read().strip().split(' ')):
            self._write(_type * index, _type, int(value))
            

    def read_byte(self, address: int):
        return self._read(address, 1)

    def write_byte(self, address: int, value: int):
        self._write(address, 1, value)

    def read_word(self, address: int):
        return self._read(address, 2)

    def write_word(self, address, value: int):
        self._write(address, 2, value)

    def read_double_word(self, address: int):
        return self._read(address, 4)
    
    def write_double_word(self, address: int, value: int):
        self._write(address, 4, value)

    def read_quad_word(self, address: int):
        return self._read(address, 8)

    def write_quad_word(self, address: int, value: int):
        self._write(address, 8, value)

if __name__ == "__main__":
    ram = RAM(64)

    ram._load(open('r.out'), 8)
    print(ram)