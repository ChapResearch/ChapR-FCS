#
# mainscreen.py
#
#   The main landing screen for the whole thing.
#

import pygame
from utils import textOutline, numberDraw, coordOffset
from screen import Screen
from buttons import Button
import globalVariables as globals
from globalVariables import RED,GREEN,BLUE,YELLOW
from tables import Table
import virtkeyboard
from settings import Settings

class MainScreen(Screen):

    matchNum = Settings.matchNumber

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
                                     **Button.standardButton("NE",["Field","Options"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.about,
                                     **Button.standardButton("SE","About",self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.nextMatch, lcolor = (0,0,0),
                                     **Button.standardButton("S",["Next","Match"],self.screen))


        self.dataTable = self.tables(fontsize=20,font="monospace")

        self.dataTable.addData("Field Name: ",align="right")
        self.dataTable.addData(Settings.fieldName, bold=True, name="fieldName",bgcolor=(50,50,50),callback=self.setFieldName)
        self.dataTable.endRow()
        self.dataTable.addData("Next Match: ", align="right")
        self.dataTable.addData(Settings.matchNumber,name="match",callback=self.setMatchNumber,bold=True)
        self.dataTable.endRow()

        # put out the title
        self.screen.blit(self.titleImage,self.titlePosition)
        self.dataTable.position = self.tablePosition

    def setFieldName(self):
        text = Settings.fieldName
        mykeyboard = virtkeyboard.VirtualKeyboard()
        userinput = mykeyboard.run(pygame.display.get_surface(), 200, text)
        Settings.fieldName = userinput
        Settings.saveSettings()
        self.dataTable.changeData("fieldName",data = Settings.fieldName)
        globals.BLE.enterMode(0,Settings.fieldName)

    def setMatchNumber(self):
        return("matchNumberChangeScreen")

    def matchOptions(self):
        return "MatchOptions"

    def systemOptions(self):
        return("SystemOptions")

    def nextMatch(self):
        return("PrepareMatch")

    def about(self):
        return("AboutScreen")

    def _enter(self):
        # whenever this screen is shown, we are in the simple mode 0
        # simply broadcasting our presence
        globals.BLE.enterMode(0,Settings.fieldName)

    def _process(self):
        pass
