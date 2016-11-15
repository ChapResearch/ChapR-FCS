#
# BLEinterfaceRN4020.py
#
#   Interface to the BLE RN4020.  Different implementations of BLE will have different
#   versions of this file.  Essentially, this is the "driver" the type of BLE that we
#   are talking to.  Each "driver" has its own implementation of the API that other
#   programs use to gather BLE data.  NOTE that each one of these files defines the
#   BLEinterface object, therefore, two drivers can't be loaded at the same time.
#
#   RN4020 - there is an ascii interface to this device, that is implemented in rn4020.py.
#   This file implements the higher-level calls for the BLE interface.
#
#   Note that this file should only be included if running on a device with the rn4020.
#   Load a different BLEinterface file if running in simulated mode.
#

from BLEprotocol import BLEprotocol
from rn4020 import RN4020

#
# NOTE - this class should only be used in a NON-SIMULATED environment.  If you are
#        simulating, load the right BLEinterfaceSimluation.py.
#

class BLEinterface(object):

    def __init__(self):
        self.rn4020 = RN4020()            # powers up the rn4020 and initializes it
        if not self.rn4020.setup():
            print("ERROR: problem initializing rn4020")
        self.mode = None                  # the mode governs how the BLE operates
        self.mode1Rotation = 0            # determines who transmits stats in mode 1

    def simpleBLETest(self):
        self.rn4020._cmd("WP")
        self.rn4020._cmd("Y")
        self.rn4020._cmd("A")

    #
    # enterMode() - enter the given mode which should be from 0 to 4 (TBD).  Each mode
    #               has a particular behavior and supports other calls during the mode.
    #               Note that BLEinterface code may call this too, for reseting the message
    #               when something interesting happens (like asking for a different xmit in mode 1)
    #
    def enterMode(self,mode,fieldName,match=None,R1=None,R2=None,B1=None,B2=None):
        print("setting mode " + ("%d" % mode))
        self.mode = mode
        if mode == 0:
            message = BLEprotocol.mode0Message(fieldName)
            self.rn4020.broadcastMessage(message)
        elif mode == 1:
            message = BLEprotocol.mode1Message(fieldName,match)
            self.rn4020.pingPongMacro(500,1000,message)
        elif mode == 1:
            message = BLEprotocol.mode2Message(fieldName,match,R1,R2,B1,B2,self.mode1Rotation)
            self.rn4020.pingPongMacro(500,1000,message)


    #
    # getIncomingTeam() - returns a(nother) incoming team.  Returns None if there aren't
    #                     any incoming teams.  Notes:
    #                       - return is a number representing a team (as opposed to a string)
    #                       - will return one team at most
    #                       - should only be called during mode 0, undefined results otherwise
    #                       - needs to be called repeatedly and quickly (like during screen process), or
    #                         data could be lost of the input buffer overflows
    #                       - blocks while reading serial port, but returns upon team, or lack of any serial data
    #
    def getIncomingTeam(self):
        line = self.rn4020._asyncReadline()
        if line:
            isWrite = self.rn4020.checkWriteLine(line)
            if isWrite:
                print("write")
                return isWrite
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
        # this routine needs to notice if it has been too long since any particular
        # robot has transmitted, and move on to the next robot, and eventually
        # signalling loss of robot signal
        # it needs to increment the mode1Rotation when moving to the next robot
        pass

