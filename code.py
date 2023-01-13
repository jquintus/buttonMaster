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

def send_ctrl_shift_alt_combo(keycode):
    k.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ALT, keycode)

def volume_down():
    print("volume going down")
    cc.send(ConsumerControlCode.VOLUME_DECREMENT)

def volume_up():
    print("volume Going up")
    cc.send(ConsumerControlCode.VOLUME_INCREMENT)

def volume_mute():
    print("volume mute")
    cc.send(ConsumerControlCode.MUTE)

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

        # Column 0
        if event.number == 3:
            print("Zoom: Toggle Audio")
            send_ctrl_shift_alt_combo(Keycode.F6)
        elif event.number == 2:
            print("Zoom: Toggle Video")
            send_ctrl_shift_alt_combo(Keycode.F1)
        elif event.number == 1:
            print("Zoom: Copy Invite Link")
            send_ctrl_shift_alt_combo(Keycode.F4)
        elif event.number == 0:
            print("Zoom: raise/lower hand")
            send_ctrl_shift_alt_combo(Keycode.F8)
        # Column 1
        if event.number == 7:
            print("Zoom: Share")
            send_ctrl_shift_alt_combo(Keycode.F2)
        elif event.number == 6:
            print("Zoom: Pause Share")
            send_ctrl_shift_alt_combo(Keycode.F7)
        elif event.number == 5:
            print("Button 5 unset")
        elif event.number == 4:
            print("Button 4 unset")
        # Column 2
        if event.number == 11:
            print("OBS: Switch to Default Scene")
            send_ctrl_shift_alt_combo(Keycode.F11)
            send_ctrl_shift_alt_combo(Keycode.F10)
        elif event.number == 10:
            print("OBS: Toggle Virtual Camera")
            send_ctrl_shift_alt_combo(Keycode.F12)
        elif event.number == 9:
            print("OBS: Screen Shot Output")
            send_ctrl_shift_alt_combo(Keycode.F9)
        elif event.number == 8:
            print("OBS: Transition")
            send_ctrl_shift_alt_combo(Keycode.F10)
        # Column 3
        elif event.number == 15:
            volume_up()

        elif event.number == 14:
            volume_down()

        elif event.number == 13:
            volume_mute()

        elif event.number == 12:
            volume_mute()

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
