

#
#
# StartMatchScreen - The screen meant to run the match timer, and if robotControl is enabled it will start and stop the robots.
#
#

import pygame
from screen import Screen
from buttons import Button
from tables import Table
from consoleClock import consoleClock
from globalVariables import RED,GREEN,BLUE,YELLOW,BLACK,WHITE
from Team import Match
import os
from statsdisplay import StatsDisplay
from settings import Settings
from matchsetup import PrepareMatchScreen

class StartMatchScreen(Screen):

#
# in the table below, the individual STOP buttons for the robots aren't yet taken into account
#

#   STATE           Upon Entry                           EVENTS           Next State   COMMENTS
# ----------------- ---------------------------------    --------------   -----------  --------------
# ENTER_STATE       reset all variables
#                   sets clock to match start value
#                   paints buttons to match state
#                                                        South Button     INIT_STATE   Robots have been placed, and ready to start match
#                                                        North Button     (back)       Completely get out of this screen
# INIT_AUTO_STATE   sends "autoinit" cmd to bots
#                   paints buttons to match state
#                                                        South Button     AUTO_STATE
#                                                        North Button     (back)       Completely get out of this screen
# AUTO_STATE        sends "autostart" cmd to bots
#                   play sound
#                   start clock (and set timeout)
#                   paints buttons to match state
#                                                        South Button     AUTO_PAUSE
#                                                        Clock Timeout    AUTO_DONE_STATE
# AUTO_PAUSE        sends "pause" cmd to all bots
#                   stop clock (and clear timoeout)
#                   paints buttons to match state
#                                                        South Button     AUTO_STATE
#                                                        North Button     (back)
# AUTO_DONE_STATE   send "stop" cmd to all bots
#                   plays beeeehhh-baahhhhh sound
#                   paints buttons to match state
#                                                        South Button     INIT_TELEOP_STATE
#                                                        North Button     (back)
# INIT_TELEOP_STATE send "teleopinit" to all bots
#                   paints buttons to match state
#                                                        South Button     TELEOP_STATE
#                                                        North Button     (back)
# TELEOP_STATE      send "teleopstart" to all bots
#                   start clock (and set timeout)
#                   plays da-da-da-DAT,-da-daaaah
#                   paints buttons to match state
#                                                        South Button     TELEOP_PAUSE
#                                                        Clock Timeout    END_GAME_STATE
# TELEOP_PAUSE      sends "pause" cmd to all bots
#                   stop clock (and clear timeout)
#                   paints buttons to match state
#                                                        South Button     TELEOP_STATE
#                                                        Norht Button     (back)
# END_GAME_STATE    sends "we're in end game my dudes"
#                   plays the hwaaaaaaaaaaaa sound
#                   paints clock (green i think)
#                                                        South Button     END_GAME_PAUSE
#
# END_GAME_PAUSE    send "pause" cmd to all bots
#                   stop clock (clear timeout)
#                   paints screen to match state
#                                                        South Button     END_GAME_STATE
#                                                        North Button     (back)
#                 
# MATCH_END         send "stop" cmd to bots
#                   stops clock
#                   paints buttons for state
#                                                        South Button     (back)
#

    ENTER_STATE       = 0 
    INIT_AUTO_STATE   = 1
    AUTO_STATE        = 2
    AUTO_PAUSE        = 3 
    AUTO_DONE_STATE   = 4
    INIT_TELEOP_STATE = 5
    TELEOP_STATE      = 6
    TELEOP_PAUSE      = 7
    END_GAME_STATE    = 8
    END_GAME_PAUSE    = 9
    MATCH_END         = 10

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

        self.clock = consoleClock(self.screen,BLACK)
        self.bigScreen = bigScreen
        self.bigStopped = False
        self.bigScreen.fill(0,0,0)
        self.stopped = False
        self.timeoutReached = False
        
        self.dataTable = self.tables(fontsize=48,font="arial",align="center",cellWidth=self.screen.get_width(),color=(255,255,0),bgcolor=(0,0,0))
        self.dataTable.addData("herro", name="state")
        self.dataTable.endRow()
        self.dataTable.position = (0,self.screen.get_height()/5*3)

        self.ButtonNW = self.buttons(bgcolor = (0,0,255), rock = "NW",fontsize = 20,
                                     **Button.standardButton("NW",["Stop",""],self.screen))
        self.ButtonNE = self.buttons(bgcolor = (255,0,0), rock = "NE",fontsize = 20,
                                     **Button.standardButton("NE",["Stop",""],self.screen))
        self.ButtonSW = self.buttons(bgcolor = (0,0,255), rock = "SW",fontsize = 20,
                                     **Button.standardButton("SW",["Stop",""],self.screen))
        self.ButtonSE = self.buttons(bgcolor = (255,0,0), rock = "SE",fontsize = 20,
                                     **Button.standardButton("SE",["Stop",""],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.changeState, rock=self.INIT_AUTO_STATE, lcolor = (0,0,0),
                                     **Button.standardButton("S",["Initialize"],self.screen))
        self.ButtonN = self.buttons(bgcolor = (0,0,0), callback=self.endMatch, lcolor = (0,0,0),
                                     **Button.standardButton("N","Yep",self.screen))

        print("startmatc init")

    def done(self):
        PrepareMatchScreen.match.clear()
        return "back"

    def none(self):
        pass

    def endMatch(self):
        self.ButtonNW.setLabels("")
        self.ButtonSW.setLabels("")
        self.ButtonNE.setLabels("")
        self.ButtonSE.setLabels("")
        self.match.clear()
        return "MainScreen"
    
    #Redraws the team numbers and stats on HDMI screen
    #-The stats variable determines whether stats are drawn
    def redrawStats(self,stats=True):
        self.bigScreen.fill(0,0,0)
        self.bigScreen.cteam("NW","148",4,95,88,stats)
        self.bigScreen.cteam("NE","2468",1,35,56,stats)
        self.bigScreen.cteam("SW","5628",3,100,100,stats)
        self.bigScreen.cteam("SE","10241",3,10,13,stats)        


    def initialize(self):
        self.matchState = StartMatchScreen.INIT
        print("Initialized")
        self.matchState - StartMatchScreen.INITsT
        self.changeHUD("Initialized")
        self.ButtonS.callback = self.startAutonomous
        self.ButtonS.setLabels(["Start","Autonomous"])
        
    def _enter(self):
        print(self.clock.time)
        # Resetup all variable use to run match
        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartAuto.wav'))
        self.matchState = StartMatchScreen.ENTER
        self.currentClockVal = Settings.autoTime + Settings.teleopTime  + Settings.endGameTime
        self.timeout = -1

        #setup clock
        self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
        self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)
        self.clock.stop()
        self.bigScreen.clockStop()
        self.clock.setColor(YELLOW)
        self.bigScreen.clockColor(YELLOW)
        self.autoTimeout = self.currentClockVal - Settings.autoTime
        self.teleopTimeout = self.currentClockVal - Settings.autoTime - Settings.teleopTime

        #Setup Buttons
        self.ButtonS.setLabels("Initialize")
        self.ButtonS.bgcolor = (255,255,255)
        self.ButtonN.setLabels("Yep")
        self.ButtonN.bgcolor = (0,0,0)
        self.ButtonSE.setLabels(["Stop",""])
        self.ButtonSW.setLabels(["Stop",""])
        self.ButtonNE.setLabels(["Stop",""])
        self.ButtonNW.setLabels(["Stop",""])
        self.updateTeams()

        #Draw teams and stats on HDMI screen
        self.updateTeams()
        self.bigScreen.cteam("NE",self.teamR1,True,75,21)
        self.bigScreen.cteam("SE",self.teamR2,False,35,61)
        self.bigScreen.cteam("NW",self.teamB1,True,99,100)
        self.bigScreen.cteam("SW",self.teamB2,True,10,13)
        print("Updated teams: R1")
        print("\""+self.teamR1+"\"")
        self.changeHUD("Match Ready")
        # Start initilization once screen opens            

