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
from utils import textOutline, numberDraw, removeKey
from screen import Screen
from buttons import Button
import globalVariables
import datetime
from settings import Settings

class NumberChangeScreen(Screen):

    heldGranularity = datetime.timedelta(0,0,100000)    # 10 incs per second

    def __init__(self,name,globalName,mode,title,color):
        Screen.__init__(self,name)

        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.done,
                                     **Button.standardButton("S","Done",self.screen))
        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.cancel,
                                     **Button.standardButton("NW","Cancel",self.screen))

        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.up, upCallback=self.release,
                                     holdCallback = self.holdCountUp, rotation = 180,
                                     **removeKey(Button.standardButton("NE","V",self.screen),'rotation'))

        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.down, upCallback=self.release,
                                     holdCallback = self.holdCountDown,
                                     **Button.standardButton("SE","V",self.screen))
        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.permenance,
                                     **Button.standardButton("SW","Permenance",self.screen))

        self.globalName = globalName
        self.mode = mode
        self.color = color
        self.title = title
        self.heldCountUp = False
        self.heldCountDown = False
        self.heldLastTime = datetime.datetime.now()
        self.needsUpdate = True
        self.PT = True

    def drawNumber(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        image = numberDraw(self.number,self.mode,
                           self.color,
                           self.height /  2,
                           title=self.title,
                           boxWidth=4)
        self.screen.blit(image,((self.width - image.get_width())/2,(self.height-image.get_height())/2))
        self.needsUpdate = True


    def holdCountUp(self):
        self.heldCountUp = True
        self.heldLastTime = datetime.datetime.now()

    def holdCountDown(self):
        self.heldCountDown = True
        self.heldLastTime = datetime.datetime.now()

    def release(self):
        self.heldCountUp = False
        self.heldCountDown = False

    def up(self):
        if self.mode == 0:
            if self.number < (9*60+59):
                self.number += 1
                self.drawNumber()
        else:
            if self.number < 999:
                self.number += 1
                self.drawNumber()

    def cancel(self):
        return("back")

    def down(self):
        if self.number > 0:
            self.number -= 1
            self.drawNumber()

    def permenance(self):
        if self.PT == False:
            self.PT = True
            self.ButtonSW.setLabels("Permenant")
        else:
            self.PT = False
            self.ButtonSW.setLabels("Temporary")
                
    def done(self):
#        setattr(globalVariables,self.globalName,self.number)
        setattr(Settings,self.globalName,self.number)
        if self.PT == True:
            Settings.saveSettings()
        return("back")

    def _enter(self):
        self.number = getattr(Settings,self.globalName)
        self.drawNumber()

    def _process(self):
        if self.heldCountUp or self.heldCountDown:
            now = datetime.datetime.now()
            if now - self.heldLastTime > NumberChangeScreen.heldGranularity:
                self.heldLastTime = now
                if self.heldCountUp:
                    self.up()
                if self.heldCountDown:
                    self.down()
                self.drawNumber()
        returnNeedsUpdate = self.needsUpdate
        self.needsUpdate = False
        return returnNeedsUpdate
