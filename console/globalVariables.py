#
# globalVariables.py
#
#   This module defines all of the global variables so that they can be shared
#   among all of the other modules.
#

#   ____  _         _             _      
#  / ___|| |  ___  | |__    __ _ | | ___ 
# | |  _ | | / _ \ | '_ \  / _` || |/ __|
# | |_| || || (_) || |_) || (_| || |\__ \
#  \____||_| \___/ |_.__/  \__,_||_||___/
#                                        
# These are used throughout the program within many modules
# (hence the "globals" :-)

autoTime = 30                    # autonomous period time in seconds
teleopTime = 240                 # time for teleop in seconds
endGameTime = 30                 # end-game seconds
matchNumber = 0                  # the match number we are on (changes frequently)

YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
