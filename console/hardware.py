#
# hardware.py
#
#   Definitions for the hardware of the console.  Most things
#   refer to the pins of the GPIO of the RPi.  But there are
#   a few other things too.
#

import os
import datetime
import pygame

if not(os.getenv("DISPLAY")):
    import RPi.GPIO as GPIO

class HARDWARE(object):

    BUTTONDOWN = pygame.USEREVENT
    BUTTONUP = pygame.USEREVENT + 1
    BUTTONHOLD = pygame.USEREVENT + 2

# wake and mldp are no longer used - they are hardwired to high and low
# respectively.  they are kept here for reference purposes.
# The RN4020 uses the serial port too.  Numbers below refer to the GPIO
# pin that is used.

    class rn4020:
        wake = 0
        mldp = 0
        connected = 3
        tty = "/dev/ttyAMA0"
        baud = 115200

    class button:
        NW = 17
        SW = 18
        NE = 23
        SE = 22
        S = 27

    class buttonTracker:
        debounce = datetime.timedelta(0,0,100000)    # debounce is in microseconds
        hold = datetime.timedelta(0,1,0)        # if held for 1 seconds, then we issue "hold" event

        def __init__(self,button):
            self.button = button
            self.value = bool(1)                     # with button pull-ups, the initial state is high
            self.held = False                        # true if button has been held down
            self.lastTime = datetime.datetime.now()

        #
        # check() - given a button, check to see if it has changed.  If it has
        #           changed, this routine will return TRUE and the button's value
        #           will indicate the new value.  Note that the caller doesn't
        #           have to worry about bounce.  This routine deals with that and
        #           will only return TRUE after applying debounce.  
        #
        def check(self):
            if os.getenv("DISPLAY"):            # if in simulation, buttons never return True
                return False

            currentValue = bool(GPIO.input(self.button))
            now = datetime.datetime.now()

            if currentValue != self.value:         # we have a change here - but need to check for bounce
                if ((now - self.lastTime) > HARDWARE.buttonTracker.debounce):
                    self.held = False
                    self.value = currentValue
                    self.lastTime = now
                    return True
            else:
                # again, a bit weird because a down button is zero
                if not(self.value) and not(self.held) and ((now - self.lastTime) > HARDWARE.buttonTracker.hold):
                    self.held = True
                    return True

            return False

    #
    # checkButtons() - checks the GPIOs to see if a button was pressed.  This must be
    #               called through each loop in a screen.  This COULD be written to
    #               be threaded, but this was easy enough - so we can stay away from
    #               bringing threads into the mix (always worried about RPi problems).
    #               Events are generated for each button press/release
    #
    @classmethod
    def checkButtons(cls):
        for button in (cls.NW,cls.SW,cls.NE,cls.SE,cls.S):
            if button.check():
                # note that because of the way the buttons are wired, high and low
                # are reversed, so they are set right here:
                if button.value:
                    pygame.event.post(pygame.event.Event(cls.BUTTONUP,{'button':button.button}))
                else:
                    if button.held:
                        pygame.event.post(pygame.event.Event(cls.BUTTONHOLD,{'button':button.button}))
                    else:
                        pygame.event.post(pygame.event.Event(cls.BUTTONDOWN,{'button':button.button}))

    if not os.getenv("DISPLAY"):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(button.NW,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button.SW,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button.NE,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button.SE,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(button.S,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    # the class has the buttons statically in it for ease of use.

    NW = buttonTracker(button.NW)
    SW = buttonTracker(button.SW)
    NE = buttonTracker(button.NE)
    SE = buttonTracker(button.SE)
    S = buttonTracker(button.S)

    @classmethod
    def cleanup(cls):
        print "hardware cleanup"
        if not os.getenv("DISPLAY"):
            GPIO.cleanup()
