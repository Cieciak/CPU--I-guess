from pynput import keyboard
import ram, time

class Keyboard:

    def __init__(self, ram_address: int, ram: ram.RAM):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.ram = ram
        self.address = ram_address
        self.listener.start()

    def on_press(self, key):
        value = key.vk
        try:
            value = int(key.char) # Numeric input
        except ValueError:
            value = int(key.name) # Numeric input
        except TypeError:
            value = key.vk - 96 # Numpad
        except:
            return

        self.ram.write(self.address, value)



if __name__ == '__main__':
    ram0 = ram.RAM(16)
    test = Keyboard(1, ram0)

    while True:
        print(ram0.content)
        time.sleep(0.5)