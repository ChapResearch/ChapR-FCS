#
# mainscreen.py
#
#   The main landing screen for the whole thing.
#

import pygame
from utils import textOutline, numberDraw, coordOffset
from screen import Screen
from buttons import Button
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW
from tables import Table
import virtkeyboard

class MainScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)
        self.titleImage = pygame.image.load("Media/ChapFCS-title.gif").convert()
        self.titlePosition = ((self.screen.get_width()-self.titleImage.get_width())/2,
                              (self.screen.get_height()/4))
        self.tablePosition = (100,175)

        self.screen.fill([0,0,0])             # just black, no graphic background image

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.systemOptions,
                                     **Button.standardButton("NW",["System","Options"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.matchOptions,
                                     **Button.standardButton("NE",["Match","Options"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.about,
                                     **Button.standardButton("SE","About",self.screen))
        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.nextMatch,
                                     **Button.standardButton("S",["Next","Match"],self.screen))

        self.dataTable = Table(fontsize=20,font="monospace")

        self.dataTable.addData("Field Name: ",align="right")
        self.dataTable.addData("Galileo", bold=True, name="fieldName",bgcolor=(50,50,50))
        self.dataTable.endRow()
        self.dataTable.addData("Waiting Robots: ", align="right")
        self.dataTable.addData("4",name="robots",bold=True)
        self.dataTable.endRow()
        self.dataTable.addData("Next Match: ", align="right")
        self.dataTable.addData("10",name="match",callback=self.setMatchNumber,bold=True)
        self.dataTable.endRow()

        self.ButtonFieldName = self.buttons(callback=self.setFieldName,
                                            **Button.tableButton(self.dataTable,"fieldName",self.tablePosition))

        # put out the title
        self.screen.blit(self.titleImage,self.titlePosition)
        self.screen.blit(self.dataTable.image(),self.tablePosition)
#        self.dataTable.updateData("robots",10)

    def setFieldName(self):
        text = self.dataTable.getCellData("fieldName")
        mykeyboard = virtkeyboard.VirtualKeyboard()
        userinput = mykeyboard.run(pygame.display.get_surface(), 200, text)
        print "got user input of: " + userinput
        return userinput

    def setMatchNumber(self):
        pass

    def matchOptions(self):
        return "MatchOptions"

    def systemOptions(self):
        return("SystemOptions")

    def nextMatch(self):
        return("RunMatch")

    def about(self):
        return("AboutScreen")

    def _process(self):
        pass