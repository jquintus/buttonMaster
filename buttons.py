from adafruit_hid.keycode import Keycode

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

