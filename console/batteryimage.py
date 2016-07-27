#
#
# Calls to give you battery images for displaying hdmi screen
#
#

import pygame

class BatteryImage(object):
    
    bat1 = None
    bat2 = None
    bat3 = None
    bat4 = None
    bat5 = None

    @classmethod
    def init(cls):
        allBattery = pygame.image.load("Media/battery-icons-60x125.png").convert()
        BatteryImage.bat1 = pygame.Surface((60,25))
        BatteryImage.bat2 = pygame.Surface((60,25))
        BatteryImage.bat3 = pygame.Surface((60,25))
        BatteryImage.bat4 = pygame.Surface((60,25))
        BatteryImage.bat5 = pygame.Surface((60,25))

        BatteryImage.bat1.blit(allBattery,(0,0),pygame.Rect((0,0),(60,25)))
        BatteryImage.bat2.blit(allBattery,(0,0),pygame.Rect((0,25),(60,25)))
        BatteryImage.bat3.blit(allBattery,(0,0),pygame.Rect((0,50),(60,25)))
        BatteryImage.bat4.blit(allBattery,(0,0),pygame.Rect((0,75),(60,25)))
        BatteryImage.bat5.blit(allBattery,(0,0),pygame.Rect((0,100),(60,25)))
    
    @classmethod
    def get(cls,num):
        if num >= 81:
            return BatteryImage.bat5
        elif num >= 61:
            return BatteryImage.bat4
        elif num >= 41:
            return BatteryImage.bat3
        elif num >= 21:
            return BatteryImage.bat2
        elif num >= 5:
            return BatteryImage.bat1
        elif num <= 4:
            return BatteryImage.bat1            
