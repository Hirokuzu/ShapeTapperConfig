from random import randrange
import sys
import os
import re
import math
import random
import shape_utils as su

#required for functions found online
import struct
import imghdr


# ShapeSpider CONFIG GENERATOR

#things you might want to change
# other variable initializations. Should set so they can be changed/configured.
feedback = 0
practice_blocks = 1
practice_trials = 10
block_pass_percent = 0
block_fb = 0
timeout = 5
total1 = total2 = total3 = timeout
onset = 1
number_of_angles = 18 #number of angles, should divide 360 evenly
ask_for_target = 1

cm_per_inch = 2.54

safety_margin_1 = int(round(100 * 4.25 / cm_per_inch * su.dpi / su.screen_height))
safety_margin_2 = int(round(100 * 4.25 / cm_per_inch * su.dpi / su.screen_height))
safety_margin_3 = int(round(100 * 4.25 / cm_per_inch * su.dpi / su.screen_height))

fixation_x = 50 # percentage
fixation_y = 50 + int(round(50 * 100 / su.screen_height)) # percentage
# the 50 is the hard coded position of the fixation in Unity, converted to a percentage

initial_x = int(round(10 * 100 * su.dpi / cm_per_inch / su.screen_width)) # 11cm as percentage
increment_x = int(round(2 * 100 * su.dpi / cm_per_inch / su.screen_width)) # 2cm
y_variance = 10 # also percentage
# let's calculate the final positions now
smallest_x = fixation_x + initial_x
smallest_radius = math.hypot(initial_x, y_variance)

point_1 = [smallest_x, fixation_y + y_variance]
point_2 = [point_1[0]+increment_x, point_1[1]]
point_3 = [point_1[0]+2*increment_x, point_1[1]]

point_4 = [int(round(fixation_x + smallest_radius)), fixation_y]
point_5 = [int(round(fixation_x + math.hypot(fixation_x - point_2[0],fixation_y - point_2[1]))), fixation_y]
point_6 = [int(round(fixation_x + math.hypot(fixation_x - point_3[0],fixation_y - point_3[1]))), fixation_y]

point_7 = [point_1[0], fixation_y - y_variance]
point_8 = [point_2[0], point_7[1]]
point_9 = [point_3[0], point_7[1]]
# points = [point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9] # don't judge my brain isn't working today
points = [point_4, point_5, point_6]
# points = []
# for i in range(0,3):
#     points.append([initial_x + increment_x * i, fixation_y])

image_stimuli_directory = './shapespider/'
positive_images_directory = image_stimuli_directory + 'Positive/'
neutral_images_directory = image_stimuli_directory + 'Neutral_grayed_scaled/'
negative_images_directory = image_stimuli_directory + 'Negative/'


#delimiter
delimiter = ","


# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else:
        num_blocks = 4
        num_trials = 50
        practice_blocks = 1
        practice_trials = 10

    total_blocks = num_blocks + practice_blocks

    #figure out which images to use first
    positive_images = get_images(positive_images_directory)
    negative_images = get_images(negative_images_directory)
    neutral_images = get_images(neutral_images_directory)

    jump_start = points[1]
    jump_points = list(points)
    jump_points.remove(jump_start)

    for block in range(0,total_blocks):
        if(practice_blocks >= 1):
            block_trials = practice_trials
        else:
            block_trials = num_trials

        neutral_trials = int(block_trials * 0.6)
        neutral_jump = int(block_trials * 0.2)
        neutral_pos = int(block_trials * 0.1)
        neutral_neg = int(block_trials * 0.1)
        for trial_num in range(0,block_trials):
            
            # image 1 always neutral
            image_1 = neutral_images[randrange(0,len(neutral_images))]
            img_1_directory = neutral_images_directory
            # some sort of RNG here
            trial_set = False
            rot_img_1 = number_of_angles * randrange(0,360/number_of_angles)
            while not trial_set:
                trial_probability = random.random()
                if(trial_probability<0.6): # neutral neutral, no jump
                    if neutral_trials <= 0:
                        continue
                    else:
                        neutral_trials-=1
                        jump = False
                        image_2 = neutral_images[randrange(0,len(neutral_images))]
                        img_2_directory = neutral_images_directory
                        trial_set = True
                        if(image_2 == image_1):
                            rot_img_2 = rot_img_1
                        else:
                            rot_img_2 = number_of_angles * randrange(0,360/number_of_angles)
                elif(trial_probability < 0.8): # Neutral Neutral, jump
                    if neutral_jump <= 0:
                        continue
                    else:
                        neutral_jump-=1
                        jump = True
                        image_2 = neutral_images[randrange(0,len(neutral_images))]
                        img_2_directory = neutral_images_directory
                        trial_set = True
                        rot_img_2 = number_of_angles * randrange(0,360/number_of_angles)
                elif(trial_probability < 0.9): # Neutral Positive, jump
                    if neutral_pos <= 0:
                        continue
                    else:
                        neutral_pos-=1
                        jump = True
                        image_2 = positive_images[randrange(0,len(positive_images))]
                        img_2_directory = positive_images_directory
                        trial_set = True
                        rot_img_2 = 0 
                else: # neutral negative, jump
                    # another random number generator
                    if neutral_neg <= 0:
                        continue
                    else:
                        neutral_neg-=1
                        jump = True
                        image_2 = negative_images[randrange(0,len(negative_images))]
                        img_2_directory = negative_images_directory
                        trial_set = True
                        rot_img_2 = 0




            #figure out positions
            # get image sizes
            img_1_width, img_1_height = get_image_size(img_1_directory + image_1)
            img_1_diag = math.hypot(img_1_width, img_1_height)
            img_1_scale = img_1_diag*su.screen_height/float(safety_margin_1)/100
            img_1_width /= img_1_scale
            img_1_height /= img_1_scale
            img_1_diag = float(safety_margin_1)*su.screen_height/100
            img_2_width, img_2_height = get_image_size(img_2_directory + image_2)
            img_2_diag = math.hypot(img_2_width, img_2_height)
            img_2_scale = img_2_diag*su.screen_height/float(safety_margin_2)/100
            img_2_width /= img_2_scale
            img_2_height /= img_2_scale
            img_2_diag = float(safety_margin_2)*su.screen_height/100

            
            if(jump != 1): # chance of it being a different image
                pos_img_1 = pos_img_2 = points[randrange(0,len(points))] # select a point for image 1
                # rotation should match also
            else:
                pos_img_1 = jump_start # select a point for image 1
                pos_img_2 = jump_points[randrange(0,len(jump_points))]

            #identifier
            trial_config = str(block+1) + delimiter
            trial_config += str(trial_num+1) + delimiter

            #trial specific
            trial_config += str(feedback) + delimiter

            #block level stuff
            trial_config += str(min(practice_blocks,1)) + delimiter
            trial_config += str(block_pass_percent) + delimiter
            trial_config += str(block_fb) + delimiter

            #trial-specific stuff
            trial_config += str(timeout) + delimiter
            trial_config += delimiter # what to show if the person responded too slowly
            trial_config += delimiter * 5 # janky stuff to skip dynamic masks - not used in oddball
            trial_config += str(1) + delimiter # this is number of replays of trial within timeout, but again, not used here
            trial_config += str(pos_img_1[0]) + delimiter # position of the first image
            trial_config += str(pos_img_1[1]) + delimiter # position of the second image
            trial_config += str(onset) + delimiter # how long before the first image should appear
            
            #image 1
            trial_config += (image_1.split('.'))[0] + delimiter
            trial_config += str(rot_img_1) + delimiter
            trial_config += str(safety_margin_1) + delimiter
            trial_config += str(1) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 2
            trial_config += (image_2.split('.'))[0] + delimiter
            trial_config += str(rot_img_2) + delimiter
            trial_config += str(safety_margin_2) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 3
            trial_config += delimiter # (image_3.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * randrange(0,360/number_of_angles)) + delimiter
            trial_config += str(safety_margin_3) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            # no image_off for image 3

            #bonus oddball config stuff
            trial_config += str(1) + delimiter #oddball_flag
            trial_config += str(pos_img_2[0]) + delimiter
            trial_config += str(pos_img_2[1]) + delimiter
            trial_config += delimiter #str(pos_img_3_x) + delimiter
            trial_config += delimiter #str(pos_img_3_y)
            trial_config += str(ask_for_target)
            print trial_config
        practice_blocks = max(practice_blocks-1,0)
    return


# gets all files with names matching the expression '^blake_[0-9]*.png$' (nothing before, nothing after.)
def get_blake_imgs(directory):
    return [x for x in os.listdir(directory) if re.match('^blake_[0-9]*.png$', x)]

def get_images(directory):
    return [x for x in os.listdir(directory) if re.match('.*\.png$', x)]

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