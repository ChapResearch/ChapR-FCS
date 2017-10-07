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
from gatt import GATT
import datetime

#
# NOTE - this class should only be used in a NON-SIMULATED environment.  If you are
#        simulating, load the right BLEinterfaceSimluation.py.
#

class BLEinterface(object):

    Mode2Timeout = datetime.timedelta(seconds=5)

    def __init__(self):
        self.rn4020 = RN4020()            # powers up the rn4020 and initializes it
        if not self.rn4020.setup():
            print("ERROR: problem initializing rn4020")
        self.mode = None                  # the mode governs how the BLE operates
        self.mode2Rotation = 0            # determines who transmits stats in mode 2
        self.lastConnect = {}
        self.lastConnect["R1"] = None;
        self.lastConnect["R2"] = None;
        self.lastConnect["B1"] = None;
        self.lastConnect["B2"] = None;


    def simpleBLETest(self):
        self.rn4020._cmd("WP")
        self.rn4020._cmd("Y")
        self.rn4020._cmd("A")

    #
    # enterMode() - enter the given mode which should be from 0 to 4 (TBD).  Each mode
    #               has a particular behavior and supports other calls during the mode.
    #               Note that BLEinterface code may call this too, for reseting the message
    #               when something interesting happens (like asking for a different xmit in mode 2)
    #
    def enterMode(self,mode,fieldName,match=None,R1=None,R2=None,B1=None,B2=None):
        if match:
            match = int(match)

        print("setting mode " + ("%d" % mode))
        print("flushing...");
        self.rn4020.flush()

        self.mode = mode
        if mode == 0:
            message = BLEprotocol.mode0Message(fieldName,match)
            self.rn4020.broadcastMessage(message)
        elif mode == 1:
            message = BLEprotocol.mode1Message(fieldName,match)
#            self.rn4020.pingPongMacro(500,1000,message)
            self.rn4020.pingPongMacro(2000,2000,message)
        elif mode == 2:
            # first clear out stale data in our record of last robot connection
            for key in self.lastConnect:
                self.lastConnect[key] = datetime.datetime.now()
            # compose an appropriate message and kick-off the ping-ponging
            # NOTE that the ping-ponging message will rotate through each robot
            message = BLEprotocol.mode2Message(fieldName,match,R1,R2,B1,B2,self.mode2Rotation)
            self.rn4020.pingPongMacro(500,1000,message)


    #
    # getIncomingTeam() - returns a(nother) incoming team.  Returns None if there aren't
    #                     any incoming teams.  Notes:
    #                       - return is a number representing a team (as opposed to a string)
    #                       - will return one team at most
    #                       - should only be called during mode 1, undefined results otherwise
    #                       - needs to be called repeatedly and quickly (like during screen process), or
    #                         data could be lost of the input buffer overflows
    #                       - blocks while reading serial port, but returns upon team, or lack of any serial data
    #
    def getIncomingTeam(self):
        line = self.rn4020._asyncReadline()
        if line:
            isWrite = self.rn4020.checkWriteLine(line)    # return is a tuple of [ handle, data(hex) ] or None
            if isWrite:
                print("write")

                handle = isWrite[0]
                data = isWrite[1]

                record = GATT.lookup(handle)
                if record:
                    # we got a record, correct write?
                    if record["name"] == 'Robot#':
                        # OK! we have a good number (in hex) - so decode and return the data, which is supposed
                        #   to be an integer, so condition it as such
                        # team = data.decode('hex')
                        team = data[:-1].decode('hex')     # there is a trailing period for some reason currently
                        return int(team)
                    else:
                        print("write to wrong attribute")
                        return None
                else:
                    print("bad handle lookup")
                    return None

        return None

    #
    # getRobotStats() - returns stats for the latest robot that reported on its stats.  Much like the
    #                   routine above, the following notes apply:
    #                       - returns a tuple (<"R1"|"R2"|"B1"|"B2">,<connected>,<bat1>,<bat2>) where 0 <= bat1,bat2  <= 1
    #                           <connected> will be TRUE or FALSE, FALSE happens if a robot doesn't report in as it should
    #                           Assuming that the caller is calling this in a loop, it should just be able to respond to
    #                           tuples without worry about any particular robot (not) reporting.
    #                       - should only be called during mode 2, undefined results otherwise
    #                       - needs to be called repeatedly and quickly (like during screen process)
    #                       - blocks while reading serial port, but returns upon report, or lack of any serial data
    #
    def getRobotStats(self):
        # this routine needs to notice if it has been too long since any particular
        # robot has transmitted, and move on to the next robot, and eventually
        # signalling loss of robot signal
        # it needs to increment the mode2Rotation when moving to the next robot

        line = self.rn4020._asyncReadline()
        if line:
            isWrite = self.rn4020.checkWriteLine(line)    # return is a tuple of [ handle, data(hex) ] or None
            if isWrite:
                print("write")
                handle = isWrite[0]
                data = isWrite[1]

                record = GATT.lookup(handle)

                if record:
                    print("write " + record["name"])

                    # we got a record, so figure out which robot reported, ignore other writes
                    # note that we just do an integer decode, which includes 2 bytes - robot battery, phone battery
                    if record["name"] == 'R1 Rep':
                        key = "R1"
                    elif record["name"] == 'R2 Rep':
                        key = "R2"
                    elif record["name"] == 'B1 Rep':
                        key = "B1"
                    elif record["name"] == 'B2 Rep':
                        key = "B2"
                    else:
                        print("mode 2 write with bad handle")
                        return None

                    batteries = data[:-1].decode('hex')     # there is a trailing period for some reason currently
                    self.lastConnect[key] = datetime.datetime.now()
                    self.mode2rotation = (self.mode2rotation + 1) % 4
                    # TODO - need to reprogram ping-pong
                    return([key,True,(batteries&0xff00)>>8,batteries&0x00ff])

                else:
                    print("bad handle lookup")
                    return None
            pass

        # TODO - need a time-out to rotate - which will reprogram ping-pong
        for key in self.lastConnect:
            if (self.lastConnect[key] + BLEinterface.Mode2Timeout) < datetime.datetime.now():
                return([key,False,0,0])

        return None

