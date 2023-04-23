"""
"""
import time
import board
from digitalio import DigitalInOut, Direction, Pull

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
import usb_hid

import rotaryio

from buttons import ZoomButtons, VolumeButtons

def create_digital_buttons():
    # Set up buttons
    button_top_red = DigitalInOut(board.D12)
    button_top_red.direction = Direction.INPUT
    button_top_red.pull = Pull.UP

    button_bot_red = DigitalInOut(board.D11)
    button_bot_red.direction = Direction.INPUT
    button_bot_red.pull = Pull.UP

    button_top_yel = DigitalInOut(board.D10)
    button_top_yel.direction = Direction.INPUT
    button_top_yel.pull = Pull.UP

    button_bot_yel = DigitalInOut(board.D9)
    button_bot_yel.direction = Direction.INPUT
    button_bot_yel.pull = Pull.UP

    button_bot_grn = DigitalInOut(board.D6)
    button_bot_grn.direction = Direction.INPUT
    button_bot_grn.pull = Pull.UP

    button_top_grn = DigitalInOut(board.D5)
    button_top_grn.direction = Direction.INPUT
    button_top_grn.pull = Pull.UP

    buttons = [
        button_top_red, 
        button_bot_red, 
        button_top_yel, 
        button_bot_yel, 
        button_top_grn,
        button_bot_grn, 
    ]

    return buttons


# Set up rotary encoder
encoder = rotaryio.IncrementalEncoder(board.A1, board.A0)
last_position = encoder.position

# Set up Keyboard and Bluethooth
hid = HIDService()

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "CircuitPython HID 2"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising bluetooth")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected bluetooth")
    print(ble.connections)

k = Keyboard(hid.devices)
cc = ConsumerControl(hid.devices)

def wait_for_bluetooth_connection(ble):
    ble_counter = 50000 + 1

    print ("Waiting for connection...")
    while not ble.connected:
        ble_counter += 1
        if ble_counter > 50000:
            ble_counter = 0
            print ("Waiting for connection...")
        pass
    print("Start typing:")

zoom = ZoomButtons("zoom", k)
volume = VolumeButtons("volume", cc)

buttons = create_digital_buttons()
commands = [ 
    zoom.toggle_video,
    zoom.toggle_audio,
    zoom.start_share,
    zoom.pause_share,
    zoom.copy_invite_link,
    zoom.raise_hand
]
            
def raise_button(idx):
    cmd = commands[idx]
    cmd.onPress()

while True:
    wait_for_bluetooth_connection(ble)

    while ble.connected:
        for idx in range(len(buttons)):
            button = buttons[idx]
            if not button.value:
                raise_button(idx)
                time.sleep(0.4)

        # Rotary encoder (volume knob)
        current_position = encoder.position
        position_change = current_position - last_position
        if position_change > 0:
            for _ in range(position_change):
                volume.down.onPress()

            print(current_position)

        elif position_change < 0:
            for _ in range(-1 * position_change):
                volume.up.onPress()
            print(current_position)

        last_position = current_position

    ble.start_advertising(advertisement)
