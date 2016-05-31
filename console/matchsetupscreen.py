#
# matchsetupscreen.py
#
#   Implements match setup thingies.
#
#   Four things are done - match number, autonomous period length, teleop period length, end-game length.
#   All times are three digits only:  0:00
#   Match number is also three digits 000.
#   The screen is divided in half, roughly, with match number on the left, and times on the right.
#
#   The screen is divided into 
#

import pygame
from utils import textOutline, numberDraw
from screen import Screen
from buttons import Button
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW
from hardware import HARDWARE

class MatchSetupScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)

        self.screen.fill([0,0,0])             # just black, no graphic background image

        # go ahead and calculate the time display/buttons

        self.buttonHeight = self.height/3
        self.buttonPadding = self.width/25

        self.matchImage, self.autoImage, self.teleopImage, self.endGameImage = self.numberImages(self.buttonHeight)
        self.buttonWidth = self.matchImage.get_width()
        self.matchPos, self.autoPos, self.teleopPos, self.endGamePos = self.numberPositions(self.buttonHeight,
                                                                                            self.buttonWidth,
                                                                                            self.buttonPadding)
        
        self.matchButton = self.buttons((self.buttonWidth,self.buttonHeight),self.matchPos,
                                        graphic=self.matchImage, callback=self.editMatchNumber,gpio=HARDWARE.button.NW)
        self.autoButton = self.buttons((self.buttonWidth,self.buttonHeight),self.autoPos,
                                       graphic=self.autoImage, callback=self.editAutoNumber,gpio=HARDWARE.button.SW)
        self.teleopButton = self.buttons((self.buttonWidth,self.buttonHeight),self.teleopPos,
                                         graphic=self.teleopImage, callback=self.editTeleopNumber,gpio=HARDWARE.button.NE)
        self.endGameButton = self.buttons((self.buttonWidth,self.buttonHeight),self.endGamePos,
                                          graphic=self.endGameImage, callback=self.editEndGameNumber,gpio=HARDWARE.button.SE)

        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.done,
                                     **Button.standardButton("S","Done",self.screen))

    def done(self):
        return("back")

    def editMatchNumber(self):
        return("matchNumberChangeScreen")

    def editTimeNumber(self):
        return("matchNumberChangeScreen")

    def editTeleopNumber(self):
        return("teleopTimeChangeScreen")

    def editAutoNumber(self):
        return("autoTimeChangeScreen")

    def editEndGameNumber(self):
        return("endGameTimeChangeScreen")

    #
    # numberImages() - draw the number images and return a list of them
    #
    def numberImages(self,imageHeight):
        matchImage = numberDraw(globalVariables.matchNumber,1,BLUE,imageHeight, title="Match:")
        autoImage = numberDraw(globalVariables.autoTime,0,YELLOW,imageHeight, title="Autonomous:")
        teleopImage = numberDraw(globalVariables.teleopTime,0,GREEN,imageHeight, title="Teleop:")
        endGameImage = numberDraw(globalVariables.endGameTime,0,RED,imageHeight, title="End Game:")
        return((matchImage,autoImage,teleopImage,endGameImage))

    #
    # numberPositions() - return a list of the positions of the images, same order
    #
    def numberPositions(self,imageHeight,imageWidth,edgePadding):
        matchPos = (edgePadding,edgePadding)
        autoPos = (edgePadding,edgePadding*2+imageHeight)
        teleopPos = (self.width - imageWidth - edgePadding,edgePadding)
        endGamePos = (self.width - imageWidth - edgePadding,edgePadding*2+imageHeight)
        return((matchPos,autoPos,teleopPos,endGamePos))

    def _enter(self):
        self.matchButton.graphic, self.autoButton.graphic, self.teleopButton.graphic, self.endGameButton.graphic = self.numberImages(self.buttonHeight)
        
    def _process(self):
        pass

