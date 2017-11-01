#
#
# statsdisplay.py - 
#
#      Displays all robot stats on HDMI screen
#
#

import pygame
from batteryimage import BatteryImage
from connectionimage import ConnectionImage
from joystickImage import JoystickImage
import math
import random

class StatsDisplay(object):

    @classmethod
    def init(cls):
        BatteryImage.init()
        ConnectionImage.init()
        JoystickImage.init()
        StatsDisplay.teamFontSize = 60
        StatsDisplay.teamFont = pygame.font.SysFont('arial', StatsDisplay.teamFontSize, bold=True)
        
    @classmethod
    def display(cls,screen,screenSize,position,number,ping,rBat,pBat,stats,joystick):
        (width,height) = StatsDisplay.teamFont.size(number)
        if stats:
            if position == "NW":
                pos = (20,10)
                screen.blit(BatteryImage.get(rBat),(95,80))
                screen.blit(BatteryImage.get(pBat),(95,110))
                screen.blit(ConnectionImage.get(ping),(20,75))
                screen.blit(JoystickImage.get(joystick),(200,75))
                temp = StatsDisplay.teamFont.render(number,1,(0,0,255))
            elif position == "NE":
                pos = (screenSize[0]-width-20,10)
                screen.blit(BatteryImage.get(rBat),(screenSize[0]-155,80))
                screen.blit(BatteryImage.get(pBat),(screenSize[0]-155,110))
                screen.blit(ConnectionImage.get(ping),(screenSize[0]-80,75))
                temp = StatsDisplay.teamFont.render(number,1,(255,0,0))
            elif position == "SW":
                screen.blit(BatteryImage.get(rBat),(95,screenSize[1]-140))
                screen.blit(BatteryImage.get(pBat),(95,screenSize[1]-110))
                screen.blit(ConnectionImage.get(ping),(20,screenSize[1]-145))            
                pos = (20, screenSize[1]-height-10)
                temp = StatsDisplay.teamFont.render(number,1,(0,0,255))
            elif position == "SE":
                pos = (screenSize[0]-width-20, screenSize[1]-height-20)
                screen.blit(BatteryImage.get(rBat),(screenSize[0]-155,screenSize[1]-140))
                screen.blit(BatteryImage.get(pBat),(screenSize[0]-155,screenSize[1]-110))
                screen.blit(ConnectionImage.get(ping),(screenSize[0]-80,screenSize[1]-145))
                temp = StatsDisplay.teamFont.render(number,1,(255,0,0))
            else:
                pos = (screenSize[0]-width,screenSize[1]-height)
        else:
            if position == "NW":
                pos = (20,10)
                temp = StatsDisplay.teamFont.render(number,1,(0,0,255))
            elif position == "NE":
                pos = (screenSize[0]-width-20,10)
                temp = StatsDisplay.teamFont.render(number,1,(255,0,0))
            elif position == "SW":
                pos = (20, screenSize[1]-height-10)
                temp = StatsDisplay.teamFont.render(number,1,(0,0,255))
            elif position == "SE":
                pos = (screenSize[0]-width-20, screenSize[1]-height-20)
                temp = StatsDisplay.teamFont.render(number,1,(255,0,0))
            else:
                pos = (screenSize[0]-width,screenSize[1]-height)
            
        screen.blit(temp,pos)

#
# updateRobotStats -- for now is a place holderm however adding the paremeter
#                     (b1,b2,r1,r2) will then be used to make actual imputs recieved from the
#                     bluetooth object
#

def updateRobotStats():
        robotStats = [False,0,0,False,0,0,False,0,0,False,0,0]

#        if b1 is not Null:
        robotStats[0] = True
        robotStats[1] = randint(0,100)
        robotStats[2] = randint(0,100)

#        if b2 is not Null:
        robotStats[3] = True
        robotStats[4] = randint(0,100)
        robotStats[5] = randint(0,100)

#        if r1 is not Null:
        robotStats[6] = True
        robotStats[7] = randint(0,100)
        robotStats[8] = randint(0,100)

#        if r2 is not Null:
        robotStats[9] = True
        robotStats[10] = randint(0,100)
        robotStats[11] = randint(0,100)
