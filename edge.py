import skimage.feature as feature
import cv2
from skimage.filters import sobel, gabor
from skimage.filters.rank import mean_bilateral
from skimage.restoration import denoise_bilateral
import matplotlib.pyplot as plt
from skimage.morphology import disk
import numpy as np
import res_drawer

def Canny(image, draw=False):
    edge = feature.canny(image, sigma=3, use_quantiles=False, low_threshold=5, high_threshold=25)
    if draw == True:
        res_drawer.binary(image, edge)
    return edge


if __name__ =="__main__":
    img = cv2.imread('E:\\File\\python\\proj2\\pic\\small1.jpg', 0)
    #img = denoise_bilateral(img, win_size=10, multichannel=False)
    g = gabor(img, 50)

    img = mean_bilateral(img, disk(25))
    d1 = sobel(img)


    img1 = feature.canny(img, sigma=3, use_quantiles=False, low_threshold=20, high_threshold=40)
    plt.imshow(img1, cmap=plt.cm.gray)
    plt.show()