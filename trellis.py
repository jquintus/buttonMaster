import time
import board
from adafruit_neotrellis.neotrellis import NeoTrellis

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


class Trellis:

    def __init__(self, on_press):
        self.on_press = on_press


    def start(self):
        on_press = self.on_press
        # create the i2c object for the trellis
        i2c_bus = board.I2C()  # uses board.SCL and board.SDA
        trellis = NeoTrellis(i2c_bus)
        trellis.brightness = 0.12

        for i in range(16):
            trellis.activate_key(i, NeoTrellis.EDGE_RISING)
            trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
            trellis.callbacks[i] = on_press

            # cycle the LEDs on startup
            trellis.pixels[i] = PURPLE
            time.sleep(0.05)

        for i in range(16):
            trellis.pixels[i] = OFF
            time.sleep(0.05)

        # private fields
        self.trellis = trellis
        self.pixels = trellis.pixels

    def sync(self):
        self.trellis.sync()
