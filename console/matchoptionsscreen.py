#
# matchoptionsscreen.py
#
#   Screen to direct the user to setting the options for a match,
#   including times, 
#
import pygame
from screen import Screen
from buttons import Button
from tables import Table
from utils import textOutline, numberDraw
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW

class MatchOptionsScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)

        self.tablePosition = (20,150)

        self.screen.fill([0,0,0])             # just black, no graphic background image

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.setTimes,
                                     **Button.standardButton("NW",["Times &","Match #"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.remoteControl,
                                     **Button.standardButton("NE",["Remote","Control"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.done,
                                     **Button.standardButton("S","Done",self.screen))

    def systemOptions(self):
        return "SystemOptions"

    def matchOptions(self):
        return "MatchOptions"

    def remoteControl(self):
        return "RemoteControl"

    def done(self):
        return "back"

    def setTimes(self):
        return "MatchSetupScreen"

    def tableDraw(self):
        self.dataTable = Table(fontsize=20,font="arial",align="right")

        self.dataTable.addData("Next Match:  ",name="matchlabel")
        self.dataTable.addData(self.matchImage,name="match")
        self.dataTable.addSpacer(10)
        self.dataTable.addData("Teleop:  ",     name="teleoplabel")
        self.dataTable.addData(self.teleopImage,name="teleop")
        self.dataTable.endRow()

        self.dataTable.addData("Autonomous:  ", name="autolabel")
        self.dataTable.addData(self.autoImage,  name="auto")
        self.dataTable.addSpacer(20)
        self.dataTable.addData("Endgame:  ",      name="endgamelabel")
        self.dataTable.addData(self.endGameImage, name="endgame")
        self.dataTable.endRow()

        self.dataTable.addData("Remote Control:  ",align="right", bold=False)
        self.dataTable.addData("On",bold=True,align="left")

        self.Buttontimes1 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"autolabel",self.tablePosition))
        self.Buttontimes2 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"auto",self.tablePosition))
        self.Buttontimes3 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"teleoplabel",self.tablePosition))
        self.Buttontimes4 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"teleop",self.tablePosition))
        self.Buttontimes5 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"endgamelabel",self.tablePosition))
        self.Buttontimes6 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"endgame",self.tablePosition))
        self.Buttontimes7 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"matchlabel",self.tablePosition))
        self.Buttontimes8 = self.buttons(callback=self.setTimes,
                                            **Button.tableButton(self.dataTable,"match",self.tablePosition))


    def numberDraw(self):
        self.matchImage = numberDraw(globalVariables.matchNumber,1,BLUE,20,boxWidth=0,outlined=False)
        self.autoImage = numberDraw(globalVariables.autoTime,0,YELLOW,20,boxWidth=0,outlined=False)
        self.teleopImage = numberDraw(globalVariables.teleopTime,0,GREEN,20,boxWidth=0,outlined=False)
        self.endGameImage = numberDraw(globalVariables.endGameTime,0,RED,20,boxWidth=0,outlined=False)

    def _enter(self):
        self._setLogo()
        self._setTitle("Match Options",italic=True,color=(255,0,0))
        self.numberDraw()
        self.tableDraw()
        self.screen.blit(self.dataTable.image(),self.tablePosition)

    def _process(self):
        pass

