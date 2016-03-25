#
# HDMIdriver.py
#
#   Contains all of the code to run the HDMI display.
#   The activities of the HDMI display are driven from
#   the given file descriptor, which is assumed to be
#   connected to the parent who is feeding this child
#   sequences of commands.
#
#   The following commands are used:
#     INIT  - initialize
#     END   - end
#     SI    - show image:  filename, (x,y), fade
#     CLS   - clear screen
#     FILL  - fill screen
#     CSET   - set the clock args: mins,secs
#     CCOLOR - set the clock color: r,g,b
#     CRUN   - start the clock counting down
#     CSTOP  - stop the count
#
#
# OLD OLD OLD BELOW THIS
#     TEAM:[NW,NE,SW,SE]:<teamstring>
#     BATTERY:[NW,NE,SW,SE]:<batterylevel>
#     STATUS:[NW,NE,SW,SE]:<status>
#     MATCH:<match>
#     PREROLL:[ON,OFF]   (note, this may just roll picture from a directory)
#     BLANK
#     PAUSE
#     LOGO:<logofile>    (this puts up a particular picture)
#     SOUND:<sound>      (plays a sound)
#     COLOR:<color>      (digits of clock in this color immediately)
#
#   Given these commands, the HDMI clock does all of the timing itself.
#   It runs sounds and everything according to SOP, sounds and digits move
#   appropriately.
#
#   Waiting for these values is done through events.  An event comes in saying
#   (essentially) start the clock, or change status, etc.

#
# The main class is HDMI - but it ends-up splitting up the functions for sender and
# receiver for control of the HDMI display.
#

import pygame
import os
import select
from time import sleep
import utils
from multiprocessing import Queue
from signal import alarm, signal, SIGALRM
from globalVariables import RED,GREEN,BLUE,YELLOW,BLACK,WHITE
from fractions import gcd
from HDMIclock import HDMIClock


class HDMI:

    def __init__(self,role,hdmiComm,framebuffer="/dev/fb0"):
        self.role = role
        self.comm = hdmiComm
        self.framebuffer = framebuffer

        if self.role == "client":
            print("going init on HDMI...")
            self._initHDMI()
            print("done")
            self.clock = HDMIClock(pygame.display.get_surface(),BLACK)
            print("done with HDMI clock as well")

            # just go into listen/dispatch loop

            #print("enter listen loop")
            while 1:
                self.clientListen()
                self.clock.update()
                pygame.display.update()

    #
    # _initHDMI() - initializes the HDMI display from the framebuffer
    #               Note that the framebuffer device is passed in to the
    #               this routine and has no default.  We have a good
    #               guess on the RPi as to what this will be, but don't
    #               know on other devices. 
    #               (/dev/fb0 is HDMI screen on the RPi)
    #               We go straight after the fbcon on RPi.  The others
    #               could be directfb or svgalib.
    #
    def _initHDMI(self):
        if not os.getenv("DISPLAY"):
            print("going real hdmi...")
            os.putenv("SDL_FBDEV", self.framebuffer)     # should switch these to os.environ
            os.putenv('SDL_VIDEODRIVER', "fbcon")
            alarm(1)                   # gets us out of the VT_WAITACTIVE bug
        else:
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500,0)

        try:
            pygame.display.init()
            pygame.init()

        except pygame.error:
            print("failed on opening frame buffer")
            return False                      # couldn't init HDMI         

        if os.getenv("DISPLAY"):
            self.screenSize = (800,600)
            self.screen = pygame.display.set_mode(self.screenSize,pygame.DOUBLEBUF)
            pygame.display.set_caption("HDMI Simulation")
        else:
            mymodes = pygame.display.list_modes()
            for mode in mymodes:
                print(mode)
                g = gcd(mode[0],mode[1])
                print((mode[0]/g,mode[1]/g))
            self.screenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            #self.screenSize = (800,600)
            print "Framebuffer size: %d x %d" % (self.screenSize[0], self.screenSize[1])
            print("going for screen")
            self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
            alarm(0)
            #self.screen = pygame.display.get_surface()
            print("good")

        print("ready to fill")
        self.screen.fill((128,128,128))
        print("ready to font init")
        pygame.font.init()
        print("ready to set invisible mouse")
        pygame.mouse.set_visible(0)
        print("updating")
        pygame.display.update()

    #
    # end() - the command that tells this HDMI client to shut down - it doesn't
    #         do anything important, just clears the screen.  The dispatcher
    #         special-cases "end"
    #
    def end(self):
        if self.role == "server":
            self._command("END")
        else:
            self.cls()              # the caller needs to notice the END and end things
            pygame.quit()
            exit()

    def fill(self,r,g,b,fade=0):
        if self.role == "server":
            self._command("FILL",r,g,b,fade)
        else:
            fill = self.screen.copy()
            fill.fill((int(r), int(g), int(b)))
            utils._showImage(fill,(0,0),1,float(fade))
            #self._showImage(fill,(0,0),1,float(fade))
            #self.screen.fill((int(r), int(g), int(b)))
            #pygame.display.update()

    def cls(self):
        if self.role == "server":
            self._command("CLS")
        else:
            self.screen.fill((255, 255, 255))
            pygame.display.update()

    def showImage(self,image,position,fade=0):
        if self.role == "server":
            self._command("SI",image,position,fade)
        else:
            utils.showImage(image,position,fade)

    #
    # clockSet(mins,secs) - routines to control the clock
    # clockColor(r,g,b)
    # clockRun()
    # clockStop()
    #

    def clockSet(self,mins,secs=None):
        if self.role == "server":
            self._command("CSET",mins,secs)
        else:
            if secs is None:
                print("clockSet() called with secs as None")
            self.clock.setTime(mins,secs)

    def clockColor(self,color):
        if self.role == "server":
            self._command("CCOLOR",color)
        else:
            self.clock.setColor(color)

    def clockRun(self):
        if self.role == "server":
            self._command("CRUN")
        else:
            self.clock.run()

    def clockStop(self):
        if self.role == "server":
            self._command("CSTOP")
        else:
            self.clock.stop()

    def init(self):
        if self.role == "server":
            self._command("INIT")
        else:
            self._initHDMI(framebuffer)   # initialize the display
            self.cls()

    def _command(self,*args):
        self.comm.put(args)            # includes the command

    def _dispatch(self,cmd,args):
        #print("dispatching " + cmd)
        for c in HDMI.commandTable:
            if cmd == c[0]:
                c[1](self,*args)
                return
        print("BAD COMMAND")
        
    #
    # clientListen() - listens for incoming requests and dispatches them
    #                  Should only be called by the client.
    #                  Commands have a command, followed by a tab, followed
    #                  by tab-separated arguments.
    #
    def clientListen(self):
        if not self.comm.empty():
            args = self.comm.get()
            cmd = args[0]
            args = args[1:]
            self._dispatch(cmd,args)
            return(cmd)

    commandTable = (
        ( "INIT", init ),
        ( "END", end ),
        ( "SI" , showImage ),
        ( "CLS", cls),
        ( "FILL", fill),
        ( "CSET", clockSet),
        ( "CCOLOR", clockColor),
        ( "CRUN", clockRun),
        ( "CSTOP", clockStop),
    )

