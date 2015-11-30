#
# startupscreen.py
#
#   Implements the start-up screen, whatever that happens to be!
#

import pygame
from screen import Screen
from buttons import Button

class StartupScreen(Screen):

    def __init__(self):
        Screen.__init__(self,"startup")
        #self.ButtonNW = self.buttons(**Button.standardButton("NW","Reboot",self.screen,self.reboot,self))
        # self.ButtonSW = 
        # self.ButtonNE = "Other"
        # self.ButtonSE = "Thing"
        # self.ButtonAction = "Action"
