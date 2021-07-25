import os
from PIL import Image

files = [Image.open(f'Frames/{x}.png') for x in range(0, 17)]

files[0].save('out.gif', save_all = True, append_images = files[1:])