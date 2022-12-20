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


print("Hello, CircuitPython!")


# create the i2c object for the trellis
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# create the trellis
trellis = NeoTrellis(i2c_bus)

# Set the brightness value (0 to 1.0)
trellis.brightness = 0.5

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

def send_complex_combo(keycode):
    k.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ALT, keycode)

# this will be called when button events are received
def blink(event):
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = GREEN
        print(f'Pressed {event.number}')

        if event.number == 1:
            print("Button 12 (top red) - Zoom: Toggle Video")
            send_complex_combo(Keycode.F1)
        elif event.number == 2:
            print("Button 11 (bot red) - Zoom: Toggle Audio")
            send_complex_combo(Keycode.F6)
        elif event.number == 3:
            print("Button 10 (top yel) - Zoom: Share Screen")
            send_complex_combo(Keycode.F2)
        elif event.number == 4:
            print("Button  9 (top yel) - Zoom: Change View")
            send_complex_combo(Keycode.F7)
        elif event.number == 5:
            print("Button  5 (top grn) - Zoom: Closing Meeting")
            send_complex_combo(Keycode.F3)
        elif event.number == 6:
            print("Button  6 (bot grn) - Zoom: Assign new host and leave meeting")
            send_complex_combo(Keycode.F8)

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
