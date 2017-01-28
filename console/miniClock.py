#
# miniClock.py
#
#   Configures and runs the clock on the console screen.  This is only ever called
#   by the startMatch screen.
#

from clock import Clock
from globalVariables import RED
import pygame

class MiniClock(Clock):

    defaultHeight = .2           # default height is 50% of screen height
    defaultColor = RED

    def __init__(self,screen,bgcolor):
        screenHeight = screen.get_height()
        screenWidth = screen.get_width()
        targetHeight = MiniClock.defaultHeight * screenHeight

        Clock.__init__(self,targetHeight,MiniClock.defaultColor)

        width = self.clockFace.get_width()
        height = self.clockFace.get_height()

        self.dimensions = pygame.Rect((screenWidth-width)/2,100,width,height)
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

        
