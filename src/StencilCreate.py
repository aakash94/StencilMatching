import cv2
import numpy as np
import glob
from pathlib import Path

'''
use this script to easily generate a stencil that fits a given set of images.

Place all images in the 'folder_path'
Stencils if any should be in the 'folder_path'
out put is an update stencil in the stencil_path
If stencil_path exists it will be updated.
Else it will be created.
All inputs and outputs are in png.

# This implementation thresholds the images, and creates a b&w stencil
# That part can be easily removed if required

***WARNING***
# Be smart in feeding images. 
# Keep backup of stencil.
# Don't add images that will break the stencil.
# (eg. image and its inverted form. There will be no overlap.)

'''

threshold_val = 128
folder_path  = "/path/to/class/images/*.png"
stencil_path = "/path/to/stencil/stencil.png"

#The source folder should have all the coloured pngs.
def get_bw_image(image_path):
    #remove all pixels from alpha_image that is different in image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if(img.shape[2] == 4):
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    elif(img.shape[2] == 3):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img , threshold_val, 255, cv2.THRESH_BINARY)
    return thresh

def image_merge(alpha_image, image):
    #remove all pixels from alpha_image that is different in image

    #alpha_image should have 4 channels
    if (alpha_image.shape[2] != 4):
        print("alpha channel image does not have 4 channels")
        print("delete stencil and try again")
        exit()

    #image should be greyscale images
    if (len(image.shape) != 2):
        print("Image not greyscale")
        exit()

    b, g, r, a = cv2.split(alpha_image)
    img = cv2.merge((b, g, r))
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    same = grey
    cv2.compare(grey, image, cv2.CMP_EQ, same)

    max_val = same.max()

    max_val = 1 if max_val == 0 else max_val
    same = same/max_val


    max_val = a.max()
    max_val = 1 if max_val == 0 else max_val
    a = a / max_val

    a = np.multiply(a, same)
    b = np.multiply(b, a)
    g = np.multiply(g, a)
    r = np.multiply(r, a)
    a = a*255

    #convert float values in alpha to unsigned int
    alpha_image = cv2.merge((b, g, r, a)).astype(np.uint8)


    return alpha_image

file_list = glob.glob(folder_path)

if(len(file_list) == 0):
    print("No file to read from")
    exit()

if Path(stencil_path).is_file():
    base = cv2.imread(stencil_path, cv2.IMREAD_UNCHANGED)
else:
    base = get_bw_image(file_list[0])
    base = cv2.cvtColor(base, cv2.COLOR_GRAY2BGRA)

if(base.shape == 3):
    base = cv2.cvtColor(base, cv2.COLOR_BGR2BGRA)

for file_path in file_list:
    print(file_path)
    img = get_bw_image(file_path)
    base = image_merge(base, img)

cv2.imwrite(stencil_path, base)