#
#   changeState()--- Calls all necesary methods to change state, update hud, 
#                    play sounds, and talk to bots.
#
    def changeState(self,state):
        print(state)
        self.repaintScreen(state)
        self.playSound(state)
        self.clockUpdate(state)
        self.talkToRobots(state)

#
#   repaintScreen(state) --- Normlly called by changeState(),
#                       changes all necesary hub, and button attributes
#                       depending on the state that it is passed
#
    def repaintScreen(self,state):
        if state==self.INIT_AUTO_STATE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock = self.AUTO_STATE
            self.changeHUD("Initialized")
            self.ButtonS.setLabels(["Start","Autonomous"])
            return 

        elif state==self.AUTO_STATE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.AUTO_PAUSE
            self.ButtonS.setLabels(["Pause","Autonomous"])
            self.changeHUD("Autonomous")
            # Make North Button Dissapear
            self.ButtonN.setLabels("")
            self.ButtonN.callBack = self.none
            self.ButtonN.bgcolor = (0,0,0)
            return

        elif state==self.AUTO_PAUSE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.AUTO_STATE
            self.ButtonS.setLabels(["Continue","Autonomous"])
            self.changeHUD("Match Paused")
            # Make North Button Appear
            self.ButtonN.setLabels(["End","Match"])
            self.ButtonN.callBack = self.endMatch()
            self.ButtonN.bgcolor = (255,255,255)
            return

        elif state==self.AUTO_DONE_STATE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.INIT_TELEOP_STATE
            self.changeHUD("Teleop Ready")
            self.ButtonS.setLabels(["Initilize","Teleop"])
            self.ButtonN.setLabels(["End","Match"])
            self.ButtonN.callBack = self.endMatch()
            self.ButtonN.bgcolor = (255,255,255)
            return

        elif state==self.INIT_TELEOP_STATE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.TELEOP_STATE
            self.ButtonS.setLabels(["Start"," Teleop"])
            return

        elif state==self.TELEOP_STATE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.TELEOP_PAUSE
            self.ButtonS.setLabels(["Pause","Teleop"])
            self.changeHUD("Teleop")
            # Make North Button Dissapear
            self.ButtonN.setLabels("")
            self.ButtonN.callBack = self.none()
            self.ButtonN.bgcolor = (0,0,0)
            return 

        elif state==self.TELEOP_PAUSE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.TELEOP_STATE
            self.ButtonS.setLabels(["Continue","Teleop"])
            self.changeHUD("Match Paused")
            # Make North Button Appear
            self.ButtonN.setLabels(["End","Match"])
            self.ButtonN.callBack = self.endMatch()
            self.ButtonN.bgcolor = (255,255,255)
            return 

        elif state==self.END_GAME_STATE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.END_GAME_PAUSE
            self.ButtonS.setLabels(["Pause","End Game"])
            self.changeHUD("End Game")
            # Make North Button Dissapear
            self.ButtonN.setLabels("")
            self.ButtonN.callBack = self.none
            self.ButtonN.bgcolor = (0,0,0)
            return 

        elif state==self.END_GAME_PAUSE:
            self.ButtonS.callback = self.changeState
            self.ButtonS.rock=self.END_GAME_STATE
            self.ButtonS.setLabels(["Continue","End Game"])
            self.changeHUD("Match Paused")
            # Make North Button Appear
            self.ButtonN.setLabels(["End","Match"])
            self.ButtonN.callBack = self.endMatch()
            self.ButtonN.bgcolor = (255,255,255)
            return

        elif state==self.MATCH_END:
            self.ButtonS.callback = self.done
            self.clock.stop()
            self.bigScreen.clockStop()
            self.changeHUD("Match Has Ended")
            self.ButtonS.setLabels("End Match")
            # Make North Button Appear
            self.ButtonN.setLabels(["End","Match"])
            self.ButtonN.callBack = self.endMatch()
            self.ButtonN.bgcolor = (0,0,0)
            return

