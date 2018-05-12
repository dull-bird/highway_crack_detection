import res_drawer
import numpy as np
import cv2
from skimage.morphology import disk, binary_erosion, binary_closing, binary_opening, remove_small_holes
from skimage.filters import threshold_yen, thresholding
from skimage.filters import thresholding
from skimage.filters.rank import mean_bilateral
import res_drawer


def mean_anchor(image, anchor):
    up = np.percentile(image, 75)
    down = np.percentile(image, 50)
    #print(up, down)
    weights = np.where((up >= image) & (image >= down), 1, 0)
    #print(weights)
    mean = np.average(image, weights=weights)
    #print(mean)
    k = np.min((anchor / mean, 1.6))
    return (k * image).astype(np.uint8)


def thr_abs(abs, draw=False):
    #thr = threshold_yen(abs)
    #thr = np.min((np.max((thr, 20)), 30))
    #print(thr)
    #print(thr)
    '''
    thr = 25
    binary = abs > thr
    '''
    binary = thresholding.apply_hysteresis_threshold(abs, 24, 25)

    #binary = morEx(abs, binary, draw=False)
    if draw == True:
        res_drawer.binary(abs, binary)
    return binary

def morEx(binary, draw=False):
    binary = binary_opening(binary, disk(2))
    binary = binary_closing(binary, disk(7))
    return binary

def hole(binary, draw=False):
    out = remove_small_holes(binary, min_size=300)
    out = morEx(out)
    if draw == True:
        res_drawer.binary_single(out)
    return out
