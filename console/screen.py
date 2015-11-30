#
# screen.py
#
#   This is the base class for doing any screen for the ChapR-FCS.
#   It includes the basic things such as buttons (touch and physical).
#

import pygame
from buttons import Button

class Screen():

    # the screenList is maintained by the class, so when a screen needs to
    # be switched, it can happen easily.

    # a screen is a surface of the same size as the current pygame display
    # it is initialized the one time

    screenList = []

    def __init__(self,name):
        self.name = name
        self.screen = pygame.display.get_surface().copy()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        Screen.screenList.append(self)
        self.buttons = Button.clone(name)    # these are the buttons for THIS screen

    #
    # findscreen() - CLASS METHOD - this routine will return the screen that
    #                is referenced by the given name.  It is assumed that the
    #                process() method of that screen is about to be called...
    #                though it doesn't have to be.
    #
    @classmethod
    def findScreen(cls,name):
        for screen in Screen.screenList:
            if screen.name == name:
                return screen
        return None

    #
    # update() - updates the current screen to the pygame display.  Generally this
    #            is not overriden by child classes.
    #
    def update(self):
        self.buttons.update(self.screen)             # needed for flashing buttons
        self.buttons.draw(self.screen)
        pygame.display.get_surface().blit(self.screen,(0,0))
        pygame.display.update()

    #
    # _process() - just in case the subclass doesn't do a _process()
    #
    def _process(self):
        pass

    #
    # _enter() - this is called whenever a screen is entered initially.  Setup stuff
    #            will happen here.  Though this is a dummy in case the subclass doesn't
    #            need an _enter().
    #
    def _enter(self):
        pass

    #
    # process() - process a screen of stuff.  This is really the eventloop() for a
    #             screen.  Each individual screen can have their own _process() to 
    #             do any specific processing for that screen.
    #
    def process(self):
        self._enter()                             # the start-up code for entering a screen
        while True:
            self._process()                       # call the process for the subclass screen
            self.update()                         # then do the update of the buttons, screen, etc.

            nextScreen = self.processEvents()     # process my events
            if nextScreen:
                if nextScreen == "back":          # request to go back up to parent
                    return None
                elif nextScreen == "quit":        # request to quit
                    return nextScreen
                else:                             # otherwise, decend to next screen
                    nextScreen = Screen.findScreen(nextScreen)
                    if not nextScreen:
                        print("ERROR: screen " + nextScreen + " not found.")
                        return("quit")
                    nextScreen = nextScreen.process()          # process this new screen and quit if asked
                    if nextScreen == "quit":
                        return nextScreen


    def processEvents(self):
        event = pygame.event.wait()
            
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            nextScreen = self.buttons.processEvent(event)       # this will call my callbacks
            if nextScreen:
                return nextScreen
        return None
