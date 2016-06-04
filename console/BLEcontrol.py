#
# BLEcontrol.py
#
#   Implements the protocol over BLE for the robots.
#   The protocol data packets look like the following (with notes):
#
#    MAGIC: The magic number is a 2 byte number that identifies the packet as
#           a ChapFCS packet.  If the number doesn't match, then this is NOT
#           a ChapFCS packet.  This magic number is 0xC4A9
#
#    MODE: The mode is a 1 byte number that identifies the particular mode that
#          the console is currently operating in:
#                   mode = 0 ==> ON_DECK
#                   mode = 1 ==> READY
#                   mode = 2 ==> MATCH
#          The data in the broadcast packet is logically split into three segments
#          corresponding to the different modes.  The data is only valid during those
#          modes or earlier.
#
#    FIELD NAME:  The field name is limited to 12 characters.  And those characters
#                 can be selected from [a-z][A-Z][0-9][-] for a total of 64 possibilities
#                 organized from 1 to 63 in the order as show in the previous line.
#                 The zero value is reserved for end-of-name.  The 64 possibilities
#                 are packed into 6-bits (6x12 chars ==> 72 bits/9 bytes)
#
# Bytes:   2     1          9         1
#       ,-----,------,-------------,-----,
#       |magic| mode |     name    |match| ...            MODE 0 DATA - ON_DECK
#       '-----'------'-------------'-----'
# Byte#:   0     2         3-11       12
#
#
#   ROBOT ASSIGNMENT: A match has 4 robot "slots", 2 for Red and 2 for Blue.  Those
#                     slots are designated as R1, R2, B1, B2.  Each slot holds the
#                     integer equivalent of a robot number from 1 to 32,000'ish.
#                     The robot number is kept in 15 bits.  The top bit is used to
#                     indicate a "request for contact" from the console.  The robot
#                     requested should connect during the next connectable broadcast.
#
# Bytes:    2      2      2      2   
#       ,------,------,------,------,
#       |  R1  |  R2  |  B1  |  B2  | ...                 MODE 1 DATA - READY
#       '------'------'------'------'
# Byte#:   13     15     17     19   
#
#
#   ROBOT COMMAND: Commands are sent to the robots through broadcast.  Those commands
#                  are encoded in 4 bits for each robot, and can be different for each
#                  robot.
#
# Bytes:            1                       1 
#       ,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,
# (bits)|    R1C    |    R2C    |    B1C    |    B2C    | MODE 2 DATA - MATCH
#       '--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'
# Byte#:            21                      22
#
# ----------------------------------------------------------------------------------------
#
# Protocol Operation
#
#   MODE 0 - ON_DECK
#      An unconnectable broadcast packet is sent out for a time, followed by a connectable
#      packet.  The robots are expected to listen for a mode 0 broadcast packet that matches
#      their current match number.  When the robot hears the broadcast, it trys to connect
#      to the console during the next connectable broadcast.  Once connected, the robot sends
#      its robot number to (1) provide the number to the console, and (2) indicate its desire
#      to join the given match.  After sending data, the robot breaks the connection, and
#      waits for a MODE 1 - READY broadcast.
#
#   MODE 1 - READY
#      Robots are waiting for a MODE 1 - READY broadcast after connecting.  Once they receive
#      the broadcast, they check to see if they are accepted for the match.  If not, they
#      return to the initial state (after feedback to the user).  If so, they start monitoring
#      the broadcasts, and will connect to console when invited to do so.  After connecting,
#      the robot identifies itself and transmits battery information to the console.  The console
#      uses this information to (1) ascertain if there is still a connection to the robot,
#      (2) gather signal statistics from the robot, and (3) gather battery information from the
#      robot.  Robots are always listening for the beginning of MODE 2 - MATCH during this time.
#
#   MODE 2 - MATCH
#      When robots receive a MODE 2 - MATCH broadcast, they stop listening for connection requests
#      and start, instead, listening for commands from the console.  As such, they stop transmitting
#      their statistics and the console simply issues commands, no longer worrying about connection.
#      Robots will continue in this mode, operating on commands, until any other mode broadcast is
#      received.  NOTE that a "fall-back" to MODE 1 - READY is possible.  In which case, the robot
#      will revert to MODE 1 - READY operation, transmitting statistics as defined.  This fall-back
#      may occur between segments of a match.
#
# ----------------------------------------------------------------------------------------
#
# This protocol is encapsulated into the BLEprotocol object.  Methods of the object
# configure the protocol modes, and implement the protocol by using the RN4020 module.
# A thread is kicked off upon instantiation of this object, to manage communication with
# the RN4020 module.  This thread ensures that the data in this object is current while
# implementing the protocol.
#
# The main thread is somewhat oblivious to the protocol that is running in the sub-thread.
# It simply tells the sub-thread what to do.  Information is communicated back to the
# main thread through a class object.  Main calls are:
#
#  pause() - console stops all communcation, including broadcast (default upon init)
#  resume() - console resumes where it left off
#  reset() - clears all state information, re-initializing the lists and protocol (defaults mode to ON_DECK, enters pause)
#  mode(x) - starts mode ON_DECK, READY, or MATCH - mode(ON_DECK) is default upon init
#  robots() - returns a list of robots depending upon the mode:
#                  mode ON_DECK - the robots that have asked to join the match
#                  mode READY/MATCH - the robots that are currently accepted as part of the match
#  command() - issues a command to one or more robots, the "all" argument takes precedent, otherwise any
#              or all of the commands can be issued
#                  all=cmd   - issued to all robots
#                  R1=cmd    - issued to R1 robot 
#                  R2=cmd    - issued to R2 robot 
#                  B1=cmd    - issued to B1 robot 
#                  B2=cmd    - issued to B2 robot 
#              It is possible that commands "stack up" such that multiple calls to commands are done in
#              a fashion that the subthread hasn't yet consumed a command when the next one comes in.
#              Since commands are simply being broadcast, that is, the subthread really doesn't do much
#              except store them, the main thread will block until the sub-thread "consumes" a command.
#              In other words, there is no list/queue of incoming commands for the sub-thread.
#  stats() - returns a list of robots with stats (signal, battery, last contact)


