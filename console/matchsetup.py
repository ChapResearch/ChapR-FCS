#
# matchsetup.py
#
#   Screen to begin setup of the next match.
#
import pygame
from screen import Screen
from buttons import Button
from tables import Table
from utils import textOutline, numberDraw
from settings import Settings
import globalVariables as globals
from globalVariables import RED,GREEN,BLUE,YELLOW
from Team import Match

class PrepareMatchScreen(Screen):

    def __init__(self,name,match):
        Screen.__init__(self,name)

        self.match = match

        self.teamB1 = ""
        self.teamR1 = ""
        self.teamB2 = ""
        self.teamR2 = ""

        self.tablePosition = (20,130)
        self.teamTablePosition = (170,200) 

        self.screen.fill([0,0,0])             # just black, no graphic background image

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.setTimes,
                                     **Button.standardButton("NW",["Times &","Match #"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.remoteControl,
                                     **Button.standardButton("NE",["Remote","Control"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (0,0,255), callback=self.robotAssignment,
                                     **Button.standardButton("SW",["Robot","Assign"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,255,255), callback=self.done,lcolor=(0,0,0),
                                     **Button.standardButton("SE","Back",self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,0,0), callback=self.startMatch,
                                     **Button.standardButton("S",["Ready","Match"],self.screen))

    def systemOptions(self):
        return "SystemOptions"

    def matchOptions(self,False):
        return "MatchOptions"

    def remoteControl(self):
        return "RemoteControl"

    def done(self):
        return "back"

    def startMatch(self):
        return "StartMatch"

    def setTimes(self):
        return "MatchSetupScreen"

    def robotAssignment(self):
        print("done")
        return "RobotAssignmentScreen"

    def tableDraw(self):
        self.dataTable = self.tables(fontsize=20,font="arial",align="right",callback=self.setTimes,bgcolor=(0,0,0))
        self.teamTable = self.tables(fontsize=20,font="arial",align="right",cellWidth=45,cellHeight=20)

        # Create the dataTable
        self.dataTable.addData("Next Match:  ",name="matchlabel",flashing=False)
        self.dataTable.addData(self.matchImage,name=0)
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
        self.dataTable.endRow()

        # Create the teamsTable

        self.teamTable.addData(self.teamB1, name = "Team1")
        self.teamTable.addSpacer(5)
        self.teamTable.addData(self.teamR1, name = "Team2")
        self.teamTable.endRow()
        self.teamTable.addData(self.teamB2, name = "Team3")
        self.teamTable.addSpacer(5)
        self.teamTable.addData(self.teamR2, name = "Team4")
        self.teamTable.endRow()


        self.dataTable.position = self.tablePosition
        self.teamTable.position = self.teamTablePosition

    def numberDraw(self):
        self.matchImage = numberDraw(Settings.matchNumber,1,BLUE,20,boxWidth=0,outlined=False)
        self.autoImage = numberDraw(Settings.autoTime,0,YELLOW,20,boxWidth=0,outlined=False)
        self.teleopImage = numberDraw(Settings.teleopTime,0,GREEN,20,boxWidth=0,outlined=False)
        self.endGameImage = numberDraw(Settings.endGameTime,0,RED,20,boxWidth=0,outlined=False)

    def _enter(self):
        globals.BLE.enterMode(1,Settings.fieldName,153)   # start asking for incoming teams
        self._setLogo()
        self._setTitle("Next Match",italic=True,color=(255,0,0))
        self.numberDraw()
        self.testchange = False
        #Setup team variables for table
        if self.match.getTeam(Match.B1) is not None:
            self.teamB1 = self.match.getTeam(Match.B1).getNumber()
        else:
            self.teamB1 = ""
        if self.match.getTeam(Match.R1) is not None:
            self.teamR1 = self.match.getTeam(Match.R1).getNumber()
        else:
            self.teamR1 = ""
        if self.match.getTeam(Match.B2) is not None:
            self.teamB2 = self.match.getTeam(Match.B2).getNumber()
        else:
            self.teamB2 = ""
        if self.match.getTeam(Match.R2) is not None:
            self.teamR2 = self.match.getTeam(Match.R2).getNumber()
        else:
            self.teamR2 = ""
        self.tableDraw()

    def _process(self):
        self.match.getBLE()                      # capture incoming teams
        if True or self.testchange:
            return False
        else:
            self.dataTable.changeData(0)
            self.testchange = True
            return True                           # returning true causes the screen to redraw stuff





