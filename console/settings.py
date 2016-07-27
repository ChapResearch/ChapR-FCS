#
#
# Settings - An object that is used to save default settings and easily load them 
#          -
#

import ConfigParser
import os

class Settings(object):                   
    
    fileName = "consoleSettings.ini"   #this the nameof the file, it is not a setting

    # THe follow settings are written to the config file, and the values here are the defaults if there is not cfg file
    fieldName = "Alpha"                
    autoTime = 30
    teleopTime = 120
    endGameTime = 30
    audio = True            #determines where audio will e played from HDMI or audio jack
    remoteControl = True

    # The following settings are not written to the config file, and the value set here is the default when the program starts
    matchNumber = 1

    @classmethod
    def saveSettings(cls):
        file = open(Settings.fileName,'w')
        settings = Settings.createConfigFile()
        settings.write(file)
        file.close()

    @classmethod
    def loadSettings(cls):
        if not os.path.isfile(Settings.fileName):
            Settings.saveSettings()
        Settings.readConfigFile(Settings.fileName)

    @classmethod
    def readConfigFile(cls,file):
        cfgfile = ConfigParser.ConfigParser()
        cfgfile.read(file)

        Settings.autoTime = cfgfile.getint("Times","Auto")
        Settings.teleopTime = cfgfile.getint("Times","Teleop")
        Settings.endGameTime = cfgfile.getint("Times","Endgame")

        Settings.fieldName = cfgfile.get("Match Options","Field Name")
        Settings.matchNumber = cfgfile.getint("Match Options","Match Number")
        Settings.remoteControl = cfgfile.getboolean("Match Options","Remote Control")

        Settings.audio = cfgfile.getboolean("HDMI and Audio","Audio Path")

    @classmethod
    def createConfigFile(cls):
        cfgfile = ConfigParser.RawConfigParser()

        cfgfile.add_section("Times")
        cfgfile.set("Times","Auto",Settings.autoTime)
        cfgfile.set("Times","Teleop",Settings.teleopTime)
        cfgfile.set("Times","Endgame",Settings.endGameTime)

        cfgfile.add_section("Match Options")
        cfgfile.set("Match Options","Field Name",Settings.fieldName)
        cfgfile.set("Match Options","Match Number",Settings.matchNumber)
        cfgfile.set("Match Options","Remote Control",Settings.remoteControl)

        cfgfile.add_section("HDMI and Audio")
        cfgfile.set("HDMI and Audio","Audio Path",Settings.audio)
        
        return cfgfile
