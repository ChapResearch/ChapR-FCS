# 
# clock.py
#
#   Defines a clock object.  Clock objects are used to display/update
#   pretty count-down clocks.  You will normally sub-class the clock
#   to contain the screen that it is on, and the size that it is initialized
#   to.  Update needs to be called periodically to keep the clock in time with
#   the reset of the planet.
#
#   NOTES:
#     You can access .width and .height - the .width is calculated based upon
#     a 4-digit display: "00:00"
#
#   .draw()                  - draws clock on display
#   .set(mins,secs)          - sets time to given
#   .down()                  - clicks time down one second
#   .pause(True|False)       - displays/not paused banner
#   .color(color)            - color of the digits

import time
import pygame
from globalVariables import WHITE
import utils

class Clock(object):

    defaultFont = "Font/DSEG7Modern-Bold.ttf"

    def __init__(self,height,fontColor,outlineColor=WHITE):
        self.clockFace = self.setFont(height,fontColor,outlineColor)
        self.time = 0
        self.running = False
        self.nextTick = 0

    def setFont(self,height,fontColor,outlineColor = WHITE):
        self.font = pygame.font.Font(Clock.defaultFont,int(height))
        self.width, self.height = self.font.size("8:88")
        self.width += 1     # for outline
        self.setColor(fontColor)
        self.outlineColor = outlineColor
        return pygame.Surface((self.width,self.height))

    def setColor(self,color):
        self.fontColor = color

    def run(self):
        self.running = True

    def stop(self):
        self.running = False

    #
    # setTime() - sets the current time for countdown.  The next countdown
    #             is scheduled for one second in the future.
    #
    def setTime(self,mins,secs=None):
        if secs is None:
            self.time = mins                  # interpret first arg as seconds
        else:
            self.time = mins * 60 + secs      # interpret first arg as minutes
        self.nextTick = pygame.time.get_ticks() + 1000
        #print("next tick set to %d" % self.nextTick)
        self.drawTime()

    def drawTime(self):
        # timeText = "%02d:%02d" % (self.time // 60,self.time % 60)
        timeText = "%01d:%02d" % (self.time // 60,self.time % 60)
        # // makes integer division in python3
        # surface = self.font.render(timeText, True, (0, 255, 0))
        surface = utils.textOutline(self.font,timeText,self.fontColor,self.outlineColor,True)
        self.clockFace.fill((9,9,9))
        self.clockFace.set_colorkey((9,9,9))
        self.clockFace.set_alpha(255)
        self.clockFace.blit(surface,(0,0))

    #
    # _update() - update the clock - counting down if a count-down time has been
    #             reached.
    #
    def _update(self):
        if self.running and self.time > 0 and pygame.time.get_ticks() >= self.nextTick:
            self.time -= 1 
            self.drawTime()
            self.nextTick += 1000                        # by just inc'ing, keeps in sync with clock
            return True
        elif pygame.time.get_ticks() >= self.nextTick:
            self.nextTick += 1000
        return False