#
#   playSound(state) --- normally called by changeState()
#                        plays repective sound for the state that is being changed to
#
    def playSound(self,state):
        if state==self.AUTO_STATE:
            self.soundFX.play()            
            return

        elif state==self.AUTO_PAUSE:
            self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndAuto.wav'))
            self.soundFX.play()                        
            return

        elif state==self.AUTO_DONE_STATE:
            self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndAuto.wav'))
            self.soundFX.play()            
            return

        elif state==self.TELEOP_STATE:
            self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartTeleop.wav'))
            self.soundFX.play()
            return 

        elif state==self.TELEOP_PAUSE:
            self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndTeleop.wav'))
            self.soundFX.play()
            return

        elif state==self.END_GAME_STATE:
            self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartEndGame.wav'))
            self.soundFX.play()
            return 

        elif state==self.END_GAME_PAUSE:
            self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndTeleop.wav'))
            self.soundFX.play()                        
            return

        elif state==self.MATCH_END:
            self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndTeleop.wav'))
            self.soundFX.play()
            return        

#
#   talkToBots(state) --- normally called by changeState()
#                         communicated with robots to tell them what to do
#                         at any given state
#
    def talkToRobots(self,state):
        if state==self.INIT_AUTO_STATE:
            return

        elif state==self.AUTO_STATE:
            return

        elif state==self.AUTO_PAUSE:
            return

        elif state==self.AUTO_DONE_STATE:
            return

        elif state==self.INIT_TELEOP_STATE:
            return

        elif state==self.TELEOP_STATE:
            return 

        elif state==self.TELEOP_PAUSE:
            return
            
        elif state==self.END_GAME_STATE:
            return 

        elif state==self.END_GAME_PAUSE:
            return

        elif state==self.MATCH_END:
            return                

