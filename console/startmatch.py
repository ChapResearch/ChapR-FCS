

#
#
# StartMatchScreen - The screen meant to run the match timer, and if robotControl is enabled it will start and stop the robots.
#
#

import pygame
from screen import Screen
from buttons import Button
from tables import Table
from HDMIclock import HDMIClock
from globalVariables import RED,GREEN,BLUE,YELLOW,BLACK,WHITE
from Team import Match
import os
from statsdisplay import StatsDisplay
from settings import Settings
from matchsetup import PrepareMatchScreen

class StartMatchScreen(Screen):

    #self.matchState
    ENTER = 0    #
    INIT = 1     #    INIT - the state in which robots initialize
    INITsT = 2   #    INITsT - inbetween INIT and AUTO state
    AUTO = 3     #    AUTO - The state in which autonomous runs
    AUTOsT = 4   #    AUTOsT - inbetween state of AUTO and TELEOP
    TELEOP = 5   #    TELEOP - teleop runs
    END = 6      #    END - endgame
    TELEOPsT = 7 #    TELEOPsT - end of match state
    STOP = 8     #    STOP - pauses match

    def __init__(self,name,match,bigScreen):
        Screen.__init__(self,name)

        self.screen.fill([0,0,0])

        self.match = match

        self.clock = HDMIClock(self.screen,BLACK)
        self.bigScreen = bigScreen
        self.bigStopped = False
        self.bigScreen.fill(0,0,0)

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), rock = "NW",fontsize = 20,
                                     **Button.standardButton("NW",["Stop",""],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (255,0,0), rock = "NE",fontsize = 20,
                                     **Button.standardButton("NE",["Stop",""],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (0,0,255), rock = "SW",fontsize = 20,
                                     **Button.standardButton("SW",["Stop",""],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,0,0), rock = "SE",fontsize = 20,
                                     **Button.standardButton("SE",["Stop",""],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.initialize, lcolor = (0,0,0),
                                     **Button.standardButton("S",["Initialize"],self.screen))
        self.ButtonN = self.buttons(bgcolor = (0,0,0), callback=self.endMatch, lcolor = (0,0,0),
                                     **Button.standardButton("N","Yep",self.screen))

    def done(self):
        PrepareMatchScreen.match.clear()
        return "back"

    def none(self):
        pass

    def endMatch(self):
        return "MainScreen"
    
    #Redraws the team numbers and stats on HDMI screen
    #        -The stats variable determines whether stats are drawn
    def redrawStats(self,stats=True):
        self.bigScreen.fill(0,0,0)
        self.bigScreen.cteam("NW","148",4,95,88,stats)
        self.bigScreen.cteam("NE","2468",1,35,56,stats)
        self.bigScreen.cteam("SW","5628",3,100,100,stats)
        self.bigScreen.cteam("SE","10241",3,10,13,stats)        

    #Pause Function for match
    def stopMatch(self):
        self.clock.stop()
        self.bigScreen.clockStop()
        self.matchState = StartMatchScreen.STOP
        # Make North Button Appear
        self.ButtonN.setLabels(["End","Match"])
        self.ButtonN.callBack = self.endMatch
        self.ButtonN.bgcolor = (255,255,255)
        # Check what section of match to go back to
        if self.matchSection == StartMatchScreen.AUTO:
            self.ButtonS.callback = self.startAutonomous
            self.ButtonS.setLabels(["Start","Autonomous"])
        elif self.matchSection == StartMatchScreen.TELEOP:
            self.ButtonS.callback = self.startTeleop
            self.ButtonS.setLabels(["Start","Teleop"])

    def initialize(self):
        self.matchState = StartMatchScreen.INIT
        print("Initialized")
        self.matchState - StartMatchScreen.INITsT
        self.ButtonS.callback = self.startAutonomous
        self.ButtonS.setLabels(["Start","Autonomous"])
        
    def startTeleop(self):
        print("StartTeleop")
        self.matchSection = StartMatchScreen.TELEOP
        self.matchState = StartMatchScreen.TELEOP
        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartTeleop.wav'))
        self.soundFX.play()
        self.ButtonS.setLabels(["Pause","Teleop"])
        self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
        self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)        
        self.ButtonS.callback = self.stopMatch
        # Make North Button Dissapear
        self.ButtonN.setLabels("")
        self.ButtonN.callBack = self.none
        self.ButtonN.bgcolor = (0,0,0)

    def startAutonomous(self):
        self.soundFX.play()
        self.ButtonS.setLabels(["Pause","Autonomous"])
        self.matchSection = StartMatchScreen.AUTO
        self.matchState = StartMatchScreen.AUTO
        self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
        self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)
        self.ButtonS.callback = self.stopMatch
        # Make North Button Dissapear
        self.ButtonN.setLabels("")
        self.ButtonN.callBack = self.none
        self.ButtonN.bgcolor = (0,0,0)

    def _enter(self):
        print(self.clock.time)
        # Resetup all variable use to run match
        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartAuto.wav'))
        self.matchState = StartMatchScreen.ENTER
        self.currentClockVal = Settings.autoTime + Settings.teleopTime 

        #setup clock
        self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
        self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)
        self.clock.setColor(YELLOW)
        self.bigScreen.clockColor(YELLOW)

        #Draw teams and stats on HDMI screen
        self.updateTeams()
        self.bigScreen.cteam("NE",self.teamR1,True,75,21)
        self.bigScreen.cteam("SE",self.teamR2,False,35,61)
        self.bigScreen.cteam("NW",self.teamB1,True,99,100)
        self.bigScreen.cteam("SW",self.teamB2,True,10,13)
        print("Updated teams: R1")
        print("\""+self.teamR1+"\"")
        # Start initilization once screen opens            

    def updateTeams(self):

        if self.match.getTeam(Match.B1) is not None:
            self.teamB1 = str(self.match.getTeam(Match.B1).getNumber())
        else:
            self.teamB1 = ""
        if self.match.getTeam(Match.R1) is not None:
            self.teamR1 = str(self.match.getTeam(Match.R1).getNumber())
        else:
            self.teamR1 = ""
        if self.match.getTeam(Match.B2) is not None:
            self.teamB2 = str(self.match.getTeam(Match.B2).getNumber())
        else:
            self.teamB2 = ""
        if self.match.getTeam(Match.R2) is not None:
            self.teamR2 = str(self.match.getTeam(Match.R2).getNumber())
        else:
            self.teamR2 = ""

        self.ButtonNW.setLabels(["Stop",self.teamB1])
        self.ButtonNE.setLabels(["Stop",self.teamR1])
        self.ButtonSW.setLabels(["Stop",self.teamB2])
        self.ButtonSE.setLabels(["Stop",self.teamR2])

    def _process(self):

        self.updateTeams()

        # If the end of initilization has been reached
