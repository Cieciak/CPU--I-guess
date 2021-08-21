from ram import RAM
from cpu import CPU
from gpu import GPU
from keyboard import Keyboard
import threading, time, os, sys

# Emulator settings
FILE_NAME = sys.argv[1]
DEBUG = False

# Load code
ram = RAM(2**16)
ram.write(0xfeff, 0xff)
with open(FILE_NAME, 'r') as file:
    ram.loads(file.read())


keyboard = Keyboard(0xff64, ram)
gpu = GPU(0xff00, 100, ram)
cpu = CPU(ram)

def gpu_loop():
    while True:
        gpu.render_frame()
        time.sleep(0.1)
        if cpu.halted: return
        os.system('cls')

def cpu_loop():
    while True:
        cpu.fetch()
        cpu.execute()

def debug_loop():
    while True:
        print(ram.content[0xff64:0xff6f])

gpu_thread = threading.Thread(target=gpu_loop)
gpu_thread.start()

cpu_thread = threading.Thread(target=cpu_loop)
cpu_thread.start()

if DEBUG:
    debug_thread = threading.Thread(target=debug_loop)
    debug_thread.start()

print(ram)