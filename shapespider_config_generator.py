from random import randrange
import sys
import os
import re
import math
import random

#required for functions found online
import struct
import imghdr


# ODDBALL CONFIG GENERATOR
# uses blake shapes only.

#things you might want to change
# other variable initializations. Should set so they can be changed/configured.
feedback = 0
practice = 0
block_pass_percent = 0
block_fb = 0
timeout = 5
total1 = total2 = total3 = timeout
onset = 1
blake_directory = './Assets/Resources/Images/'
screen_width = 1920
screen_height = 1080
ppi = 96 # screen specific
number_of_angles = 18 #number of angles, should divide 360 evenly

safety_margin_1 = int(round(100 * 3 / 2.54 * ppi / screen_height))
safety_margin_2 = int(round(100 * 3 / 2.54 * ppi / screen_height))
safety_margin_3 = int(round(100 * 3 / 2.54 * ppi / screen_height))

fixation_x = screen_width / 2.0;
fixation_y = screen_height / 2.0 + 50;

initial_x = 35 # this is a percentage of the distance from fixation to the far corner
increment_x = 10 # also a percentage
y_variance = 10 * screen_height / 100# also percentage
# let's calculate the final positions now
radius = math.hypot(screen_width-fixation_x,screen_height-fixation_y) # not sure if i need this actually
smallest_x = fixation_x + initial_x * (screen_width-fixation_x) / 100
smallest_radius = math.hypot(smallest_x - fixation_x, y_variance)
increment_x *= screen_width / 100
point_1 = [smallest_x, fixation_y + y_variance]
point_2 = [point_1[0]+increment_x, point_1[1]]
point_3 = [point_1[0]+2*increment_x, point_1[1]]

point_4 = [fixation_x + smallest_radius, fixation_y]
point_5 = [fixation_x + math.hypot(fixation_x - point_2[0],fixation_y - point_2[1]), fixation_y]
point_6 = [fixation_x + math.hypot(fixation_x - point_3[0],fixation_y - point_3[1]), fixation_y]

point_7 = [point_1[0], fixation_y - y_variance]
point_8 = [point_2[0], point_7[1]]
point_9 = [point_3[0], point_7[1]]

points = [point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8, point_9] # don't judge my brain isn't working today

image_stimuli_directory = './shapespider/Image Stimuli/'
food_directory = image_stimuli_directory + 'Positive/Food/'
flower_directory = image_stimuli_directory + 'Positive/Flowers/'
toys_directory = image_stimuli_directory + 'Positive/Toys/'
spider_directory = image_stimuli_directory + 'Negative/Spiders/'
flying_insects_directory = image_stimuli_directory + 'Negative/Flying Insects/'
bugs_beetles_directory = image_stimuli_directory + 'Negative/Bugs & Beetles/'

# define number of blocks, trials per block
num_blocks = 10
num_trials = 4

#delimiter
delimiter = ","


# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else:
        num_blocks = 10
        num_trials = 4

    for block in range(0,num_blocks):
        for trial_num in range(0,num_trials):
            #figure out which images to use first
            food_images = get_images(food_directory)
            flower_images = get_images(flower_directory)
            toys_images = get_images(toys_directory)
            spider_images = get_images(spider_directory)
            flying_insects = get_images(flying_insects_directory)
            bugs_beetles = get_images(bugs_beetles_directory)

            # some sort of RNG here
            if(random.random()<0.5): # positive or negative images
                image_1 = toys_images[randrange(0,len(toys_images))]
                img_1_directory = toys_directory
            else:
                image_1 = flower_images[randrange(0,len(flower_images))]
                img_1_directory = flower_directory
            if(random.random()<0.5): # keep the same image
                image_2 = image_1
                img_2_directory = img_1_directory
            else:
                # another random number generator
                "Who let the dogs out"
                image_2 = food_images[randrange(0,len(food_images))]
                img_2_directory = food_directory




            #figure out positions
            # get image sizes
            img_1_width, img_1_height = get_image_size(img_1_directory + image_1)
            img_2_width, img_2_height = get_image_size(img_2_directory + image_2)

            pos_img_1 = points[randrange(0,len(points))] # select a point for image 1
            if(random.random() < 0.5): # chance of it being a different image
                pos_img_2 = pos_img_1
            else:
                while True:
                    pos_img_2 = points[randrange(0,len(points))]
                    if pos_img_2 != pos_img_1:
                        break

            #convert positions into percentages (wait what this might mean overlap)
            to_percent_width = float(100)/screen_width
            to_percent_height = float(100)/screen_height
            pos_img_1_x = int(round(pos_img_1[0] * to_percent_width))
            pos_img_1_y = int(round(pos_img_1[1] * to_percent_height))
            pos_img_2_x = int(round(pos_img_2[0] * to_percent_width))
            pos_img_2_y = int(round(pos_img_2[1] * to_percent_height))

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
            trial_config += str(pos_img_2_x) + delimiter
            trial_config += str(pos_img_2_y) + delimiter
            trial_config += delimiter #str(pos_img_3_x) + delimiter
            trial_config += delimiter #str(pos_img_3_y)
            trial_config += str(1)
            print trial_config
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