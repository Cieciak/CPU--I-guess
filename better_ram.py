class RAM:

    def __init__(self, size: int):
        self.content = [0] * size

    def __repr__(self):
        return f'{self.content}'

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