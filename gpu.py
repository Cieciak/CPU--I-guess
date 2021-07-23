import ram

class GPU:

    def __init__(self, ram_space):
        self.vram_address = ram_space

    def render_frame(self, ram: ram.RAM):
        vram = ram.content[self.vram_address[0]:self.vram_address[1]]
        shade = [' ', '░', '▒', '▓', '█']
        for index, i in enumerate(vram):
            if index % 10 == 0:
                print()
            print(shade[i], end='')

        print()