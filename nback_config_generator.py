import random
import sys
import os
import re
import math
import shape_utils as su

#required for functions found online
import struct
import imghdr


# ODDBALL CONFIG GENERATOR

#things you might want to change
# other variable initializations. Should set so they can be changed/configured.
feedback = 0
practice = 1
block_pass_percent = 0
block_fb = 1
timeout = 10
total1 = total2 = total3 = timeout
onset = 5
within_pairs_difference = 3.5 # we subtract this from onset, within a pair

screen_margin = 0
number_of_angles = 18 #number of angles, should divide 360 evenly

safety_margin = 40
safety_margin_2 = 40
safety_margin_3 = 40

blake_or_simple = 0 # this sets the variable values
# 0 = blake
# 1 = simple

if(blake_or_simple == 0): # blake
    image_directory = './blake_images/'
    safety_margins = [40]
    vary_size = 0
elif(blake_or_simple == 1): # simple
    image_directory = './simple_images/'
    safety_margins = [40,45]
    vary_size = 1

#delimiter
delimiter = ","

# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else:
        num_blocks = 10
        num_trials = 36

    image_files = su.get_pngs(image_directory)

    for block in range(0,num_blocks):
        for trial_num in range(0,num_trials):
            images = []
            images.append(image_files[random.randrange(0,len(image_files))])
            if(random.randint(0,1)): # coin flip for same/different image
                # make the images the same
                images.append(images[0])
            else:
                while True:
                    image_2 = image_files[random.randrange(0,len(image_files))]
                    if images[0] != image_2:
                        images.append(image_2)
                        break


            for idx, image in enumerate(images): # for each pair
                #figure out positions
                # get image sizes
                # images are scaled to a percentage of the height, along the images' diagonal
                img_width, img_height = su.get_image_size(image_directory + image)
                img_diag = math.hypot(img_width, img_height)
                safety_margin = su.get_scaling(vary_size,safety_margins)
                img_scale = img_diag/float(safety_margin)/100*su.screen_height
                img_width /= img_scale
                img_height /= img_scale
                img_diag = float(safety_margin)/100*su.screen_height
                #print("img1scale: " + str(img_scale))
                #print("img_width: " + str(img_width) + "; img_height: " + str(img_height) + "; img_diag: " + str(img_diag))

                pos_img_x = su.get_random_x(round(img_diag))
                pos_img_y = su.get_random_y(round(img_diag))

                #convert positions into percentages (wait what this might mean overlap)
                pos_img_x = int(round(pos_img_x * float(100)/su.get_margin_width(img_diag)))
                pos_img_y = int(round(pos_img_y * float(100)/su.get_margin_height(img_diag)))

                #identifier
                trial_config = str(block+1) + delimiter
                trial_config += str(2*trial_num+1+idx) + delimiter

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
                trial_config += str(pos_img_x) + delimiter
                trial_config += str(pos_img_y) + delimiter
                trial_config += str(onset-((idx%2)*within_pairs_difference)) + delimiter
                
                #image 1
                trial_config += (image.split('.'))[0] + delimiter
                trial_config += str(number_of_angles * random.randrange(0,360/number_of_angles)) + delimiter
                trial_config += str(safety_margin) + delimiter
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
