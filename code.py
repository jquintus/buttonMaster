"""
"""
from arcade_hid import ArcadeKeyboard
from buttons import ZoomButtons, VolumeButtons
from white_box_driver import WhiteBoxDriver

ble = ArcadeKeyboard()
ble.start()

def get_commands():
    k = ble.get_keyboard()
    cc = ble.get_consumer_control()

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

    return commands

driver = WhiteBoxDriver(get_commands())
driver.initialize()

while True:
    ble.wait_for_bluetooth_connection()

    while ble.is_connected():
        driver.sync()

    ble.start_advertising()