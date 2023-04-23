import time
import board
from digitalio import DigitalInOut, Direction, Pull

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
import usb_hid

import rotaryio

# Set up constants
VOLUME_UP = 0x80
VOLUME_DOWN = 0x81

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

# Set up rotary encoder
encoder = rotaryio.IncrementalEncoder(board.A1, board.A0)
last_position = encoder.position

# Set up Keyboard and Bluethooth
hid = HIDService()

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Josh Industries")
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "White Box"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising bluetooth")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected bluetooth")
    print(ble.connections)

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)

cc = ConsumerControl(hid.devices)

def volume_down():
    print("going down")
    cc.send(ConsumerControlCode.VOLUME_DECREMENT)

def volume_up():
    print("Going up")
    cc.send(ConsumerControlCode.VOLUME_INCREMENT)

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

def send_complex_combo(keycode):
    # We shouldn't need to go through these hoops
    # but when I was testing it, just using `send(...)`
    # would always leave a modifer pressed.
    # Explicitly unpressing the modifier seems to be required.

    k.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ALT, keycode)

while True:
    wait_for_bluetooth_connection(ble)

    while ble.connected:
        if not button_top_red.value:
            print("Button 12 (top red) - Zoom: Toggle Video")
            send_complex_combo(Keycode.F1)
            time.sleep(0.4)

        if not button_bot_red.value:
            print("Button 11 (bot red) - Zoom: Toggle Audio")
            send_complex_combo(Keycode.F6)
            time.sleep(0.4)

        if not button_top_yel.value:
            print("Button 10 (top yel) - Zoom: Share Screen")
            send_complex_combo(Keycode.F2)
            time.sleep(0.4)

        if not button_bot_yel.value:
            print("Button  9 (top yel) - Zoom: Change View")
            send_complex_combo(Keycode.F7)
            time.sleep(0.4)

        if not button_top_grn.value:
            print("Button  5 (top grn) - Zoom: Closing Meeting")
            send_complex_combo(Keycode.F3)
            time.sleep(0.4)

        if not button_bot_grn.value:
            print("Button  6 (bot grn) - Zoom: Assign new host and leave meeting")
            send_complex_combo(Keycode.F8)
            time.sleep(0.4)

        # Rotary encoder (volume knob)
        current_position = encoder.position
        position_change = current_position - last_position
        if position_change > 0:
            for _ in range(position_change):
                volume_down()

            print(current_position)

        elif position_change < 0:
            for _ in range(-1 * position_change):
                volume_up()
            print(current_position)

        last_position = current_position

    ble.start_advertising(advertisement)
