
class uint8:

    def __init__(self, value: int) -> None:
        self.overflow = False

        self.value = value
        
    def __repr__(self):
        return f'{int(self.overflow)}:{self.value}'

    def __invert__(self):
        return uint8(~self.value)

    def __add__(self, other):
        return uint8(self.value + other.value)

    def set(self, value):
        self.value = value.value
        self.overflow = value.overflow

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.overflow = val >= 256
        self._value = val % 256

    def split(self):
        return self.value // 16, self.value % 16

if __name__ == '__main__':
    a = uint8(0)
    b = uint8(0xaa)

    print(a)
    print(~a)
    print(b)