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

class RobotAssignmentScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)

        self.tablePosition = (130,10)
        self.trashcanpic = pygame.image.load("Media/Trashcan.png").convert()
        self.trashcanpic = pygame.transform.scale(self.trashcanpic, (50,50))

        self.cb1 = (240,220,0)
        self.cb2 = (110,40,180)
        
        self.roboSel = None                   # if this is a robt number then that robot is selected 
        self.trashList = []
        self.AssignButtonPressed = None        #This is set to one of NW NE SW SE or NOne
        self.assignedTeams = { "NW":None, "NE":None, "SW":None, "SE":None }

        self.screen.fill([0,0,0])             # just black, no graphic background image
        self.Button = dict()
        self.Button["NW"] = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,rock = "NW",
                                     **Button.standardButton("NW","",self.screen))
        self.Button["NE"] = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,rock = "NE",
                                     **Button.standardButton("NE","",self.screen))
        self.Button["SW"] = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,rock = "SW",
                                     **Button.standardButton("SW","",self.screen))
        self.Button["SE"] = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,rock = "SE",
                                     **Button.standardButton("SE","",self.screen))
        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.done,rock = "S",
                                     **Button.standardButton("S","Done",self.screen))
        self.ButtonDel = self.buttons(graphic = self.trashcanpic, callback = self.trashButton,rock = "DelButton",
                                      size=(50,50), position=(130,275), rotation=0,labels=["",""])

    def teamAssign(self,rock):
        print("team assign called")
#        self.Button[rock].labels = ["Hello",]
#        self.Button[rock].flashing = True
        if self.roboSel is not None:
            print("This aint working")
            print("Changing the name of team assign Button")
            modifiedList = []
            for robot in self.incomingList:
                print(robot)
                if robot not in self.trashList:
                    print(robot)
                    modifiedList.append(robot)
                else:
                    robot += 1
            self.trashList.append(modifiedList[self.roboSel])
            self.Button[rock].labels = [str(modifiedList[self.roboSel]),]
            self.assignedTeams[rock] = modifiedList[self.roboSel]
            print(self.incomingList[self.roboSel])                                      
            self.dataTable.setFlash(self.roboSel,False)
            self.roboSel = None
            self.repaintTable()
        elif self.AssignButtonPressed is not None:
            if rock != self.AssignButtonPressed:
                self.Button[self.AssignButtonPressed].flashing = False
                self.Button[rock].labels = [str(self.assignedTeams[self.AssignButtonPressed])]
                self.Button[self.AssignButtonPressed].labels = [str(self.assignedTeams[rock])]
                temp = self.assignedTeams[rock]
                self.assignedTeams[rock] = self.assignedTeams[self.AssignButtonPressed]
                self.assignedTeams[self.AssignButtonPressed] = temp
            self.AssignButtonPressed = None
            self.Button[rock].flashing = False
        else:
            self.AssignButtonPressed = rock
            self.Button[rock].flashing = True

    def trashButton(self,rock):
        if self.roboSel is not None:
            self.trashList.append(self.incomingList[self.roboSel])
            self.dataTable.setFlash(self.roboSel,False)
            self.roboSel = None
            self.repaintTable()
        elif self.AssignButtonPressed is not None:
            if self.assignedTeams[self.AssignButtonPressed] is not None:
                self.trashList.append(self.assignedTeams[self.AssignButtonPressed])
                self.Button[self.AssignButtonPressed].flashing = False
                self.Button[self.AssignButtonPressed].labels = " "
                self.assignedTeams[self.AssignButtonPressed] = None
                self.AssignButtonPressed = None
                self.repaintTable()
            else:
                pass

    def tableButton(self,rock):
        print("Table Button Called")
        print(rock)
        if self.roboSel is not None:
            if self.roboSel == rock:
                self.dataTable.setFlash(rock,False)
                print("Turning off flashing for rock")
                self.roboSel = None
            else:
                self.dataTable.setFlash(rock,True)
                self.dataTable.setFlash(self.roboSel,False)
                print("turning on flashing for rock")
                self.roboSel = rock
        elif self.AssignButtonPressed is not None:
            print[self.trashList]
            for teams in self.trashList:
                print(self.trashList)
                if teams == self.assignedTeams[self.AssignButtonPressed]:
                   self.trashList.remove(teams)
            self.Button[self.AssignButtonPressed].labels = " "
            self.Button[self.AssignButtonPressed].flashing = False
            self.AssignButtonPressed = None
            self.repaintTable()
        else:
            self.dataTable.setFlash(rock,True)
            print("Turning on flashing for rock")
            self.roboSel = rock


    def delete(self):
        print("Yeet delete")
        trashList.append()

    def done(self):
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



    def _enter(self):
        self.tableCreate()
        self.lastList = list()
 
    def repaintTable(self):
        print("YOOOOO")
        print(self.trashList)
        button = 0
        self.incomingList.sort(cmp=None, key=None, reverse=False)
        for button in range(0,10):
            print("yeet")
            self.dataTable.changeData(button,data = "")
            button = 0
        for robot in self.incomingList:
            print(robot)
            if robot not in self.trashList:
                print(robot)
                self.dataTable.changeData(button,data = robot)
                button += 1


    def _process(self):
#       self.incominglist = BLE.OnDeckList()
        self.incomingList = [6710,5628,80161,12345,7975,2468,8666,9048,118,27]
        self.incomingList.sort(cmp=None, key=None, reverse=False)
        returnvalue = False
        if len(self.incomingList) > len(self.lastList):
            self.repaintTable()
            returnvalue = True
                    
        # STuff Happens here idk what it is

        self.lastList = self.incomingList
        return returnvalue
