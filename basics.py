
class int8:

    def __init__(self, value) -> None:
        self.int = value
        self.overflow = False
        self._check()

    def _check(self):
        self.zero = True if self.int == 0 else True
        self.overflow = True if self.int > 255 or self.int < 0 else False
        self.int += 256
        self.int %= 256 

    def __eq__(self, other) -> bool:
        if isinstance(other, int): return self.int == other
        elif isinstance(other, int8): return self.int == other.int

    def __lt__(self, other) -> bool:
        if isinstance(other, int): return self.int < other
        elif isinstance(other, int8): return self.int < other.int

    def __gt__(self, other) -> bool:
        if isinstance(other, int): return self.int > other
        elif isinstance(other, int8): return self.int > other.int

    def __le__(self, other) -> bool:
        if isinstance(other, int): return self.int <= other
        elif isinstance(other, int8): return self.int <= other.int

    def __ge__(self, other) -> bool:
        if isinstance(other, int): return self.int >= other
        elif isinstance(other, int8): return self.int >= other.int

    def __add__(self, other) -> bool:
        return int8(self.int + other.int)

    def __iadd__(self, other):
        return int8(self.int + other.int)

    def __sub__(self, other):
        return int8(self.int - other.int)

    def __isub__(self, other):
        return int8(self.int - other.int)

    def __repr__(self) -> str:
        return f'{self.int}'

    def __or__(self, other):
        return int8(~(self.int | other.int))

    def __ior__(self, other):
        return int8(~(self.int | other.int))

    def __matmul__(self, other):
        return self.int * 256 + other

    def split(self):
        return self.int // 16, self.int % 16

    def __int__(self):
        return self.int

if __name__ == "__main__":
    a = int8(0)
    b = int8(0)
    a |= b

    print('a == b:',a == b)
    print('a != b:',a != b)
    print('a < b:',a < b)
    print('a > b:',a > b)
    print('a >= b:',a >= b)
    print(a)