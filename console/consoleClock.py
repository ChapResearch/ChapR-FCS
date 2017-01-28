#
# ConsoleClock.py
#
#   Configures and runs the consoleClock.  This is only ever called
#   by the HDMI python process.
#

from clock import Clock
from globalVariables import RED
import pygame

class consoleClock(Clock):

    defaultHeight = .35           # default height is 50% of screen height
    defaultColor = RED

    def __init__(self,screen,bgcolor):
        screenHeight = screen.get_height()
        screenWidth = screen.get_width()
        targetHeight = consoleClock.defaultHeight * screenHeight

        Clock.__init__(self,targetHeight,consoleClock.defaultColor)

        width = self.clockFace.get_width()
        height = self.clockFace.get_height()

        self.dimensions = pygame.Rect((screenWidth-width)/2,(screenHeight-height)/4+20,width,height)
        self.screen = screen
        self.bgcolor = bgcolor

    def _draw(self):
        self.screen.fill(self.bgcolor,self.dimensions)
        self.screen.blit(self.clockFace,self.dimensions)

    def update(self):
        if self._update():                             # returns true if the clock changed
            self._draw()

    def setTime(self,mins,secs):
        Clock.setTime(self,mins,secs)
        self._draw()

    def setColor(self,color):
        Clock.setColor(self,color)

        
