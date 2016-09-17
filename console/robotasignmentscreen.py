#
#   robotasignmentscreen
#
#   This file allows the operator to select the participants in a match.
#
import pygame
from screen import Screen
from buttons import Button
from tables import Table
from utils import textOutline, numberDraw
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW
from Team import Match

class RobotAssignmentScreen(Screen):

    def __init__(self,name,match):
        Screen.__init__(self,name)

        self.match = match        
        
        self.tablePosition = (130,10)
        self.trashcanpic = pygame.image.load("Media/trashCan2.png").convert()
        self.trashcanpic = pygame.transform.scale(self.trashcanpic, (37,50))
        self.refreshpic = pygame.image.load("Media/refresh.png").convert()
        self.refreshpic = pygame.transform.scale(self.refreshpic, (50,50))

        self.cb1 = (150,150,150)
        self.cb2 = (50,50,50)
        self.sideBlue = (150,150,255)
        self.sideRed = (255,150,150)

        self.roboSel = None                   #  the index into the Table of robots
        self.trashList = []
        self.AssignButtonPressed = None        #This is set to one of NW NE SW SE or NOne
        self.assignedTeams = { "NW":None, "NE":None, "SW":None, "SE":None }

        self.screen.fill([0,0,0])             # just black, no graphic background image
        self.Button = dict()
        self.Button["NW"] = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,rock = "NW",fontsize = 25,
                                     **Button.standardButton("NW",self.assignedTeams["NW"],self.screen))
        self.Button["NE"] = self.buttons(bgcolor = (255,0,0), callback=self.teamAssign,rock = "NE",fontsize = 25,
                                     **Button.standardButton("NE",self.assignedTeams["NE"],self.screen))
        self.Button["SW"] = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,rock = "SW",fontsize = 25,
                                     **Button.standardButton("SW",self.assignedTeams["SW"],self.screen))
        self.Button["SE"] = self.buttons(bgcolor = (255,0,0), callback=self.teamAssign,rock = "SE",fontsize = 25,
                                     **Button.standardButton("SE",self.assignedTeams["SE"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done, lcolor = (0,0,0),
                                     **Button.standardButton("S","Done",self.screen))
        self.ButtonDel = self.buttons(graphic = self.trashcanpic, callback = self.trashButton,rock = "DelButton",
                                      size=(37,50), position=(130,270), rotation=0,labels=["",""])
        self.ButtonRef = self.buttons(graphic = self.refreshpic, callback = self.refresh,rock = "RefreshButton",
                                      size=(50,50), position=(300,270), rotation=0,labels=["",""])
        self.createSides()

        self.sWidth = self.screen.get_width()
        self.sHeight = self.screen.get_height()
        self.boxHeight = self.sWidth/9
        self.boxWidth = self.sHeight/3
        self.one = "1"
        self.two = "2"
        self.myfont = pygame.font.SysFont("monospace", 30)
        self.myfont.set_bold(True)
        self.N1 = self.myfont.render(self.one,1,(255,255,255))
        self.N2 = self.myfont.render(self.two,1,(255,255,255))
        self.screen.blit(self.N1,(self.boxWidth/2-10,self.boxHeight+10))
        self.screen.blit(self.N2,(self.boxWidth/2-10,self.sHeight-(self.boxHeight+40)))        
        self.screen.blit(self.N1,(self.sWidth-(self.boxWidth/2)-10,self.boxHeight+10))
        self.screen.blit(self.N2,(self.sWidth-(self.boxWidth/2)-10,self.sHeight-(self.boxHeight+40)))        



    #
    # _updateTableDIsplayList() - Update the display list acording to incoming list and trash list.
    #
    def _updateTableDisplayList(self):
        self.displayList =  list(set(self.incomingList)-set(self.trashList))
        self.displayList.sort()

    #
    # _unassignButton() - Remove team from assigned button
    #                     the button is identified by rock
    #
    def _unassignButton(self, rock):
        self.trashList.remove(self.assignedTeams[rock])
        self.Button[rock].setLabels(None)
        

    #
    # _SwapAssignedWithTable() - Swaps assigned team with selcted robot on table.
    #                            the argument rock refers to the assigned team that is swaped.
    #
    def _swapAssignedWithTable(self,rock):
        # First remove the team thats on the button
        self.trashList.remove(self.assignedTeams[rock])
        # Next assign the current selcted table robot to Button
        self._assignTeamToButton(rock)

    #
    # _assignTeamToButton() - Assign the previously clicked team to the button identified by rock
    #
    #
    def _assignTeamToButton(self,rock):
        # move the flashing table robot to the button
        self.trashList.append(self.displayList[self.roboSel])
        self.assignedTeams[rock] = self.displayList[self.roboSel]
        self.Button[rock].setLabels(str(self.displayList[self.roboSel]))
        # Clean up and repaint table
        self.dataTable.setFlash(self.roboSel,False)
        self.roboSel = None
        self.repaintTable()

    #
    #_swap2Buttons() - Swaps two assignedTeam buttons
    #                  the rock refers to the last button clicked
    #                  this routine assumes that the 2 buttons are different
    #                  (you need to ensure this before calling thi routine)
    #
    def _swap2Buttons(self,rock):
        self.Button[self.AssignButtonPressed].setFlash(False)
        if self.assignedTeams[self.AssignButtonPressed] is None:
            checklabel = None
        else:
            checklabel = str(self.assignedTeams[self.AssignButtonPressed])
        self.Button[rock].setLabels(checklabel)
        if self.assignedTeams[rock] is None:
            newlabel = None
        else:
            newlabel = str(self.assignedTeams[rock])
        self.Button[self.AssignButtonPressed].setLabels(newlabel)
        temp = self.assignedTeams[rock]
        self.assignedTeams[rock] = self.assignedTeams[self.AssignButtonPressed]
        self.assignedTeams[self.AssignButtonPressed] = temp

    #nn
    # teamAssign() - Called whenever a corner buton is clicked
    #  n              the rock identifies the buton that was presnsed.
    #
    def teamAssign(self,rock):
        
        # First check if a table button has been clicked previously
        if self.roboSel is not None:
            if self.assignedTeams[rock] is not None:       # Check if there is a team on the button
                self._swapAssignedWithTable(rock)
            else:                                          # There was no team on the button
                self._assignTeamToButton(rock)

        # No Table button had been clicked, but  another assignTeam button had been clicked
        elif self.AssignButtonPressed is not None:
            if rock != self.AssignButtonPressed:
                self._swap2Buttons(rock)
            self.AssignButtonPressed = None
            self.Button[rock].setFlash(False)
        else:
            self.AssignButtonPressed = rock
            self.Button[rock].setFlash(True)

    def trashButton(self,rock):
        self._updateTableDisplayList()
        # Trashes the robot from the table that was reviously clicked
        if self.roboSel is not None:
            self.trashList.append(self.displayList[self.roboSel])
            self.dataTable.setFlash(self.roboSel,False)
            self.roboSel = None
            self.repaintTable()
        #Trashes the the previously selected assigned team
        elif self.AssignButtonPressed is not None:
            if self.assignedTeams[self.AssignButtonPressed] is not None:
                self.trashList.append(self.assignedTeams[self.AssignButtonPressed])
                self.Button[self.AssignButtonPressed].setFlash(False)
                self.Button[self.AssignButtonPressed].setLabels(None)
                self.assignedTeams[self.AssignButtonPressed] = None
                self.AssignButtonPressed = None
                self.repaintTable()
        else:
            del self.trashList[:]
            for team in self.assignedTeams:
                if self.assignedTeams[team] is not None:
                    self.trashList.append(self.assignedTeams[team])
            self._updateTableDisplayList()
            self.repaintTable()
            pass

    def tableButton(self,rock):

        # If a robot from the table was previously selected
        if self.roboSel is not None:
            # If the clicked robot is the same as the one clicked previously then turn flashing off and clear roboSel
            if self.roboSel == rock:
                self.dataTable.setFlash(rock,False)
                self.roboSel = None
            # if the clicked robot is different than previously selected
            else:
                self.dataTable.setFlash(rock,True)
                self.dataTable.setFlash(self.roboSel,False)
                self.roboSel = rock
        # If an assigned team button has been selected previously
        elif self.AssignButtonPressed is not None:
            for teams in self.trashList:
                if teams == self.assignedTeams[self.AssignButtonPressed]:
                   self.trashList.remove(teams)
            self.Button[self.AssignButtonPressed].setLabels(None)
            self.Button[self.AssignButtonPressed].setFlash(False)
            self.assignedTeams[self.AssignButtonPressed] = None
            self.AssignButtonPressed = None
            self.repaintTable()
        else:
            self.dataTable.setFlash(rock,True)
            self.roboSel = rock

    def delete(self):
        trashList.append()

    def done(self):
        self.match.add(Match.B1,self.assignedTeams["NW"])
        self.match.add(Match.R1,self.assignedTeams["NE"])
        self.match.add(Match.B2,self.assignedTeams["SW"])
        self.match.add(Match.R2,self.assignedTeams["SE"])
        return "back"

    def tableCreate(self):
        self.dataTable = self.tables(fontsize=30,font="arial",align="center",cellWidth=110,cellHeight=50)
        

        self.dataTable.addData("", name=0,bgcolor=self.cb1,callback=self.tableButton,rock=0)
        self.dataTable.addData("", name=1,bgcolor=self.cb2,callback=self.tableButton,rock=1)
        self.dataTable.endRow()
        self.dataTable.addData("", name=2,bgcolor=self.cb2,callback=self.tableButton,rock=2)
        self.dataTable.addData("", name=3,bgcolor=self.cb1,callback=self.tableButton,rock=3)
        self.dataTable.endRow()
        self.dataTable.addData("", name=4,bgcolor=self.cb1,callback=self.tableButton,rock=4)
        self.dataTable.addData("", name=5,bgcolor=self.cb2,callback=self.tableButton,rock=5)
        self.dataTable.endRow()
        self.dataTable.addData("", name=6,bgcolor=self.cb2,callback=self.tableButton,rock=6)
        self.dataTable.addData("", name=7,bgcolor=self.cb1,callback=self.tableButton,rock=7)
        self.dataTable.endRow()
        self.dataTable.addData("", name=8,bgcolor=self.cb1,callback=self.tableButton,rock=8)
        self.dataTable.addData("", name=9,bgcolor=self.cb2,callback=self.tableButton,rock=9)
        self.dataTable.endRow()
        self.dataTable.position = self.tablePosition

    def createSides(self):
        widthRed = self.width-self.width/2
        pygame.draw.rect(self.screen,self.sideBlue,(0,0,self.width/2,self.height),0)
        pygame.draw.rect(self.screen,self.sideRed,(widthRed,0,self.width/2,self.height),0)

    def _enter(self):
#        self.incomingList = BLE.OnDeckList()
        self.trashList = list()
        self.incomingList = [6710,5628,80161,12345,7975,2468,8666,9048,118,27]
        self._updateTableDisplayList()
        #Set Labels to blank string to make sure Buttons are refreshed correctly
        self.Button["NW"].setLabels("")
        self.Button["NE"].setLabels("")
        self.Button["SE"].setLabels("")
        self.Button["SW"].setLabels("")
        self.assignedTeams["NW"] = None
        self.assignedTeams["NE"] = None
        self.assignedTeams["SW"] = None
        self.assignedTeams["SE"] = None
        if self.match.getTeam(Match.B1) is not None:
            self.assignedTeams["NW"] = self.match.getTeam(Match.B1).getNumber()
            self.trashList.append(self.match.getTeam(Match.B1).getNumber())
        if self.match.getTeam(Match.R1) is not None:
            self.assignedTeams["NE"] = self.match.getTeam(Match.R1).getNumber()
            self.trashList.append(self.match.getTeam(Match.R1).getNumber())
        if self.match.getTeam(Match.B2) is not None:
            self.assignedTeams["SW"] = self.match.getTeam(Match.B2).getNumber()
            self.trashList.append(self.match.getTeam(Match.B2).getNumber())
        if self.match.getTeam(Match.R2) is not None:
            self.assignedTeams["SE"] = self.match.getTeam(Match.R2).getNumber()
            self.trashList.append(self.match.getTeam(Match.R2).getNumber())
        self.updateButtons()
        self.tableCreate()
        self.lastList = list()
        
        self.repaintTable()

    #
    # UpdateButtons - Used to update buttons to current match Objects
    #
    def updateButtons(self):
        self.Button["NW"].setLabels((str)(self.assignedTeams["NW"]))
        self.Button["NE"].setLabels((str)(self.assignedTeams["NE"]))
        self.Button["SE"].setLabels((str)(self.assignedTeams["SE"]))
        self.Button["SW"].setLabels((str)(self.assignedTeams["SW"]))
            
 
    def repaintTable(self):
        self._updateTableDisplayList()
        button = 0
        self.incomingList.sort(cmp=None, key=None, reverse=False)
        for button in range(0,10):
            self.dataTable.changeData(button,data = "")
            button = 0
        for robot in self.displayList:
            self.dataTable.changeData(button,data = robot)
            button += 1

    def refresh(self):
        pass


    def _process(self):
#       self.incominglist = BLE.OnDeckList()
        returnvalue = False

        # STuff Happens here idk what it is

        self.incomingList = [6710,5628,80161,12345,7975,2468,8666,9048,118,27]
        self._updateTableDisplayList()        
        self.lastList = self.incomingList
        return returnvalue
