#
# systemoptionsscreen.py
#
#   Show the system options.  Includes:
#
#  ,------------------------,
#  | Field           HDMI & |
#  | Name            Audio  |
#  |                        |
#  |               Network &|
#  | Tests    Done  Internet|
#  '------------------------'
#   Network (IP address on screen)
#      WiFi
#         SSID
#         Password
#   HDMI Resolution (resolution on screen)
#   Audio (HDMI or Output jack) (current settign on screen)
#   Internet
#      Log Matches
#      Load Ads
#   Button Test
#   Screen Test
#   Done

import pygame
from screen import Screen
from buttons import Button
from tables import Table
from utils import textOutline, numberDraw
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW
import virtkeyboard
from settings import Settings

class SystemOptionsScreen(Screen):
    
    def __init__(self,name):
        Screen.__init__(self,name)
        
        

        self.tablePosition = (20,150)

        self.screen.fill([0,0,0])             # just black, no graphic background image

        self.ButtonNW = self.buttons(bgcolor = (255,0,0), callback=self.setFieldName,
                                     **Button.standardButton("NW",["Field","Name"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (255,0,0), callback=self.hdmiAudio,
                                     **Button.standardButton("NE",["HDMI &","Audio"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.tests,
                                     **Button.standardButton("SW","Tests",self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,0,0), callback=self.networkInternet,
                                     **Button.standardButton("SE",["Network &","WiFi"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done, lcolor=(0,0,0),
                                     **Button.standardButton("S","Done",self.screen))


    def setFieldName(self):
        text = Settings.fieldName
        mykeyboard = virtkeyboard.VirtualKeyboard()
        userinput = mykeyboard.run(pygame.display.get_surface(), 200, text)
        print "got user input of: " + userinput
        Settings.fieldName = userinput
        Settings.saveSettings()
        print(userinput)
        self.dataTable.changeData("fieldName",data = Settings.fieldName)

    def hdmiAudio(self):
        pass

    def tests(self):
        return "SystemTests"

    def done(self):
        return "back"

    def networkInternet(self):
        pass

    def tableDraw(self):
        self.dataTable = self.tables(fontsize=20,font="monospace")

        self.dataTable.addData("Field Name: ",align="right")
        self.dataTable.addData(Settings.fieldName, bold=True, name="fieldName",bgcolor=(50,50,50))
        self.dataTable.endRow()
        self.dataTable.addData("Next Match: ", align="right")
        self.dataTable.addData("10",name="match",bold=True)
        self.dataTable.endRow()

        self.dataTable.position = self.tablePosition

    def _enter(self):
        self._setLogo()
        self._setTitle("System Options",italic=True,color=(0,0,255))
        self.tableDraw()

    def _process(self):
        pass

    


