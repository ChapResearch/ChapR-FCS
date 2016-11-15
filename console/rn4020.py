#
# rn4020.py
#
#   Interface to the rn4020.  Does all the bluetoothy stuff.
#

from hardware import HARDWARE
import serial
import datetime
import os
import re
from gatt import GATT
import RPi.GPIO as GPIO

class RN4020:
    """Implements intereface to RN4020"""

    #
    # __init__() - creates a serial object for the port and opens
    #              it.
    #
    def __init__(self):

        # note that this thing doesn't keep the serial port parameters
        # in instance variables because they're already in the serial
        # class as ser.baudrate, ser.port, ser.timeout, etc.
        self.ser = serial.Serial(HARDWARE.rn4020.tty,HARDWARE.rn4020.baud,timeout=1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #GPIO.setup(HARDWARE.rn4020.mldp,GPIO.OUT)        # CMD/MLDP drive low
        #GPIO.setup(HARDWARE.rn4020.wake,GPIO.OUT)         # WAKE_SW drive high
        GPIO.setup(HARDWARE.rn4020.connected,GPIO.IN)         # goes high when connected
        #GPIO.output(HARDWARE.rn4020.mldp,GPIO.LOW)
        #GPIO.output(HARDWARE.rn4020.wake,GPIO.HIGH)

    def sync(self):
        # (re)syncronizes with the rn4020
        pass

    def flush(self):
        t = self.ser.timeout
        self.ser.timeout = .1
        self.ser.readlines()
        self.ser.timeout = t

    def dump(self):
        t = self.ser.timeout
        self.ser.timeout = .1
        print(self.ser.readlines())
        self.ser.timeout = t

    def reboot(self):
        self.flush()
        self._cmd("R,1")
        return(self._waitline("Reboot",1) and self._waitline("CMD",2))

    #
    # _cmd() - execute the given command, and consume the return message
    #          that comes from the command if any.  That's the tricky part
    #          some commands have return, some don't.
    #
    def _cmd(self,name):
        self.ser.write(name + "\n")

    def _cmdV(self,name):
        self._cmd(name)
        return(self._waitline("AOK",10,"ERR"))

    def _cmdB(self,name):
        self._cmd(name)
        return(self._bufferlines("END",5,"ERR"))

    #
    # _mapHandles() - maps the long UUIDs to handles so that appropriate async
    #                 mapping can be done when setting values.  This can only be
    #                 called AFTER the services have been defined.  Returns TRUE
    #                 if it worked, False otherwise.
    #
    def _mapHandles(self):
        print("here mapping handles")
        services = self._cmdB('LS')
        for entry in GATT.PrivateChars:
            uuid = entry["uuid"].translate(None,"-")
            match = re.search("(?i)" + uuid + ",(....),",services)
            if match:
                entry["handle"] = match.group(1)
            else:
                print("no match")

        print(GATT.PrivateChars)
        return(True)


    #
    # _setDeviceChar() - sets the device characteristics that will be
    #                reported to the incoming device.
    #                Note that there is a max of 20 characters for each.
    #                we assume that it works (no return monitoring), but
    #                the confirmation does build up.  Note that the 
    #                serial number characteristic is NOT set, we leave
    #                that as the MAC address of the model.  Note that a
    #                reboot has to happen to make it stick.
    #
    def _setDeviceChar(self,
                       name=None,
                       manufName=None,
                       model=None,
                       versionFW=None,
                       versionHW=None,
                       versionSW=None):
        if name and not self._cmdV('SN,' + name[0:20]):
            print("ERROR: can't set console name")
            return(False)

        if manufName and not self._cmdV('SDN,' + manufName[0:20]):
            print("ERROR: can't set manufacturer name")
            return(False)

        if model and not self._cmdV("SDM," + model[0:20]):
            print("ERROR: can't set model name")
            return(False)

        if versionFW and not self._cmdV("SDF," + versionFW[0:20]):
            print("ERROR: can't set firmware version")
            return(False)

        if versionFW and not self._cmdV("SDH," + versionHW[0:20]):
            print("ERROR: can't set hardware version")
            return(False)

        if versionFW and not self._cmdV("SDR," + versionSW[0:20]):
            print("ERROR: can't set software version")
            return(False)

        return(True)
    
    def _setFactory(self):
        self._cmd("WP")               # stop any running program first
        if self._cmdV("SF,2\n"):
            if self.reboot():
                return(True)
            else:
                print("ERROR: could not reboot after factory clear")
        else:
            print("ERROR: could not reset to factory")

    #
    # checkWriteLine() - checks to see if the given line is a GATT write from the RN4020
    #                    and returns a tuple of (ID,value) if so.  ID is 4 digits hex,
    #                    and value is hex digits.
    #
    def checkWriteLine(self,line):
        pieces = line.split(",")
        if len(pieces) == 3:
            if pieces[0] == "WV":
                return([pieces[1],pieces[2]])
        return None

    #
    # _asyncReadline() - reads a line from the serial port, but only if there IS
    #                    some data in the serial port.  If there is any data, it
    #                    will potentially stall for the timeout given.  Otherwise,
    #                    it will either return with a line immediately, or come
    #                    back with "None".  The return data is stripped.
    #
    def _asyncReadline(self):
        incoming = ""
        first = True
        while self.ser.inWaiting() > 0 or not first:
            first = False
            c = self.ser.read(1)             # may timeout if delayed char after first char read
            incoming += c
            if len(c) == 0 or c == "\n":
                break
        incoming = incoming.strip()
        if len(incoming) == 0:
            return None
        else:
            return incoming

    #
    # _waitline() - waits for a line consisting entirely of
    #               the argument.  Note that trailing "\r" and "\n"
    #               are removed.  This is a long wait, longer than
    #               the normal timeout, so the wait time must be
    #               specified.  If the badTrigger is specified,
    #               then it will match an cause immediate False
    #               return.
    #               NOTE that timeout can be 

    def _waitline(self,trigger,timeout,badTrigger=None):
        target = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while(datetime.datetime.now() < target):
            incoming = self.ser.readline().strip()
            if(incoming == trigger):
                return(True)
            if(badTrigger and incoming == badTrigger):
                return(False)
        return(False)
        
    #
    # _bufferlines() - buffers all of the data on lines leading up
    #                  a line with "trigger" at the end.  The buffer
    #                  is returned if things go OK, otherwise None
    #                  is returned.  The "trigger" is not included in
    #                  the buffer.
    #
    def _bufferlines(self,trigger,timeout,badTrigger=None):
        target = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        buffer = ""
        while(datetime.datetime.now() < target):
            incoming = self.ser.readline().strip()
            if(incoming == trigger):
                return(buffer)
            if(badTrigger and incoming == badTrigger):
                return(None)
            buffer += incoming + "\n"
        return(None)

    #
    # _setServices() - sets the services that this application supports.  Note,
    #                  however, that only the predefined services are defined for
    #                  this command.  So we really can only set "private service":
    #                      0x80000000 - device information
    #                      0x00200000 - time (experimental)
    #                      0x00000001 - private service
    #
    def _setServices(self):
        if self._cmdV("SS,80200001"):
            return(True)
        else:
            print("ERROR: setting services")
            return(False)

    #
    # _setPrivateServices() - sets the private services that this application supports.
    #                         It also sets the private service UUID that peripherals
    #                         will use to identify this application.  Note that the UUID
    #                         needs to be in smushed-hex form with just 32 hex digits
    #                         as a string.  NOTE that the %02x is necessary, the RN4020
    #                         gets angry if there aren't 2 digits.
    #
    def _setPrivateServices(self):
        print("here setting private services")
        # first clear existing private services, then set our UUID
        if(self._cmdV("PZ") and self._cmdV("PS," + GATT.ServiceUUID.translate(None,"-"))):
            for entry in GATT.PrivateChars:
                cmd = "PC," + entry["uuid"].translate(None,"-") + ",%02x,%02x" % (entry["type"],entry["size"])
                if(not(self._cmdV(cmd))):
                    print("ERROR: setting individual characteristics")
                    return(False)
            return(True)
        print("ERROR: setting up for characteristics")
        return(False)

    #
    # _setFeatures() - sets the standard features for this application.
    #                  They are static (don't really change).  The features
    #                  set are (this is more intersting in the features it turns OFF):
    #                         0x00100000      - no bonding
    #                  In the future, we may enable authentication and maybe scripts.
    #
    def _setFeatures(self):
        return(self._cmdV("SR,00100000"))

    def setup(self):
        return(self._setFactory() and
               self._setDeviceChar("Chap FCS","Chap Research","Chap FCS") and
               self._setServices() and
               self._setFeatures() and
               self._setPrivateServices() and
               self._mapHandles() and
               self.reboot())

    #
    # stopScript() - stops current program
    #
    def stopScript(self):
        self._cmd("WP")

    #
    # broadcastMessage() - a simple broadcast of a particular message.
    #
    def broadcastMessage(self,bcastMessage):
        print("going to broadcast \"" + bcastMessage + "\"")
        self._cmd("WP")                   # stop any running script
        self._cmd("Y")                    # need to stop any previous message/connection
        self._cmdV("N," + bcastMessage)
        self._cmdV("A")

    #
    # _pingPongBcast() - sub-routine for the pingPongMacro() call - sets up b-cast message
    #
    def _pingPongBcast(self,bcastTime,bcastMessage):
        self._cmd("N," + bcastMessage)                    # prepare b-cast message
        self._cmd("SM,1," + ("%08x" % (bcastTime*1000)))  # b-cast time
        self._cmd("A")                                    # start broadcast

    #
    # _pingPongConnect() - sub-routine for the pingPongMacro() call - sets up connectable
    #
    def _pingPongConnect(self,connectableTime):
        self._cmd("SM,2," + ("%08x" % (connectableTime*1000))) # connectable time
        self._cmd("A")                                         # start avertising

    #
    # pingPongMacro() - sets up an RN4020 script to ping pong between broadcast and connectable
    #                   advertisement, then starts the script.  Times in ms
    #
    def pingPongMacro(self,bcastTime,connectableTime,bcastMessage):
        self._cmd("WP")                   # stop any running script
        self._cmdV("Y")                   # stop any advertisement
        self._cmd("SR,00102000")          # turn OFF UART, no bonding, server only
        self._cmdV("WC")                  # clear current script
        self._cmdV("WW")                  # start entering the script
        self._cmd("@PW_ON")               # called by WR by default (or by wr)
        self._pingPongBcast(bcastTime,bcastMessage)

        # when timer 1 goes off, terminate b-cast and start connectable advertisement

        self._cmd("@TMR1")
        self._cmd("Y")                                         # turn off previous b-cast
        self._pingPongConnect(connectableTime)

        # when timer 2 goes off, terminate the connectable advertisement and start broadcast again

        self._cmd("@TMR2")
        self._cmd("Y")                                    # turn off previous b-cast
        self._pingPongBcast(bcastTime,bcastMessage)

        # when a connection comes in, set up for incoming data

        self._cmd("@CONN")
        self._cmd("SM,2,FFFFFFFF")                        # turn off connection timer immediately
        self._cmd("SM,1,FFFFFFFF")                        # turn off connection timer immediately
        self._cmd("SR,00103000")                          # turn ON UART output for write data

        # after a client disconnects, get the timer going again, list like @TMR2 and @PW_ON

        self._cmd("@DISCON")
        self._cmd("SR,00102000")                          # turn OFF UART, no bonding, server only
        self._pingPongBcast(bcastTime,bcastMessage)

        self._cmdB("\033")                                # escape terminates program

        self._cmd("WR")                                   # starts it up - note that "WR,0" starts w/debugging
