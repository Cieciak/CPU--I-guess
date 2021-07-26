import os
from PIL import Image
import PIL

length = len(os.listdir('Frames/'))

files = [Image.open(f'Frames/{x}.png').resize((100,100), resample=Image.NEAREST) for x in range(0, length)]

files[0].save('out.gif', save_all = True, append_images = files[1:], duration = 0)