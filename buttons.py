from adafruit_hid.keycode import Keycode

class LambdaButton:
    def __init__(self, name, func):
        self.name = name
        self.onPressFunc = func

    def onPress(self):
        print(f"Pressed - {self.name}")
        self.onPressFunc()

class EmptyButton:
    def __init__(self, name):
        self.name = name

    def onPress(self):
        print(f"Pressed - {self.name}")
        print("nothing to do")

class KeyComboButton:
    def __init__(self, name, keyboard, *keycodes):
        self.name = name
        self.keyboard = keyboard
        self.keycodes = keycodes

    def onPress(self):
        print(f"Pressed - {self.name}")
        for keycode in self.keycodes:
            print(f"Pressing {keycode}")
            self.keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ALT, keycode)

class VolumeButton:
    def __init__(self, name, consumerControl, volumeCommand):
        self.name = name
        self.consumerControl = consumerControl
        self.cmd = volumeCommand

    def onPress(self):
        print(f"Pressed - {self.name}")
        cc = self.consumerControl
        cmd = self.cmd
        cc.send(cmd)

