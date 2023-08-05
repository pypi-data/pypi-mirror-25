# Python modules
from __future__ import division

# 3rd party modules

# Our modules


def vax_to_ieee_single_float(data):
    """Converts floats in Vax format to IEEE format.

    data should be a single string of chars that have been read in from 
    a binary file. These will be processed 4 at a time into float values.
    Thus the total number of byte/chars in the string should be divisible
    by 4.
    
    Based on VAX data organization in a byte file, we need to do a bunch of 
    bitwise operations to separate out the numbers that correspond to the
    sign, the exponent and the fraction portions of this floating point
    number
    
    role :      S        EEEEEEEE      FFFFFFF      FFFFFFFF      FFFFFFFF
    bits :      1        2      9      10                               32
    bytes :     byte2           byte1               byte4         byte3    
    
    """
    f = []
    nfloats = int(len(data) / 4)
    for i in range(nfloats):
        byte2 = data[0 + i*4]
        byte1 = data[1 + i*4]
        byte4 = data[2 + i*4]
        byte3 = data[3 + i*4]
        
        # hex 0x80 = binary mask 10000000
        # hex 0x7f = binary mask 01111111
        
        sign  =  (ord(byte1) & 0x80) >> 7
        expon = ((ord(byte1) & 0x7f) << 1 )  + ((ord(byte2) & 0x80 ) >> 7 )
        fract = ((ord(byte2) & 0x7f) << 16 ) +  (ord(byte3) << 8 ) + ord(byte4)
        
        if sign == 0:
            sign_mult =  1.0
        else:
            sign_mult = -1.0
        
        if 0 < expon:
            # note 16777216.0 == 2^24  
            val = sign_mult * (0.5 + (fract/16777216.0)) * pow(2.0, expon - 128.0)   
            f.append(val)
        elif expon == 0 and sign == 0:
            f.append(0)
        else: 
            f.append(0)
            # may want to raise an exception here ...
        
    return f
