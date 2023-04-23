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
        print(f'Pressed {event.number}')
        button = buttons[event.number]

        trellis.pixels[event.number] = button.color
        button.onPress()

    # turn the LED off when a falling edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = OFF

ble = ArcadeKeyboard()
ble.start()
k = ble.get_keyboard()
cc = ble.get_consumer_control()

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
        KeyComboButton("Zoom: raise/lower hand",        GREEN, k, Keycode.F8),
        KeyComboButton("Zoom: Copy Invite Link",        GREEN, k, Keycode.F4),
        KeyComboButton("Zoom: Toggle Video",            GREEN, k, Keycode.F1),
        KeyComboButton("Zoom: Toggle Audio",            GREEN, k, Keycode.F6),

        # Column 1
        EmptyButton(   "Button 5 unset",                CYAN),
        EmptyButton(   "Button 4 unset",                CYAN),
        KeyComboButton("Zoom: Pause Share",             GREEN, k, Keycode.F7),
        KeyComboButton("Zoom: Share",                   GREEN, k, Keycode.F2),

        # Column 2
        KeyComboButton("OBS: Transition",               BLUE,  k, Keycode.F10),
        KeyComboButton("OBS: Screen Shot Output",       BLUE,  k, Keycode.F9),
        KeyComboButton("OBS: Toggle Virtual Camera",    BLUE,  k, Keycode.F12),
        KeyComboButton("OBS: Switch to Default Scene",  BLUE,  k, Keycode.F11, Keycode.F10),

        # Column 3
        VolumeButton(  "Volume Mute",                   YELLOW, cc, ConsumerControlCode.MUTE),
        VolumeButton(  "Volume Mute",                   YELLOW, cc, ConsumerControlCode.MUTE),
        VolumeButton(  "Volume Down",                   YELLOW, cc, ConsumerControlCode.VOLUME_DECREMENT),
        VolumeButton(  "Volume Up",                     YELLOW, cc, ConsumerControlCode.VOLUME_INCREMENT),
        ]

def wait_for_bluetooth_connection():
    ble_counter = 0
    pixels = trellis.pixels

    print ("Waiting for connection...")
    pixels[15] = BLUE
    next_color = YELLOW
    while not ble.is_connected():
        ble_counter += 1
        if ble_counter > 50000:
            ble_counter = 0
            print ("Waiting for connection...")
            swap = pixels[15]
            pixels[15] = next_color
            next_color = swap 
        pass

    pixels[15] = OFF
    print("Start typing:")

while True:
    wait_for_bluetooth_connection()

    while ble.is_connected():

        # call the sync function call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 millisecons or so
        time.sleep(0.02)

    ble.start_advertising()
