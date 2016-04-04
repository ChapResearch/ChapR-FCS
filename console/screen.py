#
# screen.py
#
#   This is the base class for doing any screen for the ChapR-FCS.
#   It includes the basic things such as buttons (touch and physical).
#

import pygame
from buttons import Button
from tables import Table
from hardware import HARDWARE

class Screen(object):

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
        self.tables = Table.clone(name)      # these are the tables for THIS screen
        self.title = None

    #
    # _setLogo() - puts the "standard" logo at the top of the screen - only used when
    #              there is room for it.
    #
    def _setLogo(self):
        theImage = pygame.image.load("Media/ChapFCS-title-small.gif")
        y = 10
        x = (self.width-theImage.get_width())/2
        self.screen.blit(theImage,(x,y))


    #
    # _setTitle() - sets the given title in the "normal" position.  Note, too that
    #               self.title gets set to the value.
    #
    def _setTitle(self,title,font="arial",bold=True,italic=False,size=40,color=(255,255,255),lineColor=(255,255,255),drawLines=True,lineThickness=2):
        self.title = title
        fontpath = pygame.font.match_font(font,bold,italic)
        workingFont = pygame.font.Font(fontpath,size)
        width,height = workingFont.size(title)
        positionX = (self.width - width)/2
        positionY = 60 + (80-height)/2
        titleImage = workingFont.render(title,True,color)
        self.screen.blit(titleImage,(positionX,positionY))
        if drawLines:
            pygame.draw.line(self.screen,lineColor,(positionX,positionY-3),(positionX+width,positionY-3),lineThickness)
            pygame.draw.line(self.screen,lineColor,(positionX,positionY+height+3),(positionX+width,positionY+height+3),lineThickness)
        

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
    #            is not overriden by child classes.  NOTE that screen redrawing
    #            only happens if necessary.
    #
    def update(self):
        return self.buttons.update(self.screen) or self.tables.update(self.screen)
                                                                      # needed for flashing buttons or table cells

    #
    # draw() - draws the screen - really consists mostly of buttons and tables
    #
    def draw(self):
        self.buttons.draw(self.screen)
        self.tables.draw(self.screen)
        pygame.display.get_surface().blit(self.screen,(0,0))
        pygame.display.update()

    #
    # _process() - just in case the subclass doesn't do a _process().  this is called
    #              through each screen loop as buttons are processed.
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
    # enter() - this is the screen enter routine - called whenever a screen is displayed
    #           or re-displayed.  It will call the subclass _enter() as well
    #
    def enter(self):
        self._enter()
        self.draw()

    #
    # process() - process a screen of stuff.  This is really the eventloop() for a
    #             screen.  Each individual screen can have their own _process() to 
    #             do any specific processing for that screen.  
    #
    def process(self):
        self.enter()                              # the start-up code for entering a screen
        while True:
            if self._process() or self.update():  # if the subclass needs it, or we need it, redraw
                self.draw()

            nextScreen = self.processEvents()     # process my events
            if nextScreen:
                if nextScreen == "back":          # request to go back up to parent
                    return None
                elif nextScreen == "quit":        # request to quit
                    return nextScreen
                else:                             # otherwise, decend to next screen
                    nextScreenObject = Screen.findScreen(nextScreen)
                    if not nextScreenObject:
                        print("ERROR: screen " + nextScreen + " not found.")
                        return("quit")
                    nextScreen = nextScreenObject.process()          # process this new screen and quit if asked
                    if nextScreen == "quit":
                        return nextScreen
                    self.enter()                                     # re-entering this screen

    def processEvents(self):
        while True:
            HARDWARE.checkButtons()
            event = pygame.event.poll()
            if event != pygame.NOEVENT:
                break

        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == HARDWARE.BUTTONUP or event.type == HARDWARE.BUTTONDOWN or event.type == HARDWARE.BUTTONHOLD:
            nextScreen = self.tables.processEvent(event)
            if nextScreen:
                return nextScreen
            nextScreen = self.buttons.processEvent(event)       # this will call my callbacks
            if nextScreen:
                return nextScreen
        return None
