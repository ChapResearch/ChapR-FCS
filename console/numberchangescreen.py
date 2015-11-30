#
# numberchangescreen.py
#
#   Implements the changing of a set of numbers/times.  In fact, there are two modes
#   currently:  3 digit time and 3 digit number.
#
#   This routine will also return a customized button image for the given time/number so
#   that the caller can use it to select which number to change.  This is particularly
#   useful for setting up matches.
#

import pygame
from utils import textOutline, numberDraw
from screen import Screen
from buttons import Button
import globalVariables

class NumberChangeScreen(Screen):

    def __init__(self,name,globalName,mode,title,color):
        Screen.__init__(self,name)

        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.done,
                                     **Button.standardButton("S","Done",self.screen))
        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.cancel,
                                     **Button.standardButton("NW","Cancel",self.screen))

        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.up,
                                     **Button.standardButton("NE","<",self.screen))

        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.down,
                                     **Button.standardButton("SE",">",self.screen))

        self.globalName = globalName
        self.mode = mode
        self.color = color
        self.title = title

    def drawNumber(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        image = numberDraw(self.number,self.mode,
                           self.color,
                           self.height /  2,
                           title=self.title,
                           boxWidth=4)
        self.screen.blit(image,((self.width - image.get_width())/2,(self.height-image.get_height())/2))


    def up(self):
        if self.mode == 0:
            if self.number < (9*60+59):
                self.number += 1
        else:
            if self.number < 999:
                self.number += 1

    def cancel(self):
        return("back")

    def down(self):
        if self.number > 0:
            self.number -= 1
                
    def done(self):
        setattr(globalVariables,self.globalName,self.number)
        return("back")

    def _enter(self):
        self.number = getattr(globalVariables,self.globalName)

    def _process(self):
        self.drawNumber()
