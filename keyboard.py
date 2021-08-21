from pynput import keyboard
import ram

class Keyboard:

    def __init__(self, address: int, ram: ram.RAM):
        # Key listener
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        # RAM values
        self.address = address
        self.offset = 0
        self.ram = ram
        # Flags
        self.pinned_down = False

    def on_press(self, key):
        try:
            # The normal key (Alphanumeric ?)
            mapped_value = key.vk
        except AttributeError:
            # Other keys
            mapped_value = key.value.vk
        except:
            # This should never happen
            mapped_value = None
            print('KEYBOARD API ERROR\nThis key is not mapped')

        if not self.pinned_down:
            self.ram.write(self.address + self.offset % 10, mapped_value)
            self.offset += 1
        self.pinned_down = True

    def on_release(self, key):
        self.pinned_down = False

if __name__ == '__main__':
    from time import sleep
    import os

    memory = ram.RAM(1024)
    keys = Keyboard(10, memory)

    while True:
        os.system('cls')
        print(memory)
        sleep(0.1)