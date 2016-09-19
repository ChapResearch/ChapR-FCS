#
# BLEinterfaceSimulation.py
#
#   PRETENDS to be an Interface to some BLE device.  This allows useful simulation for
#   the non-console-based testing program.  See BLEinterfaceRN4020.py for a real interface.
#

import random

class BLEinterface(object):

    def __init__(self):

        self.mode = None                  # the mode governs how the BLE operates
        self.R1 = None
        self.R2 = None
        self.B1 = None
        self.B2 = None

    #
    # enterMode() - enter the given mode which should be from 0 to 4 (TBD).  Each mode
    #               has a particular behavior and supports other calls during the mode.
    #
    def enterMode(self,mode,fieldName,match,R1=None,R2=None,B1=None,B2=None):
        self.mode = mode
        self.R1 = R1
        self.R2 = R2
        self.B1 = B1
        self.B2 = B2

    #
    # getIncomingTeam() - returns a(nother) incoming team.  Returns None if there aren't
    #                     any incoming teams.  Notes:
    #                       - return is a number representing a team (as opposed to a string)
    #                       - will return one team at most
    #                       - should only be called during mode 0, undefined results otherwise
    #                       - needs to be called repeatedly and quickly (like during screen process)
    #                       - blocks while reading serial port, but returns upon team, or lack of any serial data
    #
    def getIncomingTeam(self):
        if self.mode != 0:
            if self.mode is None:
#                print("WARNING! Trying to get incoming team before mode called")
                pass
            else:
#                print("WARNING! Trying to get incoming team in mode " + self.mode)
                pass

        if random.randint(1,100000) == 1:
            team = random.randint(100,15000)
            print("returning team " + ("%d" % team))
            return(team)

        return None

    #
    # getRobotStats() - returns stats for the latest robot that reported on its stats.  Much like the
    #                   routine above, the following notes apply:
    #                       - returns a tuple (<"R1"|"R2"|"B1"|"B2">,<bat1>,<bat2>) where 0 <= bat1,bat2  <= 1
    #                       - should only be called during mode 1, undefined results otherwise
    #                       - needs to be called repeatedly and quickly (like during screen process)
    #                       - blocks while reading serial port, but returns upon report, or lack of any serial data
    #
    def getRobotStats(self):
        # given the current teams set in the mode, generate stats for it
        return ("R1",.5,.5)
