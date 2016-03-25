#
# bootscreens.py
#
#    Display the boot screens on both the small and large screens.
#    Note that this isn't a "normal" screen like the others.
#   

import pygame
import time

class BootScreens():

    def __init__(self,smallScreen,bigScreen):
        self.smallScreen = smallScreen
        self.bigScreen = bigScreen

    def ChapResearchLogo(self):
        self.bigScreen.showImage("Media/logo_name_website.gif","expandX",1)
        self.smallScreen.showImage("Media/logo_name_website.gif","expandX",1)

    def Team2468Logo(self):
        #self.bigScreen.showImage("Media/2468Logo.gif","expandY",1)
        #self.smallScreen.showImage("Media/2468Logo.gif","expandY",1)
        self.bigScreen.showImage("Media/2468 Logo 2.gif","expandY",1)
        self.smallScreen.showImage("Media/2468 Logo 2.gif","expandY",1)

    def FIRSTLogo(self):
        self.bigScreen.showImage("Media/FTCicon_RGB.gif","expandY",1)
        self.smallScreen.showImage("Media/FTCicon_RGB.gif","expandY",1)

    def seperator(self):
        self.bigScreen.fill(255,255,255,.25)
        self.smallScreen.fill(255,255,255,.25)

    def delay(self):
        time.sleep(1)


    def process(self):
        self.seperator()
        self.ChapResearchLogo()
        self.delay()
        self.seperator()
        self.Team2468Logo()
        self.delay()
        self.seperator()
        self.FIRSTLogo()
        self.delay()
        self.seperator()
