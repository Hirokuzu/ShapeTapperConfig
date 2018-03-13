from random import randrange
import sys
import os
import re

#required for functions found online
import struct
import imghdr


# ODDBALL CONFIG GENERATOR
# uses blake shapes only.

#things you might want to change
# other variable initializations. Should set so they can be changed/configured.
feedback = 1
practice = 1
block_pass_percent = 70
block_fb = 1
timeout = 5
total1 = total2 = total3 = timeout
onset = 1
blake_directory = './blake_images/'
screen_width = 1920
screen_height = 1080
number_of_angles = 18 #number of angles, should divide 360 evenly

safety_margin_1 = 33
safety_margin_2 = 33
safety_margin_3 = 33


# define number of blocks, trials per block
num_blocks = 4
num_trials = 10

#delimiter
delimiter = ","


# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else: # define number of blocks, trials per block
        num_blocks = 4
        num_trials = 10

    for block in range(0,num_blocks):
        for trial_num in range(0,num_trials):
            #figure out which images to use first
            blake_files = get_blake_imgs(blake_directory)
            image_1 = blake_files[randrange(0,len(blake_files))]
            image_2 = image_1
            while image_1 == image_2:
                image_2 = blake_files[randrange(0,len(blake_files))]
            #figure out positions
            # get image sizes
            img_1_width, img_1_height = get_image_size(blake_directory + image_1)
            img_2_width, img_2_height = get_image_size(blake_directory + image_2)

            pos_img_1_x = randrange(img_1_width/2, screen_width-(img_1_width/2))
            pos_img_1_y = randrange(img_1_height/2, screen_height-(img_1_height/2))
            pos_img_2_x = pos_img_1_x
            pos_img_2_y = pos_img_1_y

            #potential for infinite loop depending on image sizes. for 1080p shouldn't be a problem.
            while (abs(pos_img_1_x-pos_img_2_x) < (img_1_width + img_2_width)/2
               and abs(pos_img_1_y-pos_img_2_y) < (img_1_height + img_2_height)/2
               ): #while the image distances overlap
                pos_img_2_x = randrange(img_2_width/2, screen_width-(img_2_width/2))
                pos_img_2_y = randrange(img_2_height/2, screen_height-(img_2_height/2))
            
            #the following if statements will be confusing as there are two images with three rendered on-screen
            # images 2 and 3 are the same, just that their positions have to be different.
            pos_img_3_x = pos_img_1_x
            pos_img_3_y = pos_img_1_y
            while (abs(pos_img_1_x-pos_img_3_x) < (img_1_width + img_2_width)/2
               and abs(pos_img_1_y-pos_img_3_y) < (img_1_height + img_2_height)/2
               and abs(pos_img_2_x-pos_img_2_x) < (img_1_width + img_2_width)/2
               and abs(pos_img_2_y-pos_img_2_y) < (img_1_height + img_2_height)/2
               ): #while the image distances overlap
                pos_img_3_x = randrange(img_2_width/2, screen_width-(img_2_width/2))
                pos_img_3_y = randrange(img_2_height/2, screen_height-(img_2_height/2))

            #convert positions into percentages (wait what this might mean overlap)
            to_percent_width = float(100)/screen_width
            to_percent_height = float(100)/screen_height
            pos_img_1_x = int(round(pos_img_1_x * to_percent_width))
            pos_img_1_y = int(round(pos_img_1_y * to_percent_height))
            pos_img_2_x = int(round(pos_img_2_x * to_percent_width))
            pos_img_2_y = int(round(pos_img_2_y * to_percent_height))
            pos_img_3_x = int(round(pos_img_3_x * to_percent_width))
            pos_img_3_y = int(round(pos_img_3_y * to_percent_height))

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
            print trial_config
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