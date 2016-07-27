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
from settings import Settings
from globalVariables import RED,GREEN,BLUE,YELLOW
import virtkeyboard

class MatchOptionsScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)

        self.tablePosition = (20,150)

        self.screen.fill([0,0,0])             # just black, no graphic background image

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.setTimes,
                                     **Button.standardButton("NW",["Times &","Match #"],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.remoteControl,
                                     **Button.standardButton("NE",["Remote","Control"],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (0,0,255), callback=self.setFieldName,
                                     **Button.standardButton("SW",["Field","Name"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done,lcolor = (0,0,0),
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

    def setFieldName(self):
        text = Settings.fieldName
        mykeyboard = virtkeyboard.VirtualKeyboard()
        userinput = mykeyboard.run(pygame.display.get_surface(), 200, text)
        print "got user input of: " + userinput
        Settings.fieldName = userinput
        Settings.saveSettings()
        print(userinput)
        self.dataTable.changeData("fieldName",data = Settings.fieldName)

    def tableDraw(self):
        self.dataTable = self.tables(fontsize=20,font="arial",align="right",callback=self.setTimes,bgcolor=(0,0,0))

#        self.dataTable.addData("Next Match:  ",name="matchlabel",flashing=True,bgcolor=(50,50,50))
        self.dataTable.addData("Next Match:  ",name="matchlabel")
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

        self.dataTable.addData("Remote Control:  ",align="right", bold=True)
        self.dataTable.addData("On",bold=True,align="left")
        self.dataTable.addSpacer(10)
        self.dataTable.addData("Field Name: ",bold=True)
        self.dataTable.addData(Settings.fieldName,align = "left",name="fieldName")

        self.dataTable.position = self.tablePosition

    def numberDraw(self):
        self.matchImage = numberDraw(Settings.matchNumber,1,BLUE,20,boxWidth=0,outlined=False)
        self.autoImage = numberDraw(Settings.autoTime,0,YELLOW,20,boxWidth=0,outlined=False)
        self.teleopImage = numberDraw(Settings.teleopTime,0,GREEN,20,boxWidth=0,outlined=False)
        self.endGameImage = numberDraw(Settings.endGameTime,0,RED,20,boxWidth=0,outlined=False)

    def _enter(self):
        self._setLogo()
        self._setTitle("Field Options",italic=True,color=(255,0,0))
        self.numberDraw()
        self.tableDraw()

    def _process(self):
        pass
