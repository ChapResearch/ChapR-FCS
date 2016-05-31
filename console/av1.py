#
# av1.py
#
#  Implements the AV1 character encoding.  Used to
#  pack characters together so we can send a 12 character
#  name in 9 bytes.

import math

class AV1 (object):

    # this is a test piece of data that is ABCD in AV1

    #   "ABCD" = 000001 000010 000011 000100 = 0x04, 0x20, 0xC4
    test1 = (0x04,0x20,0xC4)
    test2 = (0x04,0x20,0x00)
    test3 = (0x04,0x20,0xC4,0x04,0x20,0xC4)

    # to do quick conversions from AV1 <--> ASCII, we need some lookup tables
    # Going from AV1 --> ASCII is pretty simple because we take the 6 bits of AV1 and index an easy table
    #  that has the ASCII characters listed.  Told you it was simple.  NOTE that 0x00 in the array shows
    #  mapping to a space...however, that is special cased in the code to signal end-of-string.

    #                           0000000000000000111111111111111122222222222222223333333333333333
    #                           0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF
    fromAV1toASCII = bytearray(" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-")

    # From ASCII --> AV1 is harder.  Since the output is simply bytes, we can't use strings 
    #   - but we only do 128 bytes as opposed to 256

    fromASCIItoAV1 = (0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,
                      0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,
                      0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,
                      0x3E,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3F,0x3F,0x3F,0x3F,0x3F,0x3F,
                      0x3F,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,
                      0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x3f,0x3F,0x3F,0x3F,0x3F,
                      0x3F,0x1B,0x1C,0x1D,0x1E,0x1F,0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,
                      0x2A,0x2B,0x2C,0x2D,0x2E,0x2F,0x30,0x31,0x32,0x33,0x34,0x3f,0x3F,0x3F,0x3F,0x3F)

    #
    # pack() - given a normal string, pack it into AV1-encoded bytes.  The output array is padded with a
    #          zero AV1 character if necessary.  If "count" is given, then the output array will have
    #          that many AV1 characters in it.
    #
    @classmethod
    def pack(cls,string,*args):
        length = len(string)
        input = bytearray(string)
        inputPtr = 0

        if len(args) > 0:
            count = args
        else:
            count = int(math.ceil(length * 6.0 / 8))

        outarray = bytearray()
        outPtr = 0

        while  inputPtr < length:

            b = cls.fromASCIItoAV1[input[inputPtr] & 0x7f]

            if inputPtr % 4 == 0:
                outarray.append(b<<2 & 0xFC)

            elif inputPtr % 4 == 1:
                outarray[outPtr] |= (b>>4 & 0x03)
                outarray.append(b<<4 & 0xF0)
                outPtr += 1

            elif inputPtr % 4 == 2:
                outarray[outPtr] |= (b>>2 & 0x0F)
                outarray.append(b<<6 & 0xC0)
                outPtr += 1

            elif inputPtr % 4 == 3:
                outarray[outPtr] |= b & 0x3F
                outPtr += 1

            inputPtr += 1

        if length < count:            # need to pad a few bits
            diff = count - length

            if inputPtr % 4 == 0:
                bytes2Append = int(math.ceil(diff * 6.0 / 8))

            if inputPtr % 4 == 1:
            if inputPtr % 4 == 2:
            if inputPtr % 4 == 3:

        return outarray


    #
    # unpack() - given a 6-bits-per-character AV1 "string" (an array of bytes)
    #            unpack it into an ASCII string.  The "count" is how many of
    #            the "bits" are valid in the array of bytes - in other words,
    #            "count" number of valid AV1 characters in the input array.  If the
    #            count is too small, then the last bytes are effectively ignored.
    #
    @classmethod
    def unpack(cls,packedAV1,*args):
        countPtr = 0
        inputPtr = 0
        length = len(packedAV1)

        if len(args) > 0:
            count = args[0]
        else:
            count = length * 8 / 6

        if length * 8 < count * 6:
            raise ValueError('Too few bytes for count')
            
        outBytes = bytearray()

        while countPtr < count:

            if countPtr < count and countPtr % 4 == 0:
                countPtr += 1
                b = packedAV1[inputPtr] >> 2 & 0x3f
                if b == 0:
                    break
                outBytes.append(cls.fromAV1toASCII[b])

            if countPtr < count and countPtr % 4 == 1:
                countPtr += 1
                b = (packedAV1[inputPtr] << 4 & 0x30) | (packedAV1[inputPtr+1] >> 4 & 0x0f)
                if b == 0:
                    break
                outBytes.append(cls.fromAV1toASCII[b])
                inputPtr += 1
            
            if countPtr < count and countPtr % 4 == 2:
                countPtr += 1
                b = (packedAV1[inputPtr] << 2 & 0x3C) | (packedAV1[inputPtr+1] >> 6 & 0x03)
                if b == 0:
                    break
                outBytes.append(cls.fromAV1toASCII[b])
                inputPtr += 1
            
            if countPtr < count and countPtr % 4 == 3:
                countPtr += 1
                b = packedAV1[inputPtr] & 0x3f
                if b == 0:
                    break
                outBytes.append(cls.fromAV1toASCII[b])
                inputPtr += 1
            
        # return outBytes.decode("ascii")
        return "".join(map(chr,outBytes))
