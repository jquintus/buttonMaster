# SPDX-FileCopyrightText: 2022 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_neotrellis.neotrellis import NeoTrellis

# Needed to be a bluetooth keyboard
import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import usb_hid

from buttons import LambdaButton, EmptyButton, KeyComboButton, VolumeButton

print("Hello, CircuitPython!")

# create the i2c object for the trellis
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
trellis = NeoTrellis(i2c_bus)
trellis.brightness = 0.12

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)



# this will be called when neo-tesllis events are received
def blink(event):
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


# Set up Keyboard and Bluethooth
hid = HIDService()

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "Josh Board"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising bluetooth")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected bluetooth")
    print(ble.connections)

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)

mouse = Mouse(hid.devices)

cc = ConsumerControl(hid.devices)

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

def wait_for_bluetooth_connection(ble, pixels):
    ble_counter = 50000 + 1

    print ("Waiting for connection...")
    pixels[15] = BLUE
    next_color = YELLOW
    while not ble.connected:
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

for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    trellis.pixels[i] = PURPLE
    time.sleep(0.05)

for i in range(16):
    trellis.pixels[i] = OFF
    time.sleep(0.05)

while True:

    wait_for_bluetooth_connection(ble, trellis.pixels)

    while ble.connected:

        # call the sync function call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 millisecons or so
        time.sleep(0.02)

    ble.start_advertising(advertisement)
