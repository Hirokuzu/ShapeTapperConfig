from random import randrange
import sys
import os
import re
import math

#required for functions found online
import struct
import imghdr


# ODDBALL CONFIG GENERATOR
# uses blake shapes only.

#things you might want to change
# other variable initializations. Should set so they can be changed/configured.
feedback = 0
practice = 1
block_pass_percent = 0
block_fb = 1
timeout = 60
total1 = total2 = total3 = timeout
onset = 1
blake_directory = './Assets/Resources/Images/'
screen_width = 1440
screen_height = 900
screen_aspect = screen_width/screen_height
width_unit = 16
height_unit = 10
screen_size_inch = 20
screen_margin = 0
dpi = screen_width/(width_unit*screen_size_inch/math.sqrt((math.pow(width_unit,2)+math.pow(height_unit,2))))
number_of_angles = 18 #number of angles, should divide 360 evenly

safety_margin_1 = 40
safety_margin_2 = 40
safety_margin_3 = 40


# define number of blocks, trials per block
# set in main
num_blocks = 0
num_trials = 0

#delimiter
delimiter = ","

def get_margin_width(img_diag):
    return screen_width - img_diag - screen_margin * dpi

def get_margin_height(img_diag):
    return screen_height - img_diag - screen_margin * dpi

def get_random_x(img_diag):
    #return randrange(int(img_width/2+dpi*screen_margin), int(screen_width-(img_width/2)-dpi*screen_margin))
    return randrange(0, get_margin_width(img_diag))

def get_random_y(img_diag):
    #return randrange(int(img_height/2+dpi*screen_margin), int(screen_height-(img_height/2)-dpi*screen_margin))
    return randrange(0, get_margin_height(img_diag))

def get_cartesian_distance(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

#gives diagonal of a right angle triangle/rectangle given the two sides
def get_diagonal(x,y):
    return math.sqrt(math.pow(x,2)+math.pow(y,2))

# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else:
        num_blocks = 9
        num_trials = 75

    for block in range(0,num_blocks):
        for trial_num in range(0,num_trials):
            #figure out which images to use first
            blake_files = get_blake_imgs(blake_directory)
            image_1 = blake_files[randrange(0,len(blake_files))]
            image_2 = blake_files[randrange(0,len(blake_files))]
            while image_1 == image_2:
                image_2 = blake_files[randrange(0,len(blake_files))]
            #figure out positions
            # get image sizes
            # images are scaled to a percentage of the height, along the images' diagonal
            img_1_width, img_1_height = get_image_size(blake_directory + image_1)
            img_1_diag = get_diagonal(img_1_width, img_1_height)
            img_1_scale = img_1_diag/float(safety_margin_1)/100*screen_height
            img_1_width /= img_1_scale
            img_1_height /= img_1_scale
            img_1_diag = float(safety_margin_1)/100*screen_height
            #print("img1scale: " + str(img_1_scale))
            #print("img_1_width: " + str(img_1_width) + "; img_1_height: " + str(img_1_height) + "; img_1_diag: " + str(img_1_diag))

            img_2_width, img_2_height = get_image_size(blake_directory + image_2)
            img_2_diag = get_diagonal(img_2_width, img_2_height)
            img_2_scale = img_2_diag/float(safety_margin_2)/100*screen_height
            img_2_width /= img_2_scale
            img_2_height /= img_2_scale
            img_2_diag = float(safety_margin_2)/100*screen_height
            #print("img2scale: " + str(img_2_scale))
            #print("img_2_width: " + str(img_2_width) + "; img_2_height: " + str(img_2_height) + "; img_2_diag: " + str(img_2_diag))

            img_3_width, img_3_height = get_image_size(blake_directory + image_2)
            img_3_diag = get_diagonal(img_3_width, img_3_height)
            img_3_scale = img_3_diag/float(safety_margin_3)/100*screen_height
            img_3_width /= img_3_scale
            img_3_height /= img_3_scale
            img_3_diag = float(safety_margin_3)/100*screen_height
            #print("img3scale: " + str(img_3_scale))
            #print("img_3_width: " + str(img_3_width) + "; img_3_height: " + str(img_3_height) + "; img_3_diag: " + str(img_3_diag))

            pos_img_1_x = get_random_x(round(img_1_diag))
            pos_img_1_y = get_random_y(round(img_1_diag))
            pos_img_2_x = pos_img_1_x
            pos_img_2_y = pos_img_1_y
            pos_img_3_x = pos_img_1_x
            pos_img_3_y = pos_img_1_y

            #potential for infinite loop depending on image sizes. for 1080p shouldn't be a problem.
            while (get_cartesian_distance(pos_img_1_x,pos_img_1_y,pos_img_2_x,pos_img_2_y) < (img_1_diag + img_2_diag)/2
                or get_cartesian_distance(pos_img_1_x,pos_img_1_y,pos_img_3_x,pos_img_3_y) < (img_1_diag + img_3_diag)/2
                or get_cartesian_distance(pos_img_2_x,pos_img_2_y,pos_img_3_x,pos_img_3_y) < (img_2_diag + img_3_diag)/2
                ): #while the image distances overlap
                pos_img_1_x = get_random_x(round(img_1_diag))
                pos_img_1_y = get_random_y(round(img_1_diag))
                pos_img_2_x = get_random_x(round(img_2_diag))
                pos_img_2_y = get_random_y(round(img_2_diag))
                pos_img_3_x = get_random_x(round(img_3_diag))
                pos_img_3_y = get_random_y(round(img_3_diag))

            #convert positions into percentages (wait what this might mean overlap)
            pos_img_1_x = int(round(pos_img_1_x * float(100)/get_margin_width(img_1_diag)))
            pos_img_1_y = int(round(pos_img_1_y * float(100)/get_margin_height(img_1_diag)))
            pos_img_2_x = int(round(pos_img_2_x * float(100)/get_margin_width(img_2_diag)))
            pos_img_2_y = int(round(pos_img_2_y * float(100)/get_margin_height(img_2_diag)))
            pos_img_3_x = int(round(pos_img_3_x * float(100)/get_margin_width(img_3_diag)))
            pos_img_3_y = int(round(pos_img_3_y * float(100)/get_margin_height(img_3_diag)))

            #identifier
            trial_config = str(block+1) + delimiter
            trial_config += str(trial_num+1) + delimiter

            #trial specific
            trial_config += str(feedback) + delimiter

            #block level stuff
            trial_config += str(practice) + delimiter
            trial_config += str(block_pass_percent) + delimiter
            trial_config += str(block_fb) + delimiter

            #trial-specific stuff
            trial_config += str(timeout) + delimiter
            trial_config += delimiter
            trial_config += delimiter * 5 # janky stuff to skip dynamic masks - not used in oddball
            trial_config += str(1) + delimiter # this is number of replays of trial within timeout, but again, not used in oddball
            trial_config += str(pos_img_1_x) + delimiter
            trial_config += str(pos_img_1_y) + delimiter
            trial_config += str(onset) + delimiter
            
            #image 1
            trial_config += (image_1.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * randrange(0,360/number_of_angles)) + delimiter
            trial_config += str(safety_margin_1) + delimiter
            trial_config += str(1) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 2
            trial_config += (image_2.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * randrange(0,360/number_of_angles)) + delimiter
            trial_config += str(safety_margin_2) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 3
            trial_config += (image_2.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * randrange(0,360/number_of_angles)) + delimiter
            trial_config += str(safety_margin_3) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            # no image_off for image 3

            #bonus oddball config stuff
            trial_config += str(1) + delimiter #oddball_flag
            trial_config += str(pos_img_2_x) + delimiter
            trial_config += str(pos_img_2_y) + delimiter
            trial_config += str(pos_img_3_x) + delimiter
            trial_config += str(pos_img_3_y)
            print(trial_config)
    return


# gets all files with names matching the expression '^blake_[0-9]*.png$' (nothing before, nothing after.)
def get_blake_imgs(directory):
    return [x for x in os.listdir(directory) if re.match('^blake_[0-9]*.png$', x)]


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

if __name__ == "__main__":
    main()
