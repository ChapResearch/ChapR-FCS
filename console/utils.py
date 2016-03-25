#
# utils.py
#
#   Utility functions.
#

import pygame
from time import sleep

#
# convertPosition() - an internal routine to convert a position given as words
#                      to one with real coordinates.  Given the dimensions of a
#                      target surface, and an incoming image/surface dimensions,
#                      return the position of size of the image.
#
def convertPosition(position,targetSize,imageSize):
    targetWidth = targetSize[0]
    targetHeight = targetSize[1]
    imageWidth = imageSize[0]
    imageHeight = imageSize[1]
    size = 1
    expandTarget = 0.9

    if position == "center":
        position = ((targetWidth - imageWidth)/2,(targetHeight - imageHeight)/2)
        
    elif position == "left-center":
        position = (0,(targetHeight - imageHeight)/2)

    elif position == "right-center":
        position = ((targetWidth - imageWidth),(targetHeight - imageHeight)/2)

    elif position == "expandY":            # height is used as expansion
        size = (targetHeight * expandTarget) / imageHeight
        imageHeight = imageHeight * size
        imageWidth = imageWidth * size
        position = ((targetWidth - imageWidth)/2,(targetHeight - imageHeight)/2)

    elif position == "expandX":            # height is used as expansion
        size = (targetWidth * expandTarget) / imageWidth
        imageHeight = imageHeight * size
        imageWidth = imageWidth * size
        position = ((targetWidth - imageWidth)/2,(targetHeight - imageHeight)/2)

        # really need a few more here...

    return(position,size)

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def showImage(image,position,fade=0):
    fade = float(fade)/2.5                        # makes the fade time more accurate                 
    theImage = pygame.image.load(image)
    theImage = theImage.convert(32)  # allows for smooth scaling - but gives a grey background
    screenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)

    if not isinstance(position,list):
        position,size = convertPosition(position,screenSize,(theImage.get_width(),theImage.get_height()))

    _showImage(theImage,position,size,fade)


def _showImage(theImage,position,size,fade):
    screen = pygame.display.get_surface()

    #theImage = pygame.transform.smoothscale(theImage,(int(theImage.get_width()*size),int(theImage.get_height()*size)))
    theImage = pygame.transform.scale(theImage,(int(theImage.get_width()*size),int(theImage.get_height()*size)))

    # if we're doing fade, we loop around, blocking in this routine during
    # the fade.  We assume that we're doing 100 steps per fade second.
    # NOTE that fade is only fade IN, not fade OUT at this time, so the last
    # thing that happens is a full draw of the image (makes everything easier)

    if fade > 0:
        surfaceCopy = screen.copy()
        delay = .01
        fadeSteps = fade * 100
        alphaStep = 255 / fadeSteps;

        for a in drange(0,255,alphaStep):
            theImage.set_alpha(None)
            theImage.set_alpha(a)
            screen.blit(surfaceCopy,(0,0))
            screen.blit(theImage,position)
            pygame.display.update()
            sleep(delay)

    theImage.set_alpha(255)
    screen.blit(theImage,position)
    pygame.display.update()

def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

def textOutline(font, message, fontcolor, outlinecolor, outlined):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    if outlined:
        img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img

#
# numberDraw() - draw the given number.  The number is enclosed in a
#                nice little white box.  The height is required and
#                will be the driving force for the display.  If width
#                is given, the containing box will be drawn in that
#                width, otherwise it will be draw a pleasing distance
#                from the number.  Set boxwitdh to zero if you want
#                it gone!
#
#     mode:  0 = 3 digit time
#            1 = 3 digits
#
def numberDraw(number,mode,color,height,width=0,title=None,titleColor=(255,255,255),boxWidth=2,boxColor=(255,255,255),outlined=True):

    outlineColor = (255,255,255)
    pad = height / 15
    titleHeight = height / 8

    # padding is the amount of space at the top or bottom of the number text (plus title if there is one)
    padding = (pad + boxWidth)*2 

    if title:
        padding += pad + titleHeight

    fontHeight = height - padding
    font = pygame.font.Font("Font/DSEG7Modern-Bold.ttf",fontHeight)
    fontWidth = font.size("8:88")[0]

    minWidth = fontWidth + 2 * pad + 2 * boxWidth
    if width < minWidth:
        width = minWidth

    surface = pygame.Surface((width,height))

    if mode == 0:
        text = "%01d:%02d" % (int(number / 60),number % 60)
    else:
        text = "%03d" % int(number)

    textSurface = textOutline(font,text,color,outlineColor,outlined)
    surface.fill((9,9,9))
    surface.set_colorkey((9,9,9))
    surface.set_alpha(255)
    X = boxWidth + pad
    Y = boxWidth + pad
    if title:
        Y += titleHeight + pad

    surface.blit(textSurface,(X,Y))

    if boxWidth:
        outline = pygame.Rect(0,0,width,height)
        pygame.draw.rect(surface,boxColor,outline,boxWidth)

    if title:
        titleFont = pygame.font.SysFont('arial', titleHeight, bold=True)        
        renderedTitle = titleFont.render(title,True,titleColor)
        surface.blit(renderedTitle,(int(pad+boxWidth),int(pad+boxWidth)))

    return(surface)

def removeKey(dict,key):
    del dict[key]
    return dict

#
# coordOffset() - offset the first coordinate by the second, and return
#                 the result.
#
def coordOffset(first,second):
    return( (first[0]+second[0],first[1]+second[1]) )

