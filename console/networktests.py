import pygame
from screen import Screen
from buttons import Button
import globalVariables as globals
from settings import Settings

# these two are necessary for getting wifi information
import socket
from subprocess import check_output

class NetworkTestsScreen(Screen):

    def __init__(self,name):
        Screen.__init__(self,name)


#        self.ButtonNW = self.buttons(bgcolor = (255,0,0), callback=self.mode1broadcast,
#                                     **Button.standardButton("NW",["Broadcast","Mode 0"],self.screen))
#        self.ButtonSW = self.buttons(bgcolor = (255,0,0), callback=self.stopbroadcast,
#                                     **Button.standardButton("SW","STOP",self.screen))
#        self.ButtonNE = self.buttons(bgcolor = (255,0,0), callback=self.connection,
#                                     **Button.standardButton("NE",["Connection","Test"],self.screen))
#        self.ButtonSE = self.buttons(bgcolor = (255,0,0), callback=self.mode2broadcast,
#                                     **Button.standardButton("SE",["Broadcast","Mode 1"],self.screen))

        self.ButtonS = self.buttons(bgcolor = (255,255,255), callback=self.done,lcolor=(0,0,0),
                                     **Button.standardButton("S","Done",self.screen))

    def _enter(self):
        self.screen.fill([0,0,0])             # just black, no graphic background image
        x = self.screen.get_width()
        y = self.screen.get_height()
        myfont = pygame.font.SysFont("monospace", 25)
        host = self.get_wifi_ssid()
        ip = self.get_ip_address()
        swidth = myfont.size(host)[0]
        sheight = myfont.size(host)[1]
        swidth2 = myfont.size(ip)[0]
        B1 = myfont.render(host, 1, (255,255,0))
        B2 = myfont.render(ip, 1, (255,255,0))
        self._setTitle("Network")
        self.screen.blit(B1,((x - swidth)/2,(y - sheight)/2))
        self.screen.blit(B2,((x - swidth2)/2,(y - sheight)/2+sheight))

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def get_wifi_ssid(self):
        output = check_output(["iwgetid","wlan0","--raw"])
        if output:
            return output.strip()
        else:
            return None

#        scanoutput = check_output(["iwlist", "wlan0", "scan"])
#        for line in scanoutput.split():
#            if line.startswith("ESSID"):
#                return line.split('"')[1]
#        return None

    def done(self):
        return "back"

#    def _process(self):

