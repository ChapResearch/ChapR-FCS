import pygame
from screen import Screen
from buttons import Button
import globalVariables as globals
from settings import Settings

class BluetoothTestsScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)


        self.ButtonNW = self.buttons(bgcolor = (255,0,0), callback=self.mode1broadcast,
                                     **Button.standardButton("NW",["Broadcast","Mode 0"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.stopbroadcast,
                                     **Button.standardButton("SW","STOP",self.screen))
        self.ButtonNE = self.buttons(bgcolor = (255,0,0), callback=self.connection,
                                     **Button.standardButton("NE",["Connection","Test"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,0,0), callback=self.mode2broadcast,
                                     **Button.standardButton("SE",["Broadcast","Mode 1"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done,lcolor=(0,0,0),
                                     **Button.standardButton("S","Done",self.screen))

    def _enter(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        # self._setTitle("Bluetooth Tests")

    def mode2broadcast(self):
        globals.BLE.enterMode(2,Settings.fieldName,201,6710,10111,2468,5628)

    def mode1broadcast(self):
        globals.BLE.enterMode(1,Settings.fieldName,153)

    def stopbroadcast(self):
        pass
#        self.bluetooth.rn4020._cmd("Y")
#        self.bluetooth._cmd("Y")

    def connection(self):
        pass
#        self.bluetooth.rn4020._cmd("A")
#        self.bluetooth._cmd("A")

    def done(self):
        return "back"
