import numpy
import numpy as np
import ram
from PIL import Image

class GPU:

    def __init__(self, ram_space):
        self.vram_address = ram_space
        self.frames = 0

    def render_frame(self, ram: ram.RAM):
        vram = ram.content[self.vram_address[0]:self.vram_address[1]]
        #        0         10        20        30        40        50        60        70        80        90
        shade = ' ░▒▓█                                                            abcdefghijklmnopqrstuvwxyz'
                # ######### ######### ######### ######### ######### ######### ######### ######### #########
        for index, i in enumerate(vram):
            if index % 10 == 0:
                print()
            print(shade[i], end='')

        print()

    def save_frame(self, ram: ram.RAM):
        vram = ram.content[self.vram_address[0]:self.vram_address[1]]
        a = np.array(vram).reshape((10, 10)) * 60
        image = Image.fromarray(np.uint8(a), 'L')
        image.save(f'Frames/{self.frames}.png')
        self.frames += 1