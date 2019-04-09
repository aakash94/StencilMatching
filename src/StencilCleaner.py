import cv2
import glob
import numpy as np
from pathlib import Path

'''
use this script to easily clean a Black&White stencil.
ip should be 4 channel b&w image
removes all the edge pixels
usually edges show most difference
'''

threshold_val = 128
stencil_path = "path/to/stencil/input.png"
op_path = "path/to/stencil/output.png"

kernel = np.array([[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]])

ones = kernel.sum().sum()
kernel = kernel / ones

if Path(stencil_path).is_file():
    stencil = cv2.imread(stencil_path, cv2.IMREAD_UNCHANGED)

b, g, r, a = cv2.split(stencil)
bgr_img = cv2.merge((b, g, r))
gs_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gs_img, threshold_val, 255, cv2.THRESH_BINARY)

convoluted = cv2.filter2D(thresh, -1, kernel)
alpha = cv2.inRange(convoluted, 1, 254)
alpha = 255 - alpha
alpha_image = cv2.merge((b, g, r, alpha)).astype(np.uint8)

cv2.imwrite(op_path, alpha_image)
