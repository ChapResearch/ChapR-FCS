

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

class StartMatchScreen(Screen):

    #self.matchState
    INIT = 0     #    INIT - the state in which robots initialize
    INITsT = 1   #    INITsT - inbetween INIT and AUTO state
    AUTO = 2     #    AUTO - The state in which autonomous runs
    AUTOsT = 3   #    AUTOsT - inbetween state of AUTO and TELEOP
    TELEOP = 4   #    TELEOP - teleop runs
    END = 5      #    END - endgame
    TELEOPsT = 6 #    TELEOPsT - end of match state
    STOP = 7     #    STOP - pauses match

    def __init__(self,name,match,bigScreen):
        Screen.__init__(self,name)

        self.screen.fill([0,0,0])

        self.match = match

        self.clock = HDMIClock(self.screen,BLACK)
        self.bigScreen = bigScreen
        self.bigStopped = False
        self.bigScreen.fill(0,0,0)
#        self.BSWidth = self.get_width()
#        self.BSHeight = self.get_height()
#        pygame.draw.rect(self.bigScreen,(0,0,255),(0,0,self.BS/3,self.BSHeight/9),0)
  

        self.Button = self.buttons(bgcolor = (0,0,255), rock = "NW",fontsize = 25,
                                     **Button.standardButton("NW",str(match.getTeam(Match.B1).getNumber()),self.screen))
        self.Button = self.buttons(bgcolor = (255,0,0), rock = "NE",fontsize = 25,
                                     **Button.standardButton("NE",str(match.getTeam(Match.R1).getNumber()),self.screen))
        self.Button = self.buttons(bgcolor = (0,0,255), rock = "SW",fontsize = 25,
                                     **Button.standardButton("SW",str(match.getTeam(Match.B2).getNumber()),self.screen))
        self.Button = self.buttons(bgcolor = (255,0,0), rock = "SE",fontsize = 25,
                                     **Button.standardButton("SE",str(match.getTeam(Match.R2).getNumber()),self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done, lcolor = (0,0,0),
                                     **Button.standardButton("S",["Stop"],self.screen))

    def done(self):
        return "back"

    def stopMatch(self):
        self.clock.stop()
        self.bigScreen.clockStop()
        self.matchState = StartMatchScreen.STOP
        if self.matchSection == StartMatchScreen.AUTO:
            self.ButtonS.callback = self.startAutonomous
            self.ButtonS.setLabels(["Start","Autonomous"])
        elif self.matchSection == StartMatchScreen.TELEOP:
            self.ButtonS.callback = self.startTeleop
            self.ButtonS.setLabels(["Start","Teleop"])

    def startTeleop(self):
        print("StartTeleop")
        self.matchSection = StartMatchScreen.TELEOP
        self.matchState = StartMatchScreen.TELEOP
        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartTeleop.wav'))
        self.soundFX.play()
        self.ButtonS.setLabels(["Stop","Teleop"])
        self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
        self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)        
        self.ButtonS.callback = self.stopMatch

    def startAutonomous(self):
        self.soundFX.play()
        self.ButtonS.setLabels(["Stop","Autonomous"])
        self.matchSection = StartMatchScreen.AUTO
        self.matchState = StartMatchScreen.AUTO
        self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
        self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)
        self.ButtonS.callback = self.stopMatch
        print(self.clock.time)

    def _enter(self):
        print(self.clock.time)
        # Resetup all variable use to run match
        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartAuto.wav'))
        self.matchState = StartMatchScreen.INIT
        self.currentClockVal = 150

        self.clock.setTime(2,30)
        self.bigScreen.clockSet(2,30)
        # Start initilization once screen opens            
        self.matchState = StartMatchScreen.INITsT

    def _process(self):
        # If the end of initilization has been reached
        if self.matchState == StartMatchScreen.INITsT:
            self.ButtonS.callback = self.startAutonomous
            self.ButtonS.setLabels(["Start","Autonomous"])
           
        # Start Autonomous
        if self.matchState == StartMatchScreen.AUTO:
            print(self.clock.time)
            self.clock.run()
            self.bigScreen.clockRun()
            self.clock.update()
            print(self.clock.time)
            if self.clock.time == 119:
                self.clock.setColor(BLUE)
                self.bigScreen.clockColor(BLUE)
            if not self.bigStopped and self.clock.time == 120:
                self.currentClockVal = self.clock.time
                self.bigScreen.clockStop()
                self.bigScreen.clockSet(self.clock.time) # make sure in sync
                self.clock.stop()
                self.bigStopped = True
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndAuto.wav'))
                self.soundFX.play()
                self.matchState = StartMatchScreen.AUTOsT

        # If Autonomous has run and ended
        if self.matchState == StartMatchScreen.AUTOsT:
            self.ButtonS.callback = self.startTeleop
            self.ButtonS.setLabels(["Start","Teleop"])

        # Start TELEOP
        if self.matchState == StartMatchScreen.TELEOP:
#            print(self.clock.time)
            self.clock.run()
            self.bigScreen.clockRun()
#            print(self.clock.time)
            self.clock.update()
            if self.clock.time == 30:
                self.clock.setColor(GREEN)
                self.bigScreen.clockColor(GREEN)
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartEndGame.wav'))
                self.soundFX.play()
            if not self.bigStopped and self.clock.time == 0:
                self.bigScreen.clockSet(self.clock.time) # make sure in sync
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndTeleop.wav'))
                self.soundFX.play()
        
        # Stop State
        if self.matchState == StartMatchScreen.STOP:
            self.currentClockVal = self.clock.time
            self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
            self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)        
            
        return True                          # tells screen that a redraw is necessary
        
