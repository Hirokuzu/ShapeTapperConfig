import math
import random
import sys
import os
import re

#required for functions found online
import struct
import imghdr

# el2293t dimensions/screen size
screen_width = 1920
screen_height = 1080
screen_size = 42. # inches
dpi = math.hypot(screen_width, screen_height)/screen_size
screen_margin = 0
cm_per_inch = 2.54
format_string = "{:1.4f}"

def get_margin_width(img_diag):
    return screen_width - img_diag - screen_margin * dpi

def get_margin_height(img_diag):
    return screen_height - img_diag - screen_margin * dpi

def get_random_x(img_diag):
    #return randrange(int(img_width/2+dpi*screen_margin), int(screen_width-(img_width/2)-dpi*screen_margin))
    return random.randrange(0, get_margin_width(img_diag))

def get_random_y(img_diag):
    #return randrange(int(img_height/2+dpi*screen_margin), int(screen_height-(img_height/2)-dpi*screen_margin))
    return random.randrange(0, get_margin_height(img_diag))

# gets all files with names matching the expression '^blake_[0-9]*.png$' (nothing before, nothing after.)
def get_blake_imgs(directory):
    return [x for x in os.listdir(directory) if re.match('^blake_[0-9]*.png$', x)]

# gets all files with names matching the expression '^blake_[0-9]*.png$' (nothing before, nothing after.)
def get_images(directory):
    return [x for x in os.listdir(directory) if re.match('^.*(.png|.gif|.jpeg|.jpg)$', x)]

def get_scaling(vary_size, scaling_ratios):
    if(vary_size):
        return scaling_ratios[random.randint(0,len(scaling_ratios)-1)]
    else:
        return scaling_ratios[0] # just get the middle one

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24: #clearly the file isn't long enough
            return
        if imghdr.what(fname) == 'png': # grab the header
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height