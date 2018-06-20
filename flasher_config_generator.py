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
practice_trials = 8
block_pass_percent = 0
block_fb = 0
timeout = 1
total1 = total2 = total3 = timeout
onset = 1
number_of_angles = 18 #number of angles, should divide 360 evenly
ask_for_target = 1

size_to_scale = 6.226744186046511627906976744186

safety_margin_1 = 100. * 6.22674 / su.cm_per_inch * su.dpi / su.screen_height
safety_margin_2 = 100. * 6.22674 / su.cm_per_inch * su.dpi / su.screen_height
safety_margin_3 = 100. * 6.22674 / su.cm_per_inch * su.dpi / su.screen_height

fixation_x = 50 # percentage
fixation_y = 50 + round(50. * 100. / float(su.screen_height)) # percentage
# the 50 is the hard coded position of the fixation in Unity, converted to a percentage

initial_x = 10 * 100 * su.dpi / su.cm_per_inch / su.screen_width # 11cm as percentage
increment_x = 2 * 100 * su.dpi / su.cm_per_inch / su.screen_width # 2cm
y_variance = 10 # also percentage
# let's calculate the final positions now
smallest_x = fixation_x + initial_x
smallest_radius = math.hypot(initial_x, y_variance)


# make this into a list?
# then have a set of stimuli
image_stimuli_directory = './shapespider/'
positive_images_directory = image_stimuli_directory + 'Positive/'
negative_images_directory = image_stimuli_directory + 'Negative/'
neu_neg_images_directory = image_stimuli_directory + 'neutral_negative/'
neu_pos_images_directory = image_stimuli_directory + 'neutral_positive/'

# Fixation for the flash experiment
square_diamond_pair = ['diamond','square']
triangle_pair = ['rtriangle','ltriangle']
flash_points = [[[68.77,30.48],[71.42,50],[68.80,69.47]], # 40%
                [[78.76,30],[80.57,50],[78.78,69.94]], # 60%
                [[88.35,29.90],[89.81,50],[88.43,69.89]]] # 80%
eccentricities = [40,60,80]
square_mask = "square_mask"
diamond_mask = "diamond_mask"


#delimiter
delimiter = ","


# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else:
        practice_blocks = 1
        practice_trials = 24
        num_blocks = 7 # regular blocks

        # GUI - options for trial types, positions, number of trials
        trial_types = [(triangle_pair[0],triangle_pair[1],0,3,square_mask),
                    (triangle_pair[0],triangle_pair[1],1,3,square_mask),
                    (triangle_pair[0],triangle_pair[1],2,3,square_mask),
                    (triangle_pair[1],triangle_pair[0],0,3,square_mask),
                    (triangle_pair[1],triangle_pair[0],1,3,square_mask),
                    (triangle_pair[1],triangle_pair[0],2,3,square_mask),
                    (square_diamond_pair[0],square_diamond_pair[1],0,3,square_mask),
                    (square_diamond_pair[0],square_diamond_pair[1],1,3,square_mask),
                    (square_diamond_pair[0],square_diamond_pair[1],2,3,square_mask),
                    (square_diamond_pair[1],square_diamond_pair[0],0,3,square_mask),
                    (square_diamond_pair[1],square_diamond_pair[0],1,3,square_mask),
                    (square_diamond_pair[1],square_diamond_pair[0],2,3,square_mask),
                    (triangle_pair[0],triangle_pair[1],0,3,diamond_mask),
                    (triangle_pair[0],triangle_pair[1],1,3,diamond_mask),
                    (triangle_pair[0],triangle_pair[1],2,3,diamond_mask),
                    (triangle_pair[1],triangle_pair[0],0,3,diamond_mask),
                    (triangle_pair[1],triangle_pair[0],1,3,diamond_mask),
                    (triangle_pair[1],triangle_pair[0],2,3,diamond_mask),
                    (square_diamond_pair[0],square_diamond_pair[1],0,3,diamond_mask),
                    (square_diamond_pair[0],square_diamond_pair[1],1,3,diamond_mask),
                    (square_diamond_pair[0],square_diamond_pair[1],2,3,diamond_mask),
                    (square_diamond_pair[1],square_diamond_pair[0],0,3,diamond_mask),
                    (square_diamond_pair[1],square_diamond_pair[0],1,3,diamond_mask),
                    (square_diamond_pair[1],square_diamond_pair[0],2,3,diamond_mask)
                ]

        num_trials = 0
        for trial_type in trial_types:
            num_trials = num_trials + trial_type[3]

        trial_probs = [trial_type[3]/float(num_trials) for trial_type in trial_types]

    total_blocks = num_blocks + practice_blocks

    for block in range(0,total_blocks):
        if(practice_blocks >= 1):
            block_trials = practice_trials//2
            block_trial_counter = [[1]]*practice_trials
            practice_blocks = practice_blocks-1
        else:
            block_trials = num_trials
            block_trial_counter = []
            for trial_type in trial_types:
                block_trial_counter.append([trial_type[3]/3]*3)
        
        for trial_num in range(0,block_trials):
            
            # some sort of RNG here
            rot_img_1, rot_img_2, rot_img_3 = 0, 0, 0
            trial_set = False
            while not trial_set:
                trial_type = random.choices(trial_types,trial_probs)[0]
                trial_type_idx = trial_types.index(trial_type)
                if(any(counter > 0  for counter in block_trial_counter[trial_type_idx])):
                    trial_set = True
                else:
                    continue

            # trial picked, set up images
            img_1 = trial_type[0]
            img_2 = trial_type[1]
            img_3 = trial_type[1]
            
            # chose a position at random
            trial_points = list(flash_points[trial_type[2]])
            img_1_pos = random.choice(trial_points)
            trial_points.remove(img_1_pos)
            img_2_pos = random.choice(trial_points)
            trial_points.remove(img_2_pos)
            img_3_pos = random.choice(trial_points)
            # positions have been determined.

            mask = trial_type[4]

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
            trial_config += su.format_string.format(img_1_pos[0]) + delimiter # position of the first image
            trial_config += su.format_string.format(img_1_pos[1]) + delimiter # position of the second image
            trial_config += str(onset) + delimiter # how long before the first image should appear
            
            #image 1
            trial_config += (img_1.split('.'))[0] + delimiter
            trial_config += str(rot_img_1) + delimiter
            trial_config += su.format_string.format(safety_margin_1) + delimiter
            trial_config += str(1) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 2
            trial_config += (img_2.split('.'))[0] + delimiter
            trial_config += str(rot_img_2) + delimiter
            trial_config += su.format_string.format(safety_margin_2) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 3
            trial_config += (img_3.split('.'))[0] + delimiter
            trial_config += str(rot_img_3) + delimiter
            trial_config += su.format_string.format(safety_margin_3) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            # no image_off for image 3

            #bonus oddball config stuff
            trial_config += str(1) + delimiter #oddball_flag
            trial_config += su.format_string.format(img_2_pos[0]) + delimiter
            trial_config += su.format_string.format(img_2_pos[1]) + delimiter
            trial_config += su.format_string.format(img_3_pos[0]) + delimiter
            trial_config += su.format_string.format(img_3_pos[1]) + delimiter
            trial_config += str(ask_for_target) + delimiter
            trial_config += mask + delimiter
            trial_config += "0.5"
            print(trial_config)
        practice_blocks = max(practice_blocks-1,0)
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