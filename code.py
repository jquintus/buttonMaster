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
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
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
kl = KeyboardLayoutUS(k)

mouse = Mouse(hid.devices)

cc = ConsumerControl(usb_hid.devices)

# Define some helper functions
def move_mouse_to_right_monitor():
    SCREEN_X = 1920 * 2
    SCREEN_Y = 1080 * 2

    """
    MacOS has a concept of "hot corners". A side effect of this is that when
    you move the mouse to the very bottom of the monitor and then move the mouse
    horiztonally to the next monitor, it will get "stuck" in the bottom corner
    and not move past it, possibly also activating whatever behavior is set up
    for that "hot corner". To avoid this, I'm moving the mouse to the bottom of
    the monitor, then up just a little bit to get over the "lip" of the monitor.
    Then I move the mouse horizontally to the right monitor. 
    
    Trying to do this all in one go would likely result in getting caught in that lip.
    """
    mouse.move(y=SCREEN_Y)
    mouse.move(y=-100)
    mouse.move(x = SCREEN_X)
    mouse.move(x=-100)
    time.sleep(0.3)
    mouse.click(Mouse.LEFT_BUTTON)
    time.sleep(0.3)

def zoom_toggle_video():
    move_mouse_to_right_monitor()
    k.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.V)
    time.sleep(0.4)

def zoom_toggle_mute():
    move_mouse_to_right_monitor()
    k.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.A)
    time.sleep(0.4)

def zoom_change_view():
    move_mouse_to_right_monitor()
    k.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.W)
    time.sleep(0.4)

def zoom_start_screen_share():
    """
    Due to a recent change in Zoom's UI, you can no longer use arrow
    keys to navigate their onscreen menus. This means I have to 
    hard code mouse clicks to select the second screen to share.
    """
    move_mouse_to_right_monitor()
    move_mouse_to_right_monitor() # Doing this a secon
                                  # time ensures we kno
                                  # exactly where the mouse is
    
    k.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.S)

    mouse.move(x = -900, y = -650) # Move the mouse to the desktop 2 button

    mouse.click(Mouse.LEFT_BUTTON) # These two lines will double click 
    mouse.click(Mouse.LEFT_BUTTON) # the "Dekstop 2" button"
    
    time.sleep(0.1)

def zoom_start_meeting():
    k.send(Keycode.COMMAND, Keycode.CONTROL, Keycode.V)
    time.sleep(0.4)

def zoom_close_meeting():
    move_mouse_to_right_monitor()
    k.send(Keycode.COMMAND, Keycode.W)
    time.sleep(0.1)
    k.send(Keycode.ENTER)
    time.sleep(0.4)

def zoom_assign_host_and_leave_meeting():
    """
    Leave a meeting you started without stoping the meeting for everyone else.

    To do this, we need to select another meeting participant to become the 
    new host. There are no keyboard shortcut for this, so we have to carefully 
    move the mouse into the right position.
    """
    move_mouse_to_right_monitor()
    move_mouse_to_right_monitor() # Doing this a secon
                                  # time ensures we kno
                                  # exactly where the mouse is
    k.send(Keycode.COMMAND, Keycode.W) # Opens the "End for all or leave" menu
    # time.sleep(0.1)

    mouse.move(x=-750, y=-425)     # Move the cursor to (roughly) 
                                   # the center of the screen which 
                                   # is where the leave button is
    # time.sleep(0.1)
    mouse.click(Mouse.LEFT_BUTTON) # Click the leave button
                                   # this opens the menu to select a new host
                                   # That menu will select the first perso
                                   # by default. We don't need to change that.
    # time.sleep(0.1)
    mouse.click(Mouse.LEFT_BUTTON) # Click the "assign and leave" button
    time.sleep(0.4)


def volume_down():
    print("going down")
    # k.send(VOLUME_DOWN)
    cc.send(ConsumerControlCode.VOLUME_DECREMENT)

def volume_up():
    print("Going up")
    # k.send(VOLUME_UP)
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

while True:
    wait_for_bluetooth_connection(ble)

    while ble.connected:
        if not button_top_red.value:
            print("Button 12 (top red) - Zoom: Toggle Video")
            zoom_toggle_video()

        if not button_bot_red.value:
            print("Button 11 (bot red) - Zoom: Toggle Audio")
            zoom_toggle_mute()

        if not button_top_yel.value:
            print("Button 10 (top yel) - Zoom: Share Screen")
            zoom_start_screen_share()

        if not button_bot_yel.value:
            print("Button  9 (top yel) - Zoom: Change View")
            zoom_change_view()

        if not button_top_grn.value:
            print("Button  5 (top grn) - Zoom: Closing Meeting")
            zoom_close_meeting()

        if not button_bot_grn.value:
            print("Button  6 (bot grn) - Zoom: Assign new host and leave meeting")
            zoom_assign_host_and_leave_meeting()

        # Rotary encoder (volume knob)
        current_position = encoder.position
        position_change = current_position - last_position
        if position_change > 0:
            for _ in range(position_change):
                volume_up()

            print(current_position)

        elif position_change < 0:
            for _ in range(-1 * position_change):
                volume_down()
            print(current_position)

        last_position = current_position

    ble.start_advertising(advertisement)

