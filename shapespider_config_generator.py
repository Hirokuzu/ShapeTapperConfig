from random import randrange
import sys
import os
import re
import math
import random
import shape_utils as su
import copy

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
timeout = 5
total1 = total2 = total3 = timeout
onset = 1
number_of_angles = 18 #number of angles, should divide 360 evenly
ask_for_target = 1



safety_margin_1 = 100. * 4.25 / su.cm_per_inch * su.dpi / su.screen_height
safety_margin_2 = 100. * 4.25 / su.cm_per_inch * su.dpi / su.screen_height
safety_margin_3 = 100. * 4.25 / su.cm_per_inch * su.dpi / su.screen_height

fixation_x = 50 # percentage
fixation_y = 50 + round(50. * 100. / float(su.screen_height)) # percentage
# the 50 is the hard coded position of the fixation in Unity, converted to a percentage

initial_x = 10 * 100 * su.dpi / su.cm_per_inch / su.screen_width # 11cm as percentage
increment_x = 2 * 100 * su.dpi / su.cm_per_inch / su.screen_width # 2cm
y_variance = 10 # also percentage
# let's calculate the final positions now
smallest_x = fixation_x + initial_x
smallest_radius = math.hypot(initial_x, y_variance)

point_1 = [smallest_x, fixation_y + y_variance]
point_2 = [point_1[0]+increment_x, point_1[1]]
point_3 = [point_1[0]+2*increment_x, point_1[1]]

point_4 = [64, fixation_y]
point_5 = [66, fixation_y]
point_6 = [68, fixation_y]

point_7 = [point_1[0], fixation_y - y_variance]
point_8 = [point_2[0], point_7[1]]
point_9 = [point_3[0], point_7[1]]
# points = [point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9] # don't judge my brain isn't working today
points = [point_4, point_5, point_6]
# points = []
# for i in range(0,3):
#     points.append([initial_x + increment_x * i, fixation_y])


# make this into a list?
# then have a set of stimuli
image_stimuli_directory = './shapespider/'
positive_images_directory = image_stimuli_directory + 'Positive/'
negative_images_directory = image_stimuli_directory + 'Negative/'
neu_neg_images_directory = image_stimuli_directory + 'neutral_negative/'
neu_pos_images_directory = image_stimuli_directory + 'neutral_positive/'

#delimiter
delimiter = ","


# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else:
        practice_blocks = 1
        practice_trials = 8 
        num_blocks = 5 # regular blocks
        # use a dictionary?
        # in GUI, check for directory, default keys folder name
        stimuli_dirs = {
            'positive': image_stimuli_directory + 'Positive/',
            'negative': image_stimuli_directory + 'Negative/',
            'neu_neg': image_stimuli_directory + 'neutral_negative/',
            'neu_pos': image_stimuli_directory +'neutral_positive/'
        }

        # match key with above
        stimuli = dict()
        stimuli_counter = dict()
        for key, value in stimuli_dirs.items():
            stimuli[key] = su.get_images(value)
            for value in stimuli[key]:
                stimuli_counter[value] = 0

        # GUI - options for trial types, positions, number of trials
        trial_types = [('neu_pos','neu_pos',False,12),
            ('neu_neg','neu_neg',False,12),
            ('neu_pos','neu_pos',True,4),
            ('neu_neg','neu_neg',True,4),
            ('neu_neg','negative',True,6),
            ('neu_pos','positive',True,6)
        ]

        num_trials = 0
        for trial_type in trial_types:
            num_trials = num_trials + trial_type[3]

        trial_probs = [trial_type[3]/float(num_trials) for trial_type in trial_types]

    total_blocks = num_blocks + practice_blocks

    # #figure out which images to use first
    # positive_images = get_images(positive_images_directory)
    # negative_images = get_images(neutral_negative)
    # neu_neg_images = get_images(neu_neg_images_directory)
    # neu_pos_images = get_imates(neu_pos_images_directory)

    jump_start = points[1]
    jump_points = list(points)
    jump_points.remove(jump_start)

    experiment_stimuli = copy.deepcopy(stimuli)
    for block in range(0,total_blocks):
        if(practice_blocks >= 1):
            block_trials = practice_trials
            #this should be a list comprehension
            # block_trial_counter = [[1]*len(points),[1]*len(points),[1]*(len(points)-1),
            # [1]*(len(points)-1),[1]*(len(points)-1),[1]*(len(points)-1)]
            block_trial_counter = [[1]*(len(points)-trial_type[2]*1) for trial_type in trial_types]
            practice_blocks = practice_blocks-1
        else:
            block_trials = num_trials
            block_trial_counter = [[trial_type[3]/(len(points)-1*trial_type[2])]*(len(points)-1*trial_type[2]) for trial_type in trial_types]


        for trial_num in range(0,block_trials):
            
            # some sort of RNG here
            rot_img_1 = number_of_angles * randrange(0,360/number_of_angles)
            trial_set = False
            while not trial_set:
                trial_type = random.choices(trial_types,trial_probs)[0]
                trial_type_idx = trial_types.index(trial_type)
                if(any(counter > 0  for counter in block_trial_counter[trial_type_idx])):
                    trial_set = True
                else:
                    continue

            # trial picked, set up images
            img_1 = random.choice(stimuli[trial_type[0]]) # to keep uniformity?
            img_2 = random.choice(experiment_stimuli[trial_type[1]])
            if trial_type_idx > 4:
                img_1 = "neu_" + img_2
            if(trial_type[2]): # jump or not
                img_1_pos = jump_start
                jump_direction = random.randint(0,len(jump_points)-1) # this really only works in this specific case. needs to be fixed
                if block_trial_counter[trial_type_idx][jump_direction] > 0:
                    img_2_pos = jump_points[jump_direction]
                    block_trial_counter[trial_type_idx][jump_direction] = block_trial_counter[trial_type_idx][jump_direction] - 1
                else:
                    img_2_pos = jump_points[len(jump_points)-1-jump_direction]
                    block_trial_counter[trial_type_idx][len(block_trial_counter[trial_type_idx])-1-jump_direction] = block_trial_counter[trial_type_idx][len(block_trial_counter[trial_type_idx])-1-jump_direction] - 1
                rot_img_2 = 0
            else: # not a jump
                img_pos = random.randint(0,len(points)-1)
                while block_trial_counter[trial_type_idx][img_pos] <= 0: # that position is maxxed, choose another one
                    img_pos = random.randint(0,len(points)-1)
                img_1_pos = img_2_pos = points[img_pos]
                rot_img_2 = rot_img_1
                block_trial_counter[trial_type_idx][img_pos] = block_trial_counter[trial_type_idx][img_pos] - 1

            # regardless, remove the "target" from the list
            stimuli_counter[img_2] = stimuli_counter[img_2] + 1
            stimuli_counter[img_1] = stimuli_counter[img_1] + 1
            experiment_stimuli[trial_type[1]].remove(img_2)
            if not experiment_stimuli[trial_type[1]]:
                experiment_stimuli[trial_type[1]] = copy.deepcopy(stimuli[trial_type[1]])

                

            # #figure out positions
            # # get image sizes
            # img_1_width, img_1_height = get_image_size(stimuli_dirs[trial_type[0]] + img_1)
            # img_1_diag = math.hypot(img_1_width, img_1_height)
            # img_1_scale = img_1_diag*su.screen_height/float(safety_margin_1)/100
            # img_1_width /= img_1_scale
            # img_1_height /= img_1_scale
            # img_1_diag = float(safety_margin_1)*su.screen_height/100
            # img_2_width, img_2_height = get_image_size(stimuli_dirs[trial_type[1]] + img_2)
            # img_2_diag = math.hypot(img_2_width, img_2_height)
            # img_2_scale = img_2_diag*su.screen_height/float(safety_margin_2)/100
            # img_2_width /= img_2_scale
            # img_2_height /= img_2_scale
            # img_2_diag = float(safety_margin_2)*su.screen_height/100

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
            trial_config += delimiter # (image_3.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * randrange(0,360/number_of_angles)) + delimiter
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
            trial_config += delimiter #su.format_string.format(pos_img_3[0]) + delimiter
            trial_config += delimiter #su.format_string.format(pos_img_3[1]) + delimiter
            trial_config += str(ask_for_target)
            print(trial_config)
        practice_blocks = max(practice_blocks-1,0)
    print(stimuli_counter) # this counts all the times each stimulus appeared as the _second_ stimulus
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