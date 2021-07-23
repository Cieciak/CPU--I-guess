import os
from ram import *

class Disk:

    def set_up(self, disk_number: int, sectors: int):
        self.name = f'disk{disk_number}'
        self.sectors = sectors     

    def init(self, disk_number: int, sectors: int):
        self.name = f'disk{disk_number}'
        self.sectors = sectors
        try:
            os.mkdir(f'disk{disk_number}')
        except:
            pass
        for i in range(sectors):
            with open(f'disk{disk_number}/{i}.dsk', 'w') as file:
                file.write('0\n'*4)
                file.close()

    def write(self, sector: int, data: list):
        with open(self.name + f'/{sector}.dsk', 'w') as file:
            for i in data:
                file.write(f'{i}\n')
            file.close()
    
    def read(self, sector: int):
        with open(self.name + f'/{sector}.dsk', 'r') as file:
            content = file.read().split('\n')[0:4]
            file.close()
        return [int(x) for x in content]