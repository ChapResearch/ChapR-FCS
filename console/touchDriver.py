#
# touchDriver.py
#
#   Contains the code to manage the touch screen.
#
import pygame
import os
import select
from clock import Clock
from time import sleep
import utils
from signal import alarm, signal, SIGALRM


class touchScreen:

    def __init__(self,framebuffer="/dev/fb1"):
        self.framebuffer = framebuffer
        self._initTouch()

    #
    # _initTouch() - initializes the touch display from the framebuffer
    #               Note that the framebuffer device is passed in to the
    #               this routine and has no default.  We have a good
    #               guess on the RPi as to what this will be, but don't
    #               know on other devices. 
    #               (/dev/fb0 is HDMI screen on the RPi)
    #               We go straight after the fbcon on RPi.  The others
    #               could be directfb or svgalib.
    #
    def _initTouch(self):
        if not os.getenv("DISPLAY"):
            #print("going real touch...")
            os.putenv("SDL_FBDEV", self.framebuffer)     # should switch these to os.environ
            os.putenv('SDL_VIDEODRIVER', "fbcon")
            os.putenv("SDL_MOUSEDRV","TSLIB")
            #os.putenv("SDL_MOUSEDEV","/dev/input/event0")
            os.putenv("SDL_MOUSEDEV","/dev/input/touchscreen")
            alarm(1)                   # gets us out of the VT_WAITACTIVE bug
        else:
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

        try:
            pygame.display.init()
            #pygame.init()

        except pygame.error:
            #print("failed on opening frame buffer")
            return False                      # couldn't init HDMI         

        if os.getenv("DISPLAY"):
            self.screenSize = (480,320)
            self.screen = pygame.display.set_mode(self.screenSize,pygame.DOUBLEBUF)
            pygame.display.set_caption("Touch Screen Simulation")
        else:
            self.screenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            #print "Framebuffer size: %d x %d" % (self.screenSize[0], self.screenSize[1])
            #print("going for screen")
            self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
            #self.screen = pygame.display.get_surface()
            pygame.mouse.set_visible(0)


        alarm(0)
        self.screen.fill((128,128,128))
        pygame.font.init()
        pygame.display.update()

    def showImage(self,image,position,fade=0):
            utils.showImage(image,position,fade)

    def fill(self,r,g,b,fade=0):
        fill = self.screen.copy()
        fill.fill((int(r), int(g), int(b)))
        utils._showImage(fill,(0,0),1,float(fade))