import threading

class Robot(object):
    R1 = 0           # these are the standardized identifiers for robots
    R2 = 1           #   which are normally used for indicies of arrays
    B1 = 2
    B2 = 3

class RobotData(object):

    def __init__(self):
        self.dataLock = threading.Lock()
        self.robotData = []
        
    def setRobotList(self, R1,R2,B1,B2):
        # lock it here

    # note that the actual data for the robot isn't described here!  There needs to be some
    #   agreement eventually to the data order/form.
    # note, too, that the "copy" that occurs when getting the robot data is one level deep
    #  so it is assumed that robot data is one level deep, and that the items themselves don't change

    def setRobotData(self,robot,**args):
        self.dataLock.acquire()
        self.robotData[robot] = args
        self.dataLock.release()

    def getRobotData(self,robot):
        self.dataLock.acquire()
        snapshot = dict(self.robotData[robot])    # gets a copy so it is thread safe - ONE LEVEL ONLY
        self.dataLock.release()
        return snapshot



#
# class BLEprotocol:
#
#   This class is the work-horse of the thread controlling and communicating with the rn4020.
#   In fact, it is the only thing talking to it.  The main BLE control object kicks off this
#   thread when it initializes.  The BLE control object is responsible for communication with
#   the protocol sub-thread/object.
        
class BLEprotocol(object):


class BLEcontrol(object):

    robotData = RobotData()              # this class variable is used to pass the robot data
                                         # from the subthread to the main thread, it has getter and
                                         # setter methods that are thread-safe

    def __init__(self):
        self.protocolThread = threading.Thread(target=BLEProtocol)

        self.worker.start()              # start the thread right away
        self.rn4020 = RN4020()           # this doesn't work in simulation btw


#
# BLE sub thread
#
#   The BLE sub thread manages all communication to the rn4020, both TO it and FROM
#   it...in particular FROM it.  Many events happen asyncronously relative to the
#   console, and this thread organizes those and allows them to be presented appropriately
#   to the main thread.
#
#   The sub thread operates in MODES.  These modes control what it is expecting and
#   what the main thread is expected to be able to get from it.  These modes mirror
#   the modes for robot status:
#
#   Mode 0: ON DECK
#

    @classmethod
    def subThread(cls):
        # this is the work-horse of the protocol
