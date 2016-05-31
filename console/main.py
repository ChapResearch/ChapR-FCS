#
# main.py
#
#   Main program for the ChapR FCS.  It contains the main loop for, really,
#   anything happening in the system.  Note that the main loop runs flat out.
#   That is, there are no delays or timings involved.  It is assumed that
#   this is the only useful program running on the RPi and it can take all
#   of the resources it needs.  This is done so that anything coming in from
#   the RN4020 is noticed immediately.  Each sub-system, therefore, must
#   implement its own timing.
#
#   NOTE that unlike many python programs, this one doesn't have a main(),
#   it just starts running from the top.  Made it easier to read IMHO.
#

"""
The main program for ChapR FCS.  It sets up the display and all of the views,
firing up any threads that are necessary, too.

Note that this program forks a copy that will drive the HDMI display, while
the parent will drive the console.
"""

import pygame
import os
import sys
import time
from random import randint
import select
from HDMIdriver import HDMI
# from clock import Clock
from touchDriver import touchScreen
from screen import Screen
import multiprocessing as mp
from signal import alarm, signal, SIGALRM
import globalVariables
from globalVariables import RED,GREEN,BLUE,YELLOW
from hardware import HARDWARE
from Team import Match
from rn4020 import RN4020

#
#  ____   _                    _         _    _               
# / ___| (_) _ __ ___   _   _ | |  __ _ | |_ (_)  ___   _ __  
# \___ \ | || '_ ` _ \ | | | || | / _` || __|| | / _ \ | '_ \ 
#  ___) || || | | | | || |_| || || (_| || |_ | || (_) || | | |
# |____/ |_||_| |_| |_| \__,_||_| \__,_| \__||_| \___/ |_| |_|
#                                                             
# This code can all run in "simulated mode" for debugging and development
# purposes.  When in simulation mode you must be running in a windowed
# environment.  A small and large window will open up simulating the
# LCD and HDMI of the RPi.  Simluation mode will start automatically
# if the X-windows "DISPLAY" environmental variable is set.

#
#  ____                
# | __ )  _   _   __ _              ________  ___  ____
# |  _ \ | | | | / _` |             /        \  \ \/ /
# | |_) || |_| || (_| |            |          |_/   /
# |____/  \__,_| \__, |             \______________/
#                |___/ 
# __        __            _                                                _ 
# \ \      / /___   _ __ | | __        __ _  _ __  ___   _   _  _ __    __| |
#  \ \ /\ / // _ \ | '__|| |/ /_____  / _` || '__|/ _ \ | | | || '_ \  / _` |
#   \ V  V /| (_) || |   |   <|_____|| (_| || |  | (_) || |_| || | | || (_| |
#    \_/\_/  \___/ |_|   |_|\_\       \__,_||_|   \___/  \__,_||_| |_| \__,_|
#                                                                            
# OK, so there is a bug in the pre 2.0 version of the SDL library (SDL provides
# pygame with the graphical interface to the framebuffers).  The bug is that an
# SDL ioctl() call to the framebuffer gets stuck in VT_WAITACTIVE
# (fb_events.c:170) and can't get out.  This happens on the RPi, mostly due it
# appears to the interfaces to the framebuffers in the kernel.  The only way
# out of it is to interrupt the ioctl() - so that's what we do.  We set a very
# short alarm() right before init'ing pygame, which will go off when the SDL
# library is stuck, and get it out.  The signal, though, doesn't do anything
# itself.  Just calls a blank function.
		
def nothing():
        pass

signal(SIGALRM,nothing)

#  _   _  ____   __  __  ___ 
# | | | ||  _ \ |  \/  ||_ _|
# | |_| || | | || |\/| | | | 
# |  _  || |_| || |  | | | | 
# |_| |_||____/ |_|  |_||___|
#  ____                                
# / ___|   ___  _ __  ___   ___  _ __  
# \___ \  / __|| '__|/ _ \ / _ \| '_ \ 
#  ___) || (__ | |  |  __/|  __/| | | |
# |____/  \___||_|   \___| \___||_| |_|
#                                      
# The SDL library (hence pygame) doesn't support two screens at the same time.
# So we deal with that by creating a sub-process to run the "bigScreen" (the
# HDMI screen).  This is a bit confusing in this code.  All of the HDMI screen
# calls refer to the main pygame display - while at the same time the little
# screen calls refer to the main pygame display TOO.  Confused?  Just remember
# that the HDMI calls are running in a different process where the main pygame
# screen refers to the HDMI screen.
#
# The child process, below, is the HDMI screen process.  The HDMI class implements
# a communication pipe from the main process to the child process.  That pipe
# is set-up below.

hdmiComm = mp.Queue()
hdmiProcess = mp.Process(target=HDMI, args=("client",hdmiComm,"/dev/fb0"))
hdmiProcess = hdmiProcess.start()

bigScreen = HDMI("server",hdmiComm)    # sets up the communication to the sub-process
smallScreen = touchScreen("/dev/fb1")  # initialize the small screen interface

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()


#  ____   _               _                 _    _     
# | __ ) | | _   _   ___ | |_  ___    ___  | |_ | |__  
# |  _ \ | || | | | / _ \| __|/ _ \  / _ \ | __|| '_ \ 
# | |_) || || |_| ||  __/| |_| (_) || (_) || |_ | | | |
# |____/ |_| \__,_| \___| \__|\___/  \___/  \__||_| |_|
#                                                      
# Set up the bluetooth control.  The RN4020 is the hardward at the lowest
# level.  However, we use a special BLE object to maintain everything from
# bluetooth control, to the threads that monitor the protocol as the match
# is progressing.
# 

#bluetooth = BLEcontrol()

# set-up hardware, and run through the boot-up test sequence.  Each
# time we boot, the system tests the buttons and bluetooth (as much as
# possible anyway)

# TODO TODO TODO TODO
# TODO TODO TODO TODO
# TODO TODO TODO TODO
# TODO TODO TODO TODO

#  __  __         _          _                         
# |  \/  |  __ _ (_) _ __   | |     ___    ___   _ __  
# | |\/| | / _` || || '_ \  | |    / _ \  / _ \ | '_ \ 
# | |  | || (_| || || | | | | |___| (_) || (_) || |_) |
# |_|  |_| \__,_||_||_| |_| |_____|\___/  \___/ | .__/ 
#                                               |_|    

from bootscreens import BootScreens
from startupscreen import StartupScreen
from optionscreen import OptionScreen
from matchsetupscreen import MatchSetupScreen
from numberchangescreen import NumberChangeScreen
from teamassign import TeamAssignScreen
from buttontest import ButtonTestScreen
from mainscreen import MainScreen
from matchoptionsscreen import MatchOptionsScreen
from systemoptionsscreen import SystemOptionsScreen
from runmatchscreen import RunMatchScreen
from About import AboutScreen
from systemtests import SystemTestsScreen
from robotasignmentscreen import RobotAssignmentScreen
from matchsetup import PrepareMatchScreen
from startmatch import StartMatchScreen

# each one of these calls instantiates an object that ends-up on the
# superclass "Screen" array of screens.  Screen switching is handled
# by finding a specific screen in this array.  The names of the screens
# are hard-coded within all of the screens as they link from one to
# another.
#
# Current list of screens and names:
#
#     ButtonTestScreen() - "ButtonTestScreen"
#     OptionScreen() - "option"
#     MatchSetupScreen() - "

# All of the match info is stored in match object
MatchObject = Match()

MatchSetupScreen("MatchSetupScreen")
NumberChangeScreen("autoTimeChangeScreen","autoTime",0,"Autonomous:",YELLOW)
NumberChangeScreen("teleopTimeChangeScreen","teleopTime",0,"Teleop:",GREEN)
NumberChangeScreen("endGameTimeChangeScreen","endGameTime",0,"End Game:",RED)
NumberChangeScreen("matchNumberChangeScreen","matchNumber",1,"Match:",BLUE)
MatchOptionsScreen("MatchOptions")
SystemOptionsScreen("SystemOptions")
RunMatchScreen("RunMatch",bigScreen)
AboutScreen("AboutScreen")#.process()
SystemTestsScreen("SystemTest")
RobotAssignmentScreen("RobotAssignmentScreen",MatchObject).process()
PrepareMatchScreen("PrepareMatch",MatchObject).process()
#BootScreens(smallScreen,bigScreen).process()
#ButtonTestScreen("ButtonTestScreen").process()
#OptionScreen("OptionScreen").process()
StartMatchScreen("StartMatch",MatchObject,bigScreen).process()

while(True):
        MainScreen("MainScreen").process()

#
# END ROUTINES - these should always be called upon end
#
bigScreen.end()
#hdmiProcess.join()        # wait for the child to exit
pygame.quit()
HARDWARE.cleanup()
exit()
