import pygame
from screen import Screen
from buttons import Button
import os

class AudioTestScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)
        self.screen.fill([0,0,0])
        self.redraw = True
        self._setTitle("Audio Test")

        self.soundFX = pygame.mixer.Sound(os.path.join('Media','StartAuto.wav'))
        self.myfont = pygame.font.SysFont("impact", 50)
        self.label = self.myfont.render("Playing Sound", 1, (255,255,255))

        print("This is working")
        
        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.play,
                                     **Button.standardButton("SW",["Play","Sound"],self.screen))
        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done,lcolor = (0,0,0),
                                    **Button.standardButton("S","Done",self.screen))        

    def _enter(self):
        pass

    def done(self):
        return "back"

    def play(self):
        self.soundFX.play()
        self.screen.blit(self.label, (120,150))
        self.redraw = True

    def _process(self):
        if pygame.mixer.get_busy() == False:
            self.screen.fill([0,0,0])
            self.redraw = True
            self._setTitle("Audio Test")

        redraw = self.redraw
        self.redraw = False
        return redraw


