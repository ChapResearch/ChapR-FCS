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
        
        self.cb1 = (240,220,0)
        self.cb2 = (110,40,180)
        
        self.roboSel = None                   # if this is a robt number then that robot is selected 

        self.screen.fill([0,0,0])             # just black, no graphic background image

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,
                                     **Button.standardButton("NW","",self.screen))
        self.ButtonNE = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,
                                     **Button.standardButton("NE","",self.screen))
        self.ButtonSW= self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,
                                     **Button.standardButton("SW","",self.screen))
        self.ButtonSE = self.buttons(bgcolor = (0,0,255), callback=self.teamAssign,
                                     **Button.standardButton("SE","",self.screen))
        self.ButtonS = self.buttons(bgcolor = (0,0,255), callback=self.done,
                                     **Button.standardButton("S","Done",self.screen))
        self.ButtonDel = self.buttons(bgcolor = (255,0,0), callback = self.delete,
                                      size=(30,30), position=(150,300), rotation=0,labels=["",""])
        self.trashList=[]

    def teamAssign(self):
        print("team assign called")
        
    def tableButton(self,rock):
        print("Table Button Called")
        print(rock)
        if self.roboSel is not None:
            if self.roboSel == rock:
                self.dataTable.changeData(rock,flashing = False)
                print("Turning off flashing for rock")
                self.roboSel = None
            else:
                self.dataTable.changeData(rock,flashing = True)
                self.dataTable.changeData(self.roboSel,flashing=False)
                print("turning on flashing for rock")
                self.roboSel = rock
        else:
            self.dataTable.changeData(rock,flashing = True)
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
        self.dataTable.addData(118, name=8,bgcolor=self.cb1,callback=self.tableButton,rock=8)
        self.dataTable.addData(27, name=9,bgcolor=self.cb2,callback=self.tableButton,rock=9)
        self.dataTable.endRow()
        self.dataTable.position = self.tablePosition



    def _enter(self):
        self.tableCreate()
        self.lastList = list()
 
    def repaintTable(self):
        pass
        
    def _process(self):
#       self.incominglist = BLE.OnDeckList()
        incomingList = (6710,5628,80161,12345,7975,2468,"8666","9048")
        returnvalue = False
        if len(incomingList) > len(self.lastList):
            returnvalue = True
            button = 0
            for robot in incomingList:
                if robot not in self.trashList:
                    self.dataTable.changeData(button,data = robot)
                    button += 1

        # STuff Happens here idk what it is

        self.lastList = incomingList
        return returnvalue
