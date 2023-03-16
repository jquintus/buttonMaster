import time

# needed for keycodes 
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Needed for Edge Detection
from adafruit_neotrellis.neotrellis import NeoTrellis

# my imports
from arcade_hid import ArcadeKeyboard
from buttons import LambdaButton, EmptyButton, KeyComboButton, VolumeButton
from trellis import Trellis

print("Hello, CircuitPython!")
def on_press(event):
    # Button Orientation If the Switch is on the top
    #  3  7 11 15
    #  2  6 10 14
    #  1  5  9 13
    #  0  4  8 12
    
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = GREEN
        print(f'Pressed {event.number}')

        buttons[event.number].onPress()
    # turn the LED off when a falling edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = OFF

arcade = ArcadeKeyboard()
arcade.start()
k = arcade.get_keyboard()
cc = arcade.get_consumer_control()

trellis = Trellis(on_press)
trellis.start()

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

buttons = [
        # Column 0
        KeyComboButton("Zoom: raise/lower hand",        k, Keycode.F8),
        KeyComboButton("Zoom: Copy Invite Link",        k, Keycode.F4),
        KeyComboButton("Zoom: Toggle Video",            k, Keycode.F1),
        KeyComboButton("Zoom: Toggle Audio",            k, Keycode.F6),

        # Column 1
        EmptyButton(   "Button 5 unset"),
        EmptyButton(   "Button 4 unset"),
        KeyComboButton("Zoom: Pause Share",             k, Keycode.F7),
        KeyComboButton("Zoom: Share",                   k, Keycode.F2),

        # Column 2
        KeyComboButton("OBS: Transition",               k, Keycode.F10),
        KeyComboButton("OBS: Screen Shot Output",       k, Keycode.F9),
        KeyComboButton("OBS: Toggle Virtual Camera",    k, Keycode.F12),
        KeyComboButton("OBS: Switch to Default Scene",  k, Keycode.F11, Keycode.F10),

        # Column 3
        VolumeButton(  "Volume Mute", cc, ConsumerControlCode.MUTE),
        VolumeButton(  "Volume Mute", cc, ConsumerControlCode.MUTE),
        VolumeButton(  "Volume Down", cc, ConsumerControlCode.VOLUME_DECREMENT),
        VolumeButton(  "Volume Up",   cc, ConsumerControlCode.VOLUME_INCREMENT),
        ]

while True:
    arcade.wait_for_bluetooth_connection()

    while arcade.is_connected():

        # call the sync function call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 millisecons or so
        time.sleep(0.02)

    arcade.start_advertising()
