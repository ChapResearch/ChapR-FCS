#
# hardware.py
#
#   Definitions for the hardware of the console.  Most things
#   refer to the pins of the GPIO of the RPi.  But there are
#   a few other things too.
#

class HARDWARE:

# the RN4020 uses pins 18, 4, and 22, and also the serial port
# on pins XX,YY - but that uses the serial driver and is referenced
# as a TTY

    class rn4020:
        wake = 4
        mldp = 18
        connected = 22
        tty = "/dev/ttyAMA0"
        baud = 115200

# the mini-display uses the SPI pins as defined below.  they aren't
# used by this code, but are here to document that they ARE being
# used by the display/framebuffer driver
# ACCORDING TO THE 4D DOCS:
#   pin  gpio  status
#  ----- ----  -----------
#    4      0   unused  (could be GPIO 2)
#    6      1   unused  (could be GPIO 3)
#    7     14   unused  (UART for RN4020)
#    8      4   unused  (WAKE for RN4020)
#    9     15   unused  (UART for RN4020)
#   11     18   unused if not using PWM (MLDP for RN4020)
#   12   PENIRQ touch interrupt (GPIO17)
#   14   KEYIRQ button interrupt (next revision) (GPIO27 or GPIO21)
#   15     23   unused
#   16     22   unused  (CONNECTED for RN4020)
#   17     24   unused
#   20   MOSI
#   21     25   unused
#   22   MISO
#   23    CS0   SPI select for display
#   24   SCLK
#   25    CS1   SPI select for touch

    class display:
        ce1 = 7
        ce0 = 8
        miso = 9
        mosi = 10
        clk = 11

# buttons on the console use remaining GPIO on the RPi as below
# good candidates: 23,24,25 for sure
#                  2/3 (or 0/1) instead of I2C
#                  21 (or 27) overusing KEYIRQ if possible        
# CURRENTLY - the buttons are wired to P5 on the Rev2 board
#             connected to 28,29,30,31 - should have really
#             put a connector on there though!

    class button:
        NW = 31
        SW = 30
        NE = 29
        SE = 28
        S = 23
