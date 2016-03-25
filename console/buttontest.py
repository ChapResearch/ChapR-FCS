import pygame
from screen import Screen
from buttons import Button

class ButtonTestScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)
        self.ButtonNW = self.buttons(bgcolor = (255,0,0), callback=self.button1,
                                     **Button.standardButton("NW",["Button","1"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.button2,
                                     **Button.standardButton("SW",["Button","2"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (255,0,0), callback=self.button3,
                                     **Button.standardButton("NE",["Button","3"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,0,0), callback=self.button4,
                                     **Button.standardButton("SE",["Button","4"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,0,0), callback=self.quit,
                                     **Button.standardButton("S","Quit",self.screen))

        self.str = "Press the 1st button."
        self.target = 1
        self.str2 = ""
        # self.ButtonNE = "Other"
        # self.ButtonSE = "Thing"
        # self.ButtonAction = "Action"

    def button1(self):
        print("Button 1 is working")
        self.str2 = ""
        if self.target == 1:
            self.str = "Press the 2nd button."
            self.target += 1
        elif self.target == 5:
            return "back"
        else:
            self.str = "ERROR! Wrong button pressed."
            self.str2 = "Press Button " + str(self.target)

    def button2(self):
        print("Button 2 is working")
        self.str2 = ""
        if self.target == 2:
            self.str = "Press the 3rd button."
            self.target += 1
        elif self.target == 5:
            return "back"
        else:
            self.str = "ERROR! Wrong button pressed."
            self.str2 = "Press Button " + str(self.target)

    def button3(self):
        print("Button 3 is working")
        self.str2 = ""
        if self.target == 3:
            self.str = "Press the 4th button."
            self.target += 1
        elif self.target == 5:
            return "back"
        else:
            self.str = "ERROR! Wrong button pressed."
            self.str2 = "Press Button " + str(self.target)

    def button4(self):
        if self.target==4:
            self.str = "Press any button to continue."
            self.str2 = ""
            self.target += 1
        elif self.target == 5:
            return "back"
        else:
            self.str = "ERROR! Wrong button pressed."
            self.str2 = "Press Button " + str(self.target)

    def quit(self):
        return "back"

    def _process(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        x = self.screen.get_width()
        y = self.screen.get_height()
        myfont = pygame.font.SysFont("monospace", 25)
        swidth = myfont.size(self.str)[0]
        sheight = myfont.size(self.str)[1]
        swidth2 = myfont.size(self.str2)[0]
        B1 = myfont.render(self.str, 1, (255,255,0))
        B2 = myfont.render(self.str2, 1, (255,255,0))
        myfont2 = pygame.font.SysFont("monospace", 35)
        #self.BBT = "Button Test"
        #B3 = myfont2.render(self.BBT,1,(255,0,0))
        #swidth3 = myfont2.size(self.BBT)[0]
        #self.screen.blit(B3,((x - swidth3)/2,100))
        self._setTitle("Button Test")
        self.screen.blit(B1,((x - swidth)/2,(y - sheight)/2))
        self.screen.blit(B2,((x - swidth2)/2,(y - sheight)/2+sheight))