#        if self.matchState == StartMatchScreen.INITsT:
           
        # Start Autonomous
        if self.matchState == StartMatchScreen.AUTO:
            self.clock.run()
            self.bigScreen.clockRun()
            self.clock.update()
            if self.clock.time == Settings.teleopTime:
                self.clock.setColor(GREEN)
                self.bigScreen.clockColor(GREEN)
            if not self.bigStopped and self.clock.time == Settings.teleopTime:
                self.currentClockVal = self.clock.time
                self.bigScreen.clockStop()
                self.bigScreen.clockSet(self.clock.time) # make sure in sync
                self.clock.stop()
#                self.bigStopped = True
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndAuto.wav'))
                self.soundFX.play()
                self.matchState = StartMatchScreen.AUTOsT

        # If Autonomous has run and ended
        if self.matchState == StartMatchScreen.AUTOsT:
            self.ButtonS.callback = self.startTeleop
            self.ButtonS.setLabels(["Start","Teleop"])
            self.ButtonN.setLabels(["End","Match"])
            self.ButtonN.callBack = self.endMatch
            self.ButtonN.bgcolor = (255,255,255)

        # Start TELEOP
        if self.matchState == StartMatchScreen.TELEOP:
#            print(self.clock.time)
            self.clock.run()
            self.bigScreen.clockRun()
#            print(self.clock.time)
            self.clock.update()
            if self.clock.time == Settings.endGameTime:
                self.clock.setColor(RED)
                self.bigScreen.clockColor(RED)
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartEndGame.wav'))
                self.soundFX.play()
            if not self.bigStopped and self.clock.time == 0:
                self.bigScreen.clockSet(self.clock.time) # make sure in sync
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndTeleop.wav'))
                self.soundFX.play()
                self.matchState = StartMatchScreen.TELEOPsT

        # If Match Has Ended
        if self.matchState == StartMatchScreen.TELEOPsT:
            self.ButtonN.setLabels(["Match","Over"])
            self.ButtonN.callback = self.none
            self.ButtonN.bgcolor = (255,255,255)
            self.ButtonS.setLabels(["End","Game"])
            self.ButtonS.callback = self.endMatch

        # Stop State
        if self.matchState == StartMatchScreen.STOP:
            self.currentClockVal = self.clock.time
            self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
            self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)        
            
        return True                          # tells screen that a redraw is necessary
        
