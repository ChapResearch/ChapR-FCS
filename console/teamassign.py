import pygame
from screen import Screen
from buttons import Button

class TeamAssignScreen(Screen):

    def __init__(self):
        Screen.__init__(self,"TeamAssign")
        self.ButtonNW = self.buttons(bgcolor = (100,100,0), callback=self.reboot,
                                     **Button.standardButton("NW","Reboot",self.screen))
        self.ButtonSW = self.buttons(bgcolor = (0,0,255), callback=self.setup,
                                     **Button.standardButton("SW","Yes",self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.matchSetup,
                                     **Button.standardButton("NE",["Match","Setup"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.quit,
                                     **Button.standardButton("SE","Quit",self.screen))
        # self.ButtonNE = "Other"
        # self.ButtonSE = "Thing"
        # self.ButtonAction = "Action"

    def reboot(self):
        print("reboot called")
        return "option"

    def setup(self):
        print("setup called")
        return None

    def matchSetup(self):
        print("going to match setup")
        return "matchSetup"

    def quit(self):
        return "quit"

    def _process(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
