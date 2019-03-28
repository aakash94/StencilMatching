from pathlib import Path

import cv2
import numpy as np

'''
use this script to easily compare a stencil and an image


stencil = 4 channel alpha image
image   = 3 channel normal image

stencil_path = path of stencil
image_path   = path of image to be checked against

This implementation does a threshold of 128 and works on bw stencils
Works fine if stencils created using StencilCreate.py

'''

threshold_val = 128

image_path = "/path/to/image.png"
stencil_path = "/path/to/stencil.png"


def get_bw_image(image_path):
    # remove all pixels from alpha_image that is different in image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if len(img.shape) == 2:
        print("Image already greyscale")
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    elif img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, threshold_val, 255, cv2.THRESH_BINARY)
    return thresh


def image_compare(alpha_image, image):
    # parts of this implementation are inspired from:
    # https://www.learnopencv.com/alpha-blending-using-opencv-cpp-python/

    # alpha_image should have 4 channels
    if alpha_image.shape[2] != 4:
        print("alpha channel image does not have 4 channels")
        print("delete stencil and try again")
        exit()

    # image should be greyscale images
    if len(image.shape) != 2:
        print("Image not greyscale")
        exit()

    reference_image = image.copy()

    b, g, r, a = cv2.split(alpha_image)
    stencil_img = cv2.merge((b, g, r))
    stencil_img = cv2.cvtColor(stencil_img, cv2.COLOR_BGR2GRAY)

    # get 1.0 binary values for alpha channel
    a = a.astype(float) / 255
    # a = cv2.merge((a,a,a))

    foreground = stencil_img.astype(float)
    background = image.astype(float)

    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(a, foreground)

    # Multiply the background with ( 1 - alpha )
    background = cv2.multiply(1.0 - a, background)

    # Add the masked foreground and background.
    image = cv2.add(foreground, background)
    image = image.astype(np.uint8)

    # Check if reconstructed and original images are same
    # can use better logic to do so
    difference = cv2.subtract(reference_image, image)
    if cv2.countNonZero(difference) == 0:
        return True
    else:
        return False


if Path(stencil_path).is_file():
    stencil = cv2.imread(stencil_path, cv2.IMREAD_UNCHANGED)
else:
    print("Stencil not Found")
    exit()

if Path(image_path).is_file():
    img = get_bw_image(image_path)
else:
    print("Stencil not Found")
    exit()

if image_compare(alpha_image=stencil, image=img):
    print("Match")
else:
    print("No Match")
