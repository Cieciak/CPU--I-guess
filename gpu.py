import ram

class GPU:

    def __init__(self, address: int, size: int, memory: ram.RAM):
        self.address = address
        self.size = size
        self.ram = memory
        self.CHARACTER_SET = ' ░▒▓█                                                            abcdefghijklmnopqrstuvwxyz'

    def render_frame(self):
        vram = self.ram.content[self.address:self.address + 100]
        for index, i in enumerate(vram):
            if not index % 10: print()
            print(self.CHARACTER_SET[i], end='')
        print()


if __name__ == '__main__':
    from time import sleep
    import keyboard, os

    memory = ram.RAM(1024)

    key = keyboard.Keyboard(10, memory)
    gpu = GPU(10, 10, memory)

    while True:
        gpu.render_frame()
        sleep(0.1)
        os.system('cls')