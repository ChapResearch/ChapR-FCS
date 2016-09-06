#
# rn4020.py
#
#   Interface to the rn4020.  Does all the bluetoothy stuff.
#

#
# Here are the constants that define the UUIDs for this
# service.  But first, here's how things are going to work
# from a GATT perspective:
#
#  This "service" UUID, referred to here as UUID, will be
#  the one that the console uses to broadcast on for both
#  information and connections.  When central devices
#  connect, they will provide a server for attributes as
#  well.
#
#  The RN4020 has a built-in "Device Information Service"
#  which is part of the "profile" of the console.  Although
#  it is initially set to describe the RN4020 device itself,
#  we hijack that description to make that part of the profile
#  describe the console.

from hardware import HARDWARE
import serial
import datetime
import os

class RN4020:
    """Implements intereface to RN4020"""

    # class variables here - shared by all instances of this class

    # the service UUID was generated with www.uuidgenerator.net and is really
    # quite arbitrary.  Note that the dashes will be stripped before sending
    # to the RN4020

    UUID = "1840e436-bf53-45f1-a1dd-a56336e20377"

    # private characteristics are defined for peripherals to query
    # again, UUIDs were generated from the web site and are completely arbitrary
    # the second argument is the type, where type is:
    #
    #   INDICATE                0'b00100000    Indicate value of characteristic WITH 
    #                                            acknowledgment from server to client.
    #   NOTIFY                  0'b00010000    Notify value of characteristic WITHOUT
    #                                            acknowledgment from server to client.
    #   WRITE                   0'b00001000    Write value of characteristic WITH
    #                                            acknowledgment from client to server.
    #   WRITE WITHOUT RESPONSE  0'b00000100    Write value of characteristic WITHOUT
    #                                            acknowledgment from client to server.
    #   READ                    0'b00000010    Read value of characteristic. Value is
    #                                            sent from server to client.
    #   BROADCAST               0'b00000001    Broadcast value of characteristic.
    #
    # The third arg is the size in bytes.

    #
    # PROPERTY TYPE = 0010 0000 = indicate            (other values aren't supported
    #                 0001 0000 = notify                   by the RN4020 yet)
    #                 0000 1000 = write with ack
    #                 0000 0100 = write without ack
    #                 0000 0010 = read
    #
    # TODO: read is turned on for the attributes below, for testing.  They do NOT need
    #       to be read for distribiton. (0x08 instead of 0x0a)
    #
    #                      UUID                        PROPERTY TYPE   MAX BYTES
    #           -------------------------------------  -------------   ---------
    pchars = [ ["0d48b2e8-3312-11e6-ac61-9e71128cae77",    0x0a,         2],   # robot number (for joining)
               ["0d48b6da-3312-11e6-ac61-9e71128cae77",    0x0a,        10],   # R1 report (see above for report format)
               ["0d48b900-3312-11e6-ac61-9e71128cae77",    0x0a,        10],   # R2 report
               ["0d48ba22-3312-11e6-ac61-9e71128cae77",    0x0a,        10],   # B1 report
               ["0d48bb08-3312-11e6-ac61-9e71128cae77",    0x0a,        10]    # B2 report
             ]


    #
    # __init__() - creates a serial object for the port and opens
    #              it.
    #
    def __init__(self):

        # the rn4020 module is only viable on the actual console platform, so simulation
        # is a problem.  However, the module shouldn't break everything else during
        # simulation, so this code makes it work right duing simulation.

        self.simulation = True
        if not os.getenv("DISPLAY"):
            self.simulation = False
            import RPi.GPIO as GPIO

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
        if not self.simulation:
            t = self.ser.timeout
            self.ser.timeout = .1
            self.ser.readlines()
            self.ser.timeout = t

    def dump(self):
        if not self.simulation:
            t = self.ser.timeout
            self.ser.timeout = .1
            print(self.ser.readlines())
            self.ser.timeout = t

    def reboot(self):
        if not self.simulation:
            self.flush()
            self._cmd("R,1")
            return(self._waitline("Reboot",1) and self._waitline("CMD",2))
        else:
            return(True)

    #
    # _cmd() - execute the given command, and consume the return message
    #          that comes from the command if any.  That's the tricky part
    #          some commands have return, some don't.
    #
    def _cmd(self,name):
        if not self.simulation:
            self.ser.write(name + "\n")

    def _cmdV(self,name):
        if not self.simulation:
            self._cmd(name)
            return(self._waitline("AOK",10,"ERR"))
        else:
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
        return( (not(name) or self._cmdV('SN,' + name[0:20])) and
                (not(manufName) or self._cmdV('SDN,' + manufName[0:20])) and
                (not(model) or self._cmdV("SDM," + model[0:20])) and
                (not(versionFW) or self._cmdV("SDF," + versionFW[0:20])) and
                (not(versionHW) or self._cmdV("SDH," + versionHW[0:20])) and
                (not(versionSW) or self._cmdV("SDR," + versionSW[0:20])))

    
    def _setFactory(self):
        return(self._cmdV("SF,2\n") and self.reboot())
        
    #
    # _waitline() - waits for a line consisting entirely of
    #               the argument.  Note that trailing "\r" and "\n"
    #               are removed.  This is a long wait, longer than
    #               the normal timeout, so the wait time must be
    #               specified.  If the badTrigger is specified,
    #               then it will match an cause immediate False
    #               return.

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
    # _setServices() - sets the services that this application supports.  Note,
    #                  however, that only the predefined services are defined for
    #                  this command.  So we really can only set "private service":
    #                      0x80000000 - device information
    #                      0x00200000 - time (experimental)
    #                      0x00000001 - private service
    #
    def _setServices(self):
        return(self._cmdV("SS,80200001"))

    #
    # _setPrivateServices() - sets the private services that this application supports.
    #                         It also sets the private service UUID that peripherals
    #                         will use to identify this application.  Note that the UUID
    #                         needs to be in smushed-hex form with just 32 hex digits
    #                         as a string.  NOTE that the %02d is necessary, the RN4020
    #                         gets angry if there aren't 2 digits.
    #
    def _setPrivateServices(self):
        # first clear existing private services, then set our UUID
        if(self._cmdV("PZ") and self._cmdV("PS," + RN4020.UUID.translate(None,"-"))):
            for entry in RN4020.pchars:
                cmd = "PC," + entry[0].translate(None,"-") + ",%02d,%02d" % (entry[1],entry[2])
                if(not(self._cmdV(cmd))):
                    return(False)
            return(True)
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
        if not self.simulation:
            return(self._setFactory() and
                   self._setDeviceChar("Chap FCS","Chap Research","Chap FCS") and
                   self._setServices() and
                   self._setFeatures() and
                   self._setPrivateServices() and
                   self.reboot())
        else:
            return(True)
