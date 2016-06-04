

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

    def __init__(self,name,match,bigScreen):
        Screen.__init__(self,name)

        self.screen.fill([0,0,0])

        self.match = match

        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartAuto.wav'))

        self.clock = HDMIClock(self.screen,BLACK)
        self.bigScreen = bigScreen
        self.bigStopped = False
        self.bigScreen.fill(0,0,0)
#        self.BSWidth = self.get_width()
 #       self.BSHeight = self.get_height()
  #      pygame.draw.rect(self.bigScreen,(0,0,255),(0,0,self.BS/3,self.BSHeight/9),0)

        self.initialize = True
        self.initializeStopped = False
        self.autoRunning = False
        self.autoStopped = False
        self.teleopStart = False
        self.teleopStopped = False
        self.endGame = False
        self.matchEnd = False
        self.matchSection = "Initialize"
        self.currentClockVal = 150

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
        self.currentClockVal = self.clock.time
        self.clock.stop()
        self.bigScreen.clockStop()
        self.autoRunning = False
        self.teleopRunning = False
        if self.matchSection == "Autonomous":
            self.ButtonS.callback = self.startAutonomous
        elif self.matchSection == "Teleop":
            self.ButtonS.callback = self.startTeleop

    def startTeleop(self):
        self.autoStopped = False
        self.teleopStart = True
        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartTeleop.wav'))
        self.soundFX.play()
        self.ButtonS.setLabels(["Stop","Teleop"])
        self.matchSection = "Teleop"
        self.ButtonS.callback = self.stopMatch()

    def startAutonomous(self):
        self.initializeStopped = False
        self.autoRunning = True
        self.soundFX.play()
        self.ButtonS.setLabels(["Stop","Autonomous"])
        self.matchSection = "Autonomous"
#        self.ButtonS.callback = self.stopMatch()

    def _enter(self):
        self.clock.setTime(2,30)
        self.bigScreen.clockSet(2,30)

    def _process(self):
        # Start initilization once screen opens
        if self.initialize:
            print("Initializing")
            # Initializes robots
            self.initializeStopped = True
            self.initialize = False
            
        # If the end of initilization has been reached
        if self.initializeStopped:
            self.ButtonS.callback = self.startAutonomous
            self.ButtonS.setLabels(["Start","Autonomous"])
           
        # Start Autonomous
        if self.autoRunning:
            self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
            self.bigScreen.clockSet(self.currentClockVal)
            self.clock.run()
            self.bigScreen.clockRun()
            self.clock.update()
            if self.clock.time == 119:
                self.clock.setColor(BLUE)
                self.bigScreen.clockColor(BLUE)
            if not self.bigStopped and self.clock.time == 120:
                self.bigScreen.clockStop()
                self.bigScreen.clockSet(self.clock.time) # make sure in sync
                self.clock.stop()
                self.bigStopped = True
                self.autoStopped = True
                self.autoRunning = False
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndAuto.wav'))
                self.soundFX.play()

        # If Autonomous has run and ended
        if self.autoStopped:
            self.ButtonS.callback = self.startTeleop
            self.ButtonS.setLabels(["Start","Teleop"])

        # Start TELEOP
        if self.teleopStart:
            self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
            self.bigScreen.cloclSet(self.currentClockVal)
            self.clock.run()
            self.bigScreen.clockRun()
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
        return True                          # tells screen that a redraw is necessary

