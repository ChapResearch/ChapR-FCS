#
# optionscreen.py
#
#   Implements changing options or viewing system information.
#   Options implemented here are:
#       - reboot
#       - rescan HDMI
#       - set BLE name (FIELD-1 etc.)
#
#   Sub-screens will be entered for some of these, such as "set BLE name"
#

import pygame
from screen import Screen
from buttons import Button

class OptionScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)
        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.reboot,
                                     **Button.standardButton("NW","Reboot",self.screen))
        self.ButtonSW = self.buttons(bgcolor = (0,0,255), callback=self.setup,
                                     **Button.standardButton("SW","Setup",self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.matchSetup,
                                     **Button.standardButton("NE",["Match","Setup"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.quit,
                                     **Button.standardButton("SE","Quit",self.screen))
        # self.ButtonNE = "Other"
        # self.ButtonSE = "Thing"
        # self.ButtonAction = "Action"

    def reboot(self):
        print("reboot called")
        return("matchNumberChangeScreen")

    def setup(self):
        print("setup called")
        return 

    def matchSetup(self):
        print("going to match setup")
        return "matchSetup"

    def quit(self):
        return "quit"

    def _process(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
