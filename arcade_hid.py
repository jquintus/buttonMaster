# Needed to be a bluetooth keyboard
import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse
import usb_hid

class ArcadeKeyboard:
    def start(self):
        # set up keyboard and bluethooth
        hid = HIDService()

        advertisement = ProvideServicesAdvertisement(hid)
        advertisement.appearance = 961
        scan_response = Advertisement()
        scan_response.complete_name = "NeoPixel Buttons"

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

        # private fields 
        self.hid = hid        
        self.ble = ble        
        self.advertisement = advertisement
        self.k = k
        self.kl = kl
        self.mouse = mouse
        self.cc = cc


    def wait_for_bluetooth_connection(self):
        ble = self.ble
        ble_counter = 50000 + 1

        print ("waiting for connection...")
        while not ble.connected:
            ble_counter += 1
            if ble_counter > 50000:
                ble_counter = 0
                print ("waiting for connection...")
            pass

        print("bluetooth connected")


    def start_advertising(self):
        ble = self.ble
        advertisement = self.advertisement

        ble.start_advertising(advertisement)


    def is_connected(self):
        return self.ble.connected

    def get_keyboard(self):
        return self.k

    def get_consumer_control(self):
        return self.cc
