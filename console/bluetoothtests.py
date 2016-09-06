import pygame
from screen import Screen
from buttons import Button
from rn4020 import RN4020
from av1 import AV1
import binascii

class BluetoothTestsScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)


        self.bluetooth = RN4020()  # this will be a BLE control thing eventually
        self.bluetooth.setup()


        self.ButtonNW = self.buttons(bgcolor = (255,0,0), callback=self.mode0broadcast,
                                     **Button.standardButton("NW",["Broadcast","Mode 0"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.stopbroadcast,
                                     **Button.standardButton("SW","STOP",self.screen))
        self.ButtonNE = self.buttons(bgcolor = (255,0,0), callback=self.connection,
                                     **Button.standardButton("NE",["Connection","Test"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,0,0), callback=self.mode1broadcast,
                                     **Button.standardButton("SE",["Broadcast","Mode 1"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done,lcolor=(0,0,0),
                                     **Button.standardButton("S","Done",self.screen))

    def _enter(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        # self._setTitle("Bluetooth Tests")

    def mode1broadcast(self):

        payload = "C4A9"                                   # the magic number
        payload += "%02x" % 1                              # mode one
        payload += binascii.b2a_hex(AV1.pack("Hello",9))   # 9 bytes of name
        payload += "%02x" % 201                            # match number
        payload += "%04x" % (( 6710 &0x7fff)|0x0000)       # R1
        payload += "%04x" % ((10111 &0x7fff)|0x0000)       # R2
        payload += "%04x" % (( 2468 &0x7fff)|0x8000)       # B1
        payload += "%04x" % (( 5628 &0x7fff)|0x0000)       # B2

        self.bluetooth._cmd("N," + payload)
        self.bluetooth._cmd("A")

    def mode0broadcast(self):
#        self.bluetooth.rn4020._cmd("N,11223344")
#        self.bluetooth.rn4020._cmd("A")
#        # hello is 001000 011111 100110 100110 101001 => 00100001 11111001 10100110 101000100
#        self.bluetooth._cmd("N,C4A90021F9A6A400")

        payload = "C4A9"                                   # the magic number
        payload += "%02x" % 0                              # mode zero
        payload += binascii.b2a_hex(AV1.pack("Hello",9))   # 9 bytes of name
        payload += "%02x" % 153                            # match number

        self.bluetooth._cmd("N," + payload)
        self.bluetooth._cmd("A")

    def stopbroadcast(self):
#        self.bluetooth.rn4020._cmd("Y")
        self.bluetooth._cmd("Y")

    def connection(self):
#        self.bluetooth.rn4020._cmd("A")
        self.bluetooth._cmd("A")

    def done(self):
        return "back"
