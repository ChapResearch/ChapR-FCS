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
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW
from Team import Match

class PrepareMatchScreen(Screen):

    def __init__(self,name,match):
        Screen.__init__(self,name)

        self.match = match

        self.tablePosition = (20,130)
        self.teamTablePosition = (185,177) 

        self.screen.fill([0,0,0])             # just black, no graphic background image

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.setTimes,
                                     **Button.standardButton("NW",["Times &","Match #"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.remoteControl,
                                     **Button.standardButton("NE",["Remote","Control"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (0,0,255), callback=self.robotAssignment,
                                     **Button.standardButton("SW",["Robot","Assign"],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.remoteControl,
                                     **Button.standardButton("SE",["",""],self.screen))
        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.startMatch,
                                     **Button.standardButton("S",["Start","Match"],self.screen))

    def systemOptions(self):
        return "SystemOptions"

    def matchOptions(self):
        return "MatchOptions"

    def remoteControl(self):
        return "RemoteControl"

    def done(self):
        return "back"

    def startMatch(self):
        pass

    def setTimes(self):
        return "MatchSetupScreen"

    def robotAssignment(self):
        return "RobotAssignmentScreen"

    def tableDraw(self):
        self.dataTable = self.tables(fontsize=20,font="arial",align="right",callback=self.setTimes,bgcolor=(0,0,0))
        self.teamTable = self.tables(fontsize=20,font="arial",align="right",bgcolor=(50,50,50))

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
        self.dataTable.addData(" ", name="space1")
        self.dataTable.endRow()
        self.dataTable.addData(" ", name="space2")
        self.dataTable.endRow()

        # Create the teamsTable
        self.teamTable.addData(self.match.getTeam(Match.R1).getNumber(), name = "Team1", bgcolor=(50,50,50))
        self.teamTable.addSpacer(5)
        self.teamTable.addData(self.match.getTeam(Match.R2).getNumber(), name = "Team2", bgcolor=(50,50,50))
        self.teamTable.endRow()
        self.teamTable.addData(self.match.getTeam(Match.B1).getNumber(), name = "Team3", bgcolor=(50,50,50))
        self.teamTable.addSpacer(5)
        self.teamTable.addData(self.match.getTeam(Match.B2).getNumber(), name = "Team4", bgcolor=(50,50,50))
        self.teamTable.endRow()

        self.dataTable.addData("Remote Control:  ",align="right", bold=False)
        self.dataTable.addData("On",bold=True,align="left")

        self.dataTable.position = self.tablePosition
        self.teamTable.position = self.teamTablePosition

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
        self.testchange = False

    def _process(self):
        if self.testchange:
            return False
        else:
            self.dataTable.changeData(0)
            self.testchange = True
            return True                           # returning true causes the screen to redraw stuff
