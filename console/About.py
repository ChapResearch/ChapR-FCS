import pygame
from screen import Screen
from buttons import Button
from textwrap import wrap

class AboutScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)

        self.ButtonS = self.buttons(bgcolor = (255,0,0), callback=self.quit,
                                     **Button.standardButton("S","Quit",self.screen))

        self.str = "The Chap FCS is a project created by Chap Research,\nat Westlake High School, in Austin, Texas. The project was created by Arnhav Iyengar, Jacob Rothfus, Lewis Jones, and Eric Rothfus, in association with FRC Team 2468, Team Appreciate. This system was made to promote fariness and safety in the FTC competition, by creating a consistant, and easy way to start and stop all the robots in a match."
        self.target = 1
        self.str2 = ""
        self.x = 10
        self.y = 75

    def _enter(self):
        self.ButtonS.labels = ("Done",)
        self.ButtonS.flashing = False
        self.redraw()

    def quit(self):
        return "back"

    def redraw(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        x = self.screen.get_width()
        y = self.screen.get_height()
        myfont = pygame.font.SysFont("monospace", 16)
        swidth = myfont.size(self.str)[0]
        sheight = myfont.size(self.str)[1]
        self._setLogo()

        y=self.y
        for line in wrap(self.str,45):
            B1 = myfont.render(line, 1, (255,255,0))
            self.screen.blit(B1,(self.x,y))
            y+=16

#        self._setTitle("About Chap FCS")
        
       
