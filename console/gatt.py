#
# gatt.py
#
#   Defines the GATT database for any of the BLE operations independent
#   upon the implementation of the bluetooth.
#

class GATT (object):

    """Definition of the BLE GATT for the FCS"""

    # the service UUID was generated with www.uuidgenerator.net and is really
    # quite arbitrary.  Note that the dashes will be stripped before sending
    # to the RN4020

    ServiceUUID = "1840e436-bf53-45f1-a1dd-a56336e20377"

    # private characteristics are defined for peripherals to query
    # again, UUIDs were generated from the web site and are completely arbitrary
    # the second argument is the type, where type is:
    #
    #   INDICATE                0'b00100000    Indicate value of characteristic WITH 
    #                                            acknowledgment from server to client.
    #   NOTIFY                  0'b00010000    Notify value of characteristic WITHOUT
    #                                            acknowledgment from server to client.
    #   WRITE                   0'b00001000    Write value of characteristic WITH
    #                                            acknowledgment from client to server.
    #   WRITE WITHOUT RESPONSE  0'b00000100    Write value of characteristic WITHOUT
    #                                            acknowledgment from client to server.
    #   READ                    0'b00000010    Read value of characteristic. Value is
    #                                            sent from server to client.
    #   BROADCAST               0'b00000001    Broadcast value of characteristic.
    #
    # The third arg is the size in bytes.  Note that this format matches the format
    # used by the RN4020 BLE device, but can easily be translated to other devices.
    #
    # TODO: read is turned on for the attributes below, for testing.  They do NOT need
    #       to be read for distribiton. (0x08 instead of 0x0a)
    #
    # note that the handles for private characteristics will need to be added at run-time
    #
    #                                                                   PROPERY   MAX     16-BIT
    #                             UUID                                    TYPE   BYTES    HANDLE
    #                           -------------------------------------  --------- ------ -----------
    PrivateChars = [ dict(uuid="0d48b2e8-3312-11e6-ac61-9e71128cae77",type=0x0a,size=2, handle=None),  # robot number (for joining)
                     dict(uuid="0d48b6da-3312-11e6-ac61-9e71128cae77",type=0x0a,size=10,handle=None),  # R1 report (see report format)
                     dict(uuid="0d48b900-3312-11e6-ac61-9e71128cae77",type=0x0a,size=10,handle=None),  # R2 report
                     dict(uuid="0d48ba22-3312-11e6-ac61-9e71128cae77",type=0x0a,size=10,handle=None),  # B1 report
                     dict(uuid="0d48bb08-3312-11e6-ac61-9e71128cae77",type=0x0a,size=10,handle=None)   # B2 report
    ]
