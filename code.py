"""
"""
import time

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
import usb_hid

from buttons import ZoomButtons, VolumeButtons
from WhiteBoxDriver import WhiteBoxDriver

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

commands = [ 
    zoom.toggle_video,
    zoom.toggle_audio,
    zoom.start_share,
    zoom.pause_share,
    zoom.copy_invite_link,
    zoom.raise_hand,
    volume.down,
    volume.up,
]

driver = WhiteBoxDriver(commands)
driver.initialize()

def raise_button(idx):
    cmd = commands[idx]
    cmd.onPress()

while True:
    wait_for_bluetooth_connection(ble)

    while ble.connected:
        driver.sync()

    ble.start_advertising(advertisement)
