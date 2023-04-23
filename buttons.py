from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

class LambdaButton:
    def __init__(self, name, color, func):
        self.name = name
        self.color = color
        self.onPressFunc = func

    def onPress(self):
        print(f"Pressed - {self.name}")
        self.onPressFunc()

class EmptyButton:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def onPress(self):
        print(f"Pressed - {self.name}")
        print("nothing to do")

class KeyComboButton:
    def __init__(self, name, color, keyboard, *keycodes):
        self.name = name
        self.color = color
        self.keyboard = keyboard
        self.keycodes = keycodes

    def onPress(self):
        print(f"Pressed - {self.name}")
        for keycode in self.keycodes:
            print(f"Pressing {keycode}")
            self.keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ALT, keycode)

class VolumeButton:
    def __init__(self, name, color, consumerControl, volumeCommand):
        self.name = name
        self.color = color
        self.consumerControl = consumerControl
        self.cmd = volumeCommand

    def onPress(self):
        print(f"Pressed - {self.name}")
        cc = self.consumerControl
        cmd = self.cmd
        cc.send(cmd)

class ZoomButtons:
    def __init__(self, color, k):
        self.raise_hand       = KeyComboButton("Zoom: raise/lower hand", color, k, Keycode.F8),
        self.copy_invite_link = KeyComboButton("Zoom: Copy Invite Link", color, k, Keycode.F4),
        self.toggle_video     = KeyComboButton("Zoom: Toggle Video",     color, k, Keycode.F1),
        self.toggle_audio     = KeyComboButton("Zoom: Toggle Audio",     color, k, Keycode.F6),
        self.pause_share      = KeyComboButton("Zoom: Pause Share",      color, k, Keycode.F7),
        self.start_share      = KeyComboButton("Zoom: Share",            color, k, Keycode.F2),

class OBS_Buttons:
    def __init__(self, color, k):
        self.transition              = KeyComboButton("OBS: Transition",               color,  k, Keycode.F10),
        self.screen_shot             = KeyComboButton("OBS: Screen Shot Output",       color,  k, Keycode.F9),
        self.toggle_virtual_camera   = KeyComboButton("OBS: Toggle Virtual Camera",    color,  k, Keycode.F12),
        self.switch_to_default_scene = KeyComboButton("OBS: Switch to Default Scene",  color,  k, Keycode.F11, Keycode.F10),

class VolumeButtons:
    def __init__(self, color, cc):
        self.mute = VolumeButton("Volume Mute", color, cc, ConsumerControlCode.MUTE),
        self.down = VolumeButton("Volume Down", color, cc, ConsumerControlCode.VOLUME_DECREMENT),
        self.up   = VolumeButton("Volume Up",   color, cc, ConsumerControlCode.VOLUME_INCREMENT),