#
#   clockUpdate() --- Normally called by change state,
#                     Changes the color and time for the clock, 
#                     and calls setTimeout() method
#
    def clockUpdate(self,state):
        print("inside clockUpdate()")
        if state==self.AUTO_STATE:
            self.clock.run()
            self.bigScreen.clockRun()
            self.clock.setColor(YELLOW)
            self.bigScreen.clockColor(YELLOW)
            
        elif state==self.AUTO_PAUSE:
            self.clock.stop()
            self.bigScreen.clockStop()

        elif state==self.AUTO_DONE_STATE:
            self.clock.stop()
            self.bigScreen.clockStop()

        elif state==self.TELEOP_STATE:
            self.clock.run()
            self.bigScreen.clockRun()
            self.clock.setColor(GREEN)
            self.bigScreen.clockColor(GREEN)

        elif state==self.TELEOP_PAUSE:
            self.clock.stop()
            self.bigScreen.clockStop()

        elif state==self.END_GAME_STATE:
            self.clock.run()
            self.bigScreen.clockRun()
            self.clock.setColor(RED)
            self.bigScreen.clockColor(RED)

        elif state==self.END_GAME_PAUSE:
            self.clock.stop()
            self.bigScreen.clockStop()

        elif state==self.MATCH_END:
            self.clock.stop()
            self.bigScreen.clockStop()
        
        self.setTimeout(state)


#
#   setTimeout() --- normally called by updateClock()
#                    set the timeout of the clock for each state respectivley
#
    def setTimeout(self,state):
        print("inside setTimeout()")
        if state==self.AUTO_STATE:
            print("indide first if in setTimeout()")
            self.timeout = self.currentClockVal - Settings.autoTime
            return 

        elif state==self.INIT_TELEOP_STATE:
            self.timeout = self.currentClockVal - Settings.autoTime - Settings.teleopTime
            return 

        elif state==self.END_GAME_STATE:
            self.timeout = 0
            return 
        
        self.timeoutReached = False


#
#   updateTeams() --- Updates the teams values in this screen
#
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



    def changeHUD(self,state):
        self.dataTable.setFlash("state",True);
        self.dataTable.changeData("state",data = state,cellWidth=self.screen.get_width())        

#        color = (255,255,0)
#        fontpath = pygame.font.match_font("arial",True,False)
#        workingFont = pygame.font.Font(fontpath,48)
#        width, height = workingFont.size(state)        
#        stateDisplay = workingFont.render(state,True,color)        
#        x = (self.screen.get_width()-width)/2
#        y = (self.screen.get_height()/5)*3
#        self.screen.blit(stateDisplay,(x,y))
        pass



    def _process(self):

        self.updateTeams()

        self.clock.update()

        if self.clock.time == self.timeout and not self.timeoutReached:
            print("inside if statement")
            if self.timeout == self.currentClockVal - Settings.autoTime:
                self.changeState(self.AUTO_DONE_STATE)
                self.timeoutReached = True

            elif self.timeout ==  self.currentClockVal - Settings.autoTime - Settings.teleopTime:
                self.changeState(self.END_GAME_STATE)
                self.timeoutReached = False

            elif self.timeout == 0:
                self.changeState(self.MATCH_END)
                self.timeoutReached = True
            

        # If the end of initilization has been reached
#        if self.matchState == StartMatchScreen.INITsT:
           
        # Start Autonomous
"""
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
            self.changeHUD("Teleop Ready")
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
                #self.changeHUD("End Game")
            if not self.bigStopped and self.clock.time == 0:
                self.bigScreen.clockSet(self.clock.time) # make sure in sync
                self.soundFX = pygame.mixer.Sound(os.path.join('Media','EndTeleop.wav'))
                self.soundFX.play()
                self.matchState = StartMatchScreen.TELEOPsT

        # If Match Has Ended
        if self.matchState == StartMatchScreen.TELEOPsT:
            #self.ButtonN.setLabels(["Match","Over"])
            #self.ButtonN.callback = self.none
            #self.ButtonN.bgcolor = (255,255,255)
            #self.ButtonS.setLabels(["End","Game"])
            #self.changeHUD("Match Over")
            #self.ButtonS.callback = self.endMatch
            self.stopMatch()

        # Stop State
        if self.stopped:
            self.currentClockVal = self.clock.time
            self.clock.setTime(self.currentClockVal/60,self.currentClockVal%60)
            self.bigScreen.clockSet(self.currentClockVal/60,self.currentClockVal%60)        
"""

#        return True                          # tells screen that a redraw is necessary
        
