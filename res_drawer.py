import cv2
import matplotlib.pyplot as plt

def split(image, limits, imglist):
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    cv2.rectangle(image, (limits[0], 0), (limits[1], image.shape[0]), (0,255,0), 15)

    for sub in imglist:
        cv2.rectangle(image, (limits[0] +8, sub[0]), (image.shape[1]//2 - 2, sub[1]), (255, 0, 255), 10)
        cv2.rectangle(image, (image.shape[1]//2 + 2, sub[0]), (limits[1] - 8, sub[1]), (255, 0, 255), 10)
    plt.figure(1)
    plt.imshow(image)
    plt.show()
    cv2.imwrite('split.png', image)

def binary(image, binary):
    #cv2.imshow('blur', image)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    ax1.imshow(image, cmap="gray", vmin=0, vmax=255)
    ax2.imshow(binary, cmap="gray")

    fig.tight_layout()
    plt.show()

def binary_single(binary):
    plt.figure(1)
    plt.imshow(binary, cmap="gray")
    plt.show()

def gray_single(image):
    plt.figure(1)
    plt.imshow(image, cmap="gray", vmin=0, vmax=255)
    plt.show()