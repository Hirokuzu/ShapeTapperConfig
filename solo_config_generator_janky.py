from random import randrange
import sys
import os
import re
import math
import shape_utils as su

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
onset = 2
image_directory = './simple_images/'
screen_margin = 0
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
            image_files = su.get_pngs(image_directory)
            #image_files = get_solo_blake()
            image_1 = image_files[randrange(0,len(image_files))]
            #figure out positions
            # get image sizes
            # images are scaled to a percentage of the height, along the images' diagonal
            img_1_width, img_1_height = su.get_image_size(image_directory + image_1)
            img_1_diag = math.hypot(img_1_width, img_1_height)
            img_1_scale = img_1_diag/float(safety_margin_1)/100*su.screen_height
            img_1_width /= img_1_scale
            img_1_height /= img_1_scale
            img_1_diag = float(safety_margin_1)/100*su.screen_height
            #print("img1scale: " + str(img_1_scale))
            #print("img_1_width: " + str(img_1_width) + "; img_1_height: " + str(img_1_height) + "; img_1_diag: " + str(img_1_diag))

            pos_img_1_x = su.get_random_x(round(img_1_diag))
            pos_img_1_y = su.get_random_y(round(img_1_diag))

            #convert positions into percentages (wait what this might mean overlap)
            pos_img_1_x = int(round(pos_img_1_x * float(100)/su.get_margin_width(img_1_diag)))
            pos_img_1_y = int(round(pos_img_1_y * float(100)/su.get_margin_height(img_1_diag)))

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
            trial_config += delimiter #img 2 name
            trial_config += str(0) +delimiter
            trial_config += str(0) +delimiter
            trial_config += str(0) +delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) +delimiter # dyn_mask_flag not used
            trial_config += str(0) +delimiter
            trial_config += str(0) +delimiter # not used in oddball image_on
            trial_config += str(0) +delimiter # not used in oddball image_off

            #image 3
            trial_config += delimiter # img 3 name
            trial_config += str(0) +delimiter
            trial_config += str(0) +delimiter
            trial_config += str(0) +delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) +delimiter # dyn_mask_flag not used
            trial_config += str(0) +delimiter
            trial_config += str(0) +delimiter # not used in oddball image_on
            # no image_off for image 3

            #bonus oddball config stuff
            trial_config += str(1) + delimiter #oddball_flag
            trial_config += str(0) + delimiter
            trial_config += str(0) + delimiter
            trial_config += str(0) + delimiter
            trial_config += str(0)
            print(trial_config)
    return


if __name__ == "__main__":
    main()
