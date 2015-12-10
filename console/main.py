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


# from rn4020 import RN4020

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
# | __ )  _   _   __ _ 
# |  _ \ | | | | / _` |
# | |_) || |_| || (_| |
# |____/  \__,_| \__, |
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

#  ____   _                _                 
# / ___| | |_  __ _  _ __ | |_  _   _  _ __  
# \___ \ | __|/ _` || '__|| __|| | | || '_ \ 
#  ___) || |_| (_| || |   | |_ | |_| || |_) |
# |____/  \__|\__,_||_|    \__| \__,_|| .__/ 
#                                     |_|    
# 
# We don't work immediately with the HDMI, but it nice NOT to have to crash
# into the set-up of the touch screen.  The child waits for a signal from
# the parent before it initializes the HDMI screen.
#


#mp.set_start_method('spawn')
hdmiComm = mp.Queue()
hdmiProcess = mp.Process(target=HDMI, args=("client",hdmiComm,"/dev/fb0"))
hdmiProcess = hdmiProcess.start()

# at this point we have the hdmiProcess running, and waiting for comms
# anything to write to it, simply use the hdmiComm queue.  Remember
# to hdmiProcess.join() when ending.

# fire-up the connection to the big screen

bigScreen = HDMI("server",hdmiComm)

# (1) initialize the smallScreen

smallScreen = touchScreen("/dev/fb1")

# (2) display the boot screens including the Chap Research logo.

bigScreen.fill(0,0,0)
smallScreen.fill(0,0,0)

bigScreen.fill(255,255,255,.5)
smallScreen.fill(255,255,255,.5)

#bigScreen.showImage("Media/chap.gif","expand",2)

bigScreen.showImage("Media/logo_name_website.gif","expandX",1)
smallScreen.showImage("Media/logo_name_website.gif","expandX",1)

#time.sleep(3)

bigScreen.fill(255,255,255,.25)
smallScreen.fill(255,255,255,.25)

bigScreen.showImage("Media/FTCicon_RGB.gif","expandY",1)
smallScreen.showImage("Media/FTCicon_RGB.gif","expandY",1)

#time.sleep(2)

bigScreen.fill(255,255,255,.25)
smallScreen.fill(255,255,255,.25)

# (3) set-up hardware, and run through the boot-up test sequence.  Each
# time we boot, the system tests the buttons and bluetooth (as much as
# possible anyway)

# (4) set-up the operational state machine, where the screens are organized
# by the current state.  In each state, the appropriate screen is called to
# process whatever event is being received (button press, connection, etc.)
# Some states require other protocols being processed such as BTE connections.

# (5) upon a reboot selection, start the whole process over.

#  __  __         _          _                         
# |  \/  |  __ _ (_) _ __   | |     ___    ___   _ __  
# | |\/| | / _` || || '_ \  | |    / _ \  / _ \ | '_ \ 
# | |  | || (_| || || | | | | |___| (_) || (_) || |_) |
# |_|  |_| \__,_||_||_| |_| |_____|\___/  \___/ | .__/ 
#                                               |_|    

from startupscreen import StartupScreen
from optionscreen import OptionScreen
from matchsetupscreen import MatchSetupScreen
from numberchangescreen import NumberChangeScreen
from teamassign import TeamAssignScreen
from buttontest import ButtonTestScreen

# each one of these calls instantiates an object that ends-up on the
# superclass "Screen" array of screens.  Screen switching is handled
# by finding a specific screen in this array.

MatchSetupScreen()
NumberChangeScreen("autoTimeChangeScreen","autoTime",0,"Autonomous:",YELLOW)
NumberChangeScreen("teleopTimeChangeScreen","teleopTime",0,"Teleop:",GREEN)
NumberChangeScreen("endGameTimeChangeScreen","endGameTime",0,"End Game:",RED)
NumberChangeScreen("matchNumberChangeScreen","matchNumber",1,"Match:",BLUE)

OptionScreen()
#StartupScreen().process()
print("boop")
ButtonTestScreen().process()
OptionScreen().process()

bigScreen.end()
pygame.quit()
exit()
