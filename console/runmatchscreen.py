#
# runmatchscreen.py
#
#    This is the main screen where a match is run.  It is pretty-much
#    automatic, that is, until PAUSE is pressed.  At that point, the
#    operator can either terminate the match or continue it.
#
#    Screen shows the robots on each of the buttons, and their status
#    below the buttons.  If match is not full, a warning will appear
#    indicating that the robots aren't attached.  Unless the Remote Control
#    is off.
#
#    When Start Match is pressed, the match will begin, and each robot
#    button will be labeled "xxxxx DISABLE" if Remote Control is on.
#    Otherwise, the buttons won't be painted.
#
#

import pygame
from screen import Screen
from buttons import Button
from tables import Table
from utils import textOutline, numberDraw
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW,BLACK,WHITE
from HDMIclock import HDMIClock

class RunMatchScreen(Screen):
        
 #screen is run as a state machine
    #   State   Description
    #  ------  --------------------------
    #    0     Waiting to start the match
    #    1     Match has started autonomous
    #    2     Match is between autonomous and teleop
    #    3     Match has started teleop
    #    4     Match has started end-game
    #    5     Match is over
    #
    def __init__(self,name,bigScreen):
        Screen.__init__(self,name)
        self.clock = HDMIClock(self.screen,BLACK)
        self.state = 0
        self.bigScreen = bigScreen
        self.bigStopped = False

    def _enter(self):
        self.state = 0
        self.clock.setTime(2,30)
        self.clock.run()
        self.bigScreen.clockSet(2,30)
        self.bigScreen.clockRun()

    def _process(self):
        self.clock.update()
        if self.clock.time == 140:
            self.bigScreen.clockColor(BLUE)
        if not self.bigStopped and self.clock.time == 130:
            self.bigScreen.clockStop()
            self.bigScreen.clockSet(self.clock.time) # make sure in sync
            self.bigStopped = True
        return True                          # tells screen that a redraw is necessary

    #
    # _state0() - implements the state zero
    #
    def _state0(self):
        # clear the big screen
        pass

    #
    # stateEnter() - using the current state, prepare the screen for that
    #                state.
    #
    def stateEnter(self):

        if state == 0:              # entering the initial state, there is a big button in the middle
            self._state0()          #   used to assign teams if Remote Control is on.
        
