import pygame
from screen import Screen
from buttons import Button

class SystemTestsScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)
        self.ButtonNW = self.buttons(bgcolor = (255,0,0), callback=self.buttontest,
                                     **Button.standardButton("NW",["Button","Test"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.networktest,
                                     **Button.standardButton("SW",["Network","Test"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (255,0,0), callback=self.audiotest,
                                     **Button.standardButton("NE",["Audio","Test"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,0,0), callback=self.bletests,
                                     **Button.standardButton("SE",["Bluetooth","Tests"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.quit,lcolor=(0,0,0),
                                     **Button.standardButton("S","Done",self.screen))

        # self.ButtonNE = "Other"
        # self.ButtonSE = "Thing"
        # self.ButtonAction = "Action"
        
    def _enter(self):
        print("entered")
        self.redraw()

    def buttontest(self):
        return "ButtonTestScreen" 

    def networktest(self):
        return "NetworkTests" 

    def audiotest(self):
        self.redraw() 

    def bletests(self):
        return("BluetoothTests")

    def quit(self):
        return "back"

    def redraw(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        x = self.screen.get_width()
        y = self.screen.get_height()
        myfont = pygame.font.SysFont("monospace", 25)
        self._setTitle("System Tests")

    def _process(self):
        return True
