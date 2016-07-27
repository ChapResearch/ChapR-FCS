#
#
# Calls to give you connection images for displaying hdmi screen
#
#

import pygame

class ConnectionImage(object):
    
    con0 = None
    con1 = None

    @classmethod
    def init(cls):
        red = pygame.image.load("Media/RedDot.png").convert_alpha()
        blue =  pygame.image.load("Media/BlueDot.png").convert_alpha()
        ConnectionImage.con0 = pygame.Surface((64,64))
        ConnectionImage.con1 = pygame.Surface((64,64))
        ConnectionImage.con0.blit(red,(0,0),pygame.Rect((0,0),(64,64)))
        ConnectionImage.con1.blit(blue,(0,0),pygame.Rect((0,0),(64,64)))

    @classmethod
    def get(cls,ping):
        if ping:
            return ConnectionImage.con1
        else:
            return ConnectionImage.con0

