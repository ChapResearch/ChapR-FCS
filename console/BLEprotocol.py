#
# BLEprotocol.py
#
#   Implements the BLE protocol, independent upon the interface to BLE.
#   All methods are class methods.
#
#    MAGIC: The magic number is a 2 byte number that identifies the packet as
#           a ChapFCS packet.  If the number doesn't match, then this is NOT
#           a ChapFCS packet.  This magic number is 0xC4A9
#
#    MODE: The mode is a 1 byte number that identifies the particular mode that
#          the console is currently operating in:
#                   mode = 0 ==> WAITING
#                   mode = 1 ==> ON_DECK
#                   mode = 2 ==> READY
#                   mode = 3 ==> MATCH
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
# Bytes:   2     1         9       
#       ,-----,-----,-------------,
#       |magic|  0  |     name    |...            MODE 0 DATA - WAITING
#       '-----'-----'-------------'
# Byte#:   0     2        3-11     
#
# Bytes:   2     1         9         1
#       ,-----,-----,-------------,-----,
#       |magic|  1  |     name    |match| ...            MODE 1 DATA - ON_DECK
#       '-----'-----'-------------'-----'
# Byte#:   0     2        3-11       12
#
#
#   ROBOT ASSIGNMENT: A match has 4 robot "slots", 2 for Red and 2 for Blue.  Those
#                     slots are designated as R1, R2, B1, B2.  Each slot holds the
#                     integer equivalent of a robot number from 1 to 32,000'ish.
#                     The robot number is kept in 15 bits.  The top bit is used to
#                     indicate a "request for contact" from the console.  The robot
#                     requested should connect during the next connectable broadcast.
#
#     Bytes:    2      2      2      2   
#           ,------,------,------,------,
#        ...|  R1  |  R2  |  B1  |  B2  | ...                 MODE 2 DATA - READY
#           '------'------'------'------'
#     Byte#:   13     15     17     19   
#
#
#   ROBOT COMMAND: Commands are sent to the robots through broadcast.  Those commands
#                  are encoded in 4 bits for each robot, and can be different for each
#                  robot.
#
# Bytes:            1                       1 
#       ,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,
# (bits)|    R1C    |    R2C    |    B1C    |    B2C    | MODE 3 DATA - MATCH
#       '--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'
# Byte#:            21                      22
#
# ----------------------------------------------------------------------------------------
#
# Protocol Operation
#
#   MODE 0 - WAITING
#      In this mode, the console is simply broadcasting it's presence.  All robots can see
#      the console, but they cannot connect to it.  Further, the "match number" isn't really
#      available, because the console is in a mode where it may not be valid.  It is important
#      to point out, that if the console ever switches back to Mode 0 from another mode (like
#      from mode 1 for example) that the robots need to assume that all previous information
#      has been lost, so, for example, they need to tell the console that they are interested
#      in joining AGAIN.
#
#   MODE 1 - ON_DECK
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
# This protocol is encapsulated into the BLEprotocol object.  NOTE that this doesn't prescribe
# the particular BLE driver such as the RN4020 for example.  All methods in this file are class
# methods, so no object is necessary.

from av1 import AV1
import binascii

class BLEprotocol(object):

    #
    # messageHeader() - generates the standard message header for all messages along with the
    #                   mode, fieldName, and match number.
    #                    fieldName - up to 12 character string - will be encoded in av1 9 bytes
    #                    match - match number between 0 and 255
    #
    @classmethod
    def messageHeader(cls,mode,fieldName,match=0):
        message = "C4A9"                                   # the magic number
        message += "%02x" % mode                           
        message += binascii.b2a_hex(AV1.pack(fieldName,9))
        message += "%02x" % match
        return message

    #
    # mode0Message() - generates an ascii representation of a bluetooth message for the mode 0
    #                  protocol, which is just the header.  Note that a mode 0 message includes
    #                  the match, but since it is labeled as mode 0, it should be ignored.
    #
    @classmethod
    def mode0Message(cls,fieldName):
        mode = 0
        message = BLEprotocol.messageHeader(mode,fieldName,0)
        return message

    #
    # mode1Message() - generates an ascii representation of a bluetooth message for the mode 1
    #                  protocol, which is just the header.
    #
    @classmethod
    def mode1Message(cls,fieldName,match):
        mode = 1
        message = BLEprotocol.messageHeader(mode,fieldName,match)
        return message

    #
    # mode2Message() - generates an ascii representation of a bluetooth message for the mode 2
    #                  protocol.
    #                    R1,R2,B1,B2 - team numbers between 0x0000 and 0x7FFF - top bit for xmit request
    #                    xmitReq - a number where number%4 positionaly points to who transmits stats next
    #
    @classmethod
    def mode2Message(cls,fieldName,match,R1,R2,B1,B2,xmitReq):
        mode = 2
        message = BLEprotocol.messageHeader(mode,fieldName,match)
        xmitReq = xmitReq % 4

        defaultTeam = 0

        R1 = defaultTeam if R1 is None else R1       # if any team is None it transmits as defaultTeam
        R2 = defaultTeam if R2 is None else R2
        B1 = defaultTeam if B1 is None else B1
        B2 = defaultTeam if B2 is None else B2

        message += "%04x" % (( R1 &0x7fff)|(0x8000 if xmitReq == 0 else 0x0000))
        message += "%04x" % (( R2 &0x7fff)|(0x8000 if xmitReq == 1 else 0x0000))
        message += "%04x" % (( B1 &0x7fff)|(0x8000 if xmitReq == 2 else 0x0000))
        message += "%04x" % (( B2 &0x7fff)|(0x8000 if xmitReq == 3 else 0x0000))

        return message
