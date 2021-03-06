#   
# buttons.py
#
#   Implements buttons on the screens.  It does both the virtual buttons next to
#   the real buttons, as well as the real buttons through their associated GPIO.
#   You can do a whole bunch of stuff with buttons, but there are also some
#   "standard" buttons that you can use to make programming easier.
#
#   The Button class keeps track of itself, and can be used to dispatch clicks to
#   the callbacks.  This class is used in multiple screens, so the class should
#   be "cloned" to make it so that button lists don't crash into each other.
#   See "screen.py" for how this is done.
#

import pygame
from utils import coordOffset
from hardware import HARDWARE

class Button():

    # here is the list of buttons that are in this class (or cloned class)
    buttonList = []

    flashSpeed = 250

                                          # NOTE - a "default" button is just a region that is clickable
    def __init__(self,
                 size,                    # a tuple of (width,height) for the button - prior to any rotation
                 position,                # a button location (x,y) - upper left corner AFTER rotation
                 labels=None,             # label for the button - multi-lines will attempt to center
                 font=None,               # the font to use - defaults to something nice
                 fontsize=None,           # the font size to use - defaults to something nice
                 rotation=0,              # 0,90,180,270 rotation of the button
                 bgcolor=None,            # the background color of the button
                 lcolor=(255,255,255),    # font and outline color for the button
                 outline=0,               # thickness of outline, zero means no outline
                 graphic=None,            # graphic to place on the button (NOT IMPLEMENTED YET)
                 flashing=0,              # if true, the content of the button will flash
                 gpio=None,               # the GPIO connected to the associated physical button
                 callback=None,           # callback when the button is pressed (synonym for downCallback)
                 downCallback=None,       # callback when the button is moves down
                 upCallback=None,         # callback when the button is moves up
                 holdCallback=None,       # callback when the button is held down
                 rock=None):              # if given, the rock will be passed to any callback called

        self.bgcolor = bgcolor
        self.setLabels(labels)

        if fontsize is not None:
            self.fontsize = fontsize
        else:
            self.fontsize = size[1]/3

        if not(font):
            font = pygame.font.SysFont('arial', self.fontsize, bold=True)        

        self.font = font
        self.lcolor = lcolor
        self.size = size                # gets adjusted if the button is rotated
        self.position = position        # does NOT get adjusted for rotation!
        self.rotation = rotation        # only does 0, 90, 180, 270
        self.outline = outline
        self.surface = pygame.Surface(self.size)
        self.graphic = graphic
        self.flashing = flashing
        self.flashState = True
        self.flashTarget = pygame.time.get_ticks() + self.__class__.flashSpeed
        self.gpio = gpio
        self.callback = callback
        self.upCallback = upCallback
        self.downCallback = downCallback
        self.holdCallback = holdCallback
        self.rock = rock
        self.needsUpdating = True                     # set to true if an update is necessary
        self.__class__.buttonList.append(self)

    #
    # setLabels() - simple method to set the labels for a button.  It was turned into a method
    #               so that they can be easily updated.
    #
    def setLabels(self,labels):
        self.needsUpdating = True
        if labels is None or isinstance(labels,list):
            self.labels = labels
        else:
            self.labels = [ labels ]   # target label needs to always be list of labels (or None)

    #
    # setFlash(self,on) - turns on flashing if on is true, otherwise flash is turned off
    #
    def setFlash(self,on):
        self.flashing = on
        self.flashState = True            # always turn the button back on when changing flashing
        self.needsUpdating = True

    #
    # clone() - ok, this is somewhat obscure
    #           By calling Button.clone("name") this routine will create a NEW class
    #           called "nameButtons" that inherits from Button, but has a different
    #           button list.  This makes it possible to easily have different sets of
    #           buttons for different screens.
    #
    @classmethod
    def clone(cls,name):
        return(type(name + "Buttons",(Button,object),{'buttonList':[]}))
    
    # NOTE to future self - the callback that is passed to a button, is normally from an
    # object instance of something.  so when it is passed, it is bound to the object
    # instance, becoming an "instance method" - so when calling the callback, below, the
    # "self" (object) gets passed to the method.

    @classmethod
    def processEvent(cls,event):
        for button in cls.buttonList:               # need to add GPIO events!

            if event.type == HARDWARE.BUTTONUP or event.type == HARDWARE.BUTTONDOWN or event.type == HARDWARE.BUTTONHOLD:
                if button.gpio == event.button:
                    if event.type == HARDWARE.BUTTONDOWN:
                        if hasattr(button,'callback') and button.callback:
                            return button._callit(button.callback)
                        if hasattr(button,'downCallback') and button.downCallback:
                            return button._callit(button.downCallback)
                    elif event.type == HARDWARE.BUTTONUP:
                        if hasattr(button,'upCallback') and button.upCallback:
                            return button._callit(button.upCallback)
                    elif event.type == HARDWARE.BUTTONHOLD:
                        if hasattr(button,'holdCallback') and button.holdCallback:
                            return button._callit(button.holdCallback)


            elif button.inside(event.pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(button,'callback') and button.callback:
                        return button._callit(button.callback)
                    if hasattr(button,'downCallback') and button.downCallback:
                        return button._callit(button.downCallback)
                if event.type == pygame.MOUSEBUTTONUP:
                    if hasattr(button,'upCallback') and button.upCallback:
                        return button._callit(button.upCallback)

    @classmethod
    def draw(cls,surface):
        for button in cls.buttonList:
            button._draw(surface)

    @classmethod
    def update(cls,surface):
        madeAChange = False
        for button in cls.buttonList:
            if button.needsUpdating:
                madeAChange = True
                button.needsUpdating = False
            if button.flashing and pygame.time.get_ticks() > button.flashTarget:
                button.flashState = not(button.flashState)
                button.flashTarget = pygame.time.get_ticks() + cls.flashSpeed
                madeAChange = True
        return madeAChange


    #
    # tableButton() - a shorthand for creating a button based upon a cell in a table.
    #
    @classmethod
    def tableButton(cls,table,cellName,location):
        if table.getCellSize(cellName) is None:
            return None
        return({ "size": table.getCellSize(cellName),
                 "position": coordOffset(location,table.getCellLocation(cellName)),
                 "graphic": table.getCellImage(cellName) })

    #
    # standardButton() - given an identifier and a surface (for laying out the button)
    #                    compose one of the "standard" buttons that are used throughout
    #                    this interface.  The return is a dictionary that can be fed into
    #                    the creation of a new button (to the __init__).  Note that colors
    #                    and fonts aren't specified for these buttons.
    #
    @classmethod
    def standardButton(cls,ident,name,surface):
        width = surface.get_width()
        height = surface.get_height()
        boxHeight = width/9
        boxWidth = height/3
        leftPosition = 0
        rightPosition = width-boxWidth
        topPosition = 0
        bottomPosition = height-boxHeight
        midPosition = (width-boxWidth)/2
        midBotPosition = height-boxHeight

        if ident == "NW":
            return({"size":(boxWidth,boxHeight),
                    "position":(leftPosition,topPosition),
                    "rotation":0,
                    "labels":name,
                    "gpio":HARDWARE.button.NW})
        elif ident == "SW":
            return({"size":(boxWidth,boxHeight),
                    "position":(leftPosition,bottomPosition),
                    "rotation":0,
                    "labels":name,
                    "gpio":HARDWARE.button.SW})
        elif ident == "NE":
            return({"size":(boxWidth,boxHeight),
                    "position":(rightPosition,topPosition),
                    "rotation":0,
                    "labels":name,
                    "gpio":HARDWARE.button.NE})
        elif ident == "SE":
            return({"size":(boxWidth,boxHeight),
                    "position":(rightPosition,bottomPosition),
                    "rotation":0,
                    "labels":name,
                    "gpio":HARDWARE.button.SE})
        elif ident == "S":
            return({"size":(boxWidth,boxHeight),
                    "position":(midPosition,midBotPosition),
                    "rotation":0,
                    "labels":name,
                    "gpio":HARDWARE.button.S})
        elif ident == "N":
            return({"size":(boxWidth,boxHeight),
                    "position":(midPosition,topPosition),
                    "rotation":0,
                    "labels":name})

    #
    # _callit() - a routine to make the code prettier - this calls the given callback
    #             with the rock if given, otherwise with no arguments.
    #
    def _callit(self,theCall):
        if self.rock is not None:
            return theCall(self.rock)
        else:
            return theCall()

    #
    # _drawLabel() - a routine to simplify the procedure of drawing labels in buttons
    #                This assumes that the whole surface is used to draw (ie - ignoring outline)
    #
    def _drawLabel(self,surface):
        if self.bgcolor is not None:
            surface.fill(self.bgcolor)
        if self.labels is not None and self.flashState:
            width,realHeight = surface.get_size()
            height = 0.7 * realHeight                         # leave some top and bottom
            heightDivision = height / len(self.labels)
            i = 0
            for label in self.labels:
                rwidth, rheight = self.font.size(label)
                x = (width-rwidth)/2
                y = max(0,(heightDivision-rheight))/2 + realHeight*0.15 + i*heightDivision
                renderedLabel = self.font.render(label,True,self.lcolor)
                surface.blit(renderedLabel,(x,y))
                i += 1


    #
    # _draw() - draws the given button on given surface - unlike the previous version of these
    #           routines, this one doesn't use surfaces for the buttons themselves, instead just
    #           drawing rectangles.
    #
    def _draw(self,surface):

        # drawing only happens if there is something to draw, this means that one or more of the
        # following need to be set:
        
        if self.outline != 0 or self.labels is not None or self.bgcolor is not None or self.graphic:

            if self.outline != 0:
                self.surface.fill(self.lcolor)

            width, height = self.size
            labelSurface = pygame.Surface((width - 2*self.outline,height - 2*self.outline))

            self._drawLabel(labelSurface)

            self.surface.blit(labelSurface,(self.outline,self.outline))

            if self.graphic:
                self.surface.blit(self.graphic,(0,0))

            buttonSurface = pygame.transform.rotate(self.surface,self.rotation)

            surface.blit(buttonSurface,self.position)

    def printClicked(self):
        print(" ".join(self.labels) + " clicked")

    #
    # inside() - returns True if the given position (x,y) is within the bounds
    #            the button itself.  Used for figuring out clicks.  Note that this
    #            duplicates the rotation so that the best possible job of matching
    #            clicks can be done
    #
    def inside(self,pos):

        x,y = pos;
        myx,myy = self.position

        # since rotation is only on 0,90,180,270 it is easy to get the right width/height
        if self.rotation % 180 == 0:
            width,height = self.size
        else:
            height,width = self.size

        return(x >= myx and 
               x <= myx + width and
               y >= myy and
               y <= myy + height)

