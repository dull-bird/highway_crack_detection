import cv2
import numpy as np
from scipy.signal import argrelextrema, spline_filter, order_filter, medfilt
import res_drawer
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def white2average(img):
    ret, mask = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV) #分割白色部分，置为0

    #白色部分可以膨胀一下
    #...

    mask_inv = cv2.bitwise_not(mask) #反色的mask
    res = maskCompensation(img, mask_inv)
    return res, mask_inv

def maskCompensation(img, mask):
    mask_inv = cv2.bitwise_not(mask)# 反色的mask，路标为0，其余255
    #print('mask size', mask_inv.shape)
    #print('img size', img.shape)
    img1 = cv2.bitwise_and(img, mask_inv)  # 找到非白色区域
    # 计算非白色区域的平均值
    N = np.sum(mask_inv) // 255
    S = np.sum(img1)
    avr = S//N
    # 反色mask置为该平均值
    mask2 = mask // 255 * avr
    res = cv2.add(img1, mask2)
    return res

def limit_fast(img):
    row_max, col_max = img.shape
    left_lim = 400
    right_lim = col_max - 400
    for i in range(col_max // 2, 0, -2):
        #line = medfilt(img[:, i], 11)
        if np.alen(np.where(img[:, i] > 230)[0]) > 400:
            left_lim = i
            #print('left', i)
            break

    for i in range(col_max // 2, col_max, 2):
        #line = medfilt(img[:, i], 11)
        if np.alen(np.where(img[:, i] > 230)[0]) > 400:
            right_lim = i
            #print('right', i)
            break
    return (left_lim, right_lim)

def split_x(img, imglist = None, draw = False, plot=False):
    img0 = cv2.medianBlur(img, 11)
    img1, mask = white2average(img0)
    #img1 = cv2.medianBlur(img1, 11)
    imgs = []
    #修改为使用函数limit
    (left_lim, right_lim) = limit_fast(img0)
    print(left_lim, right_lim)
    row_max, col_max = img.shape

    if imglist == None:
        sx = np.sum(img1[:, 350: img1.shape[1] - 350], 1)
        #sx = medfilt(sx, 11)

        minima_x = argrelextrema(sx, np.less_equal, order=300)
        if plot:
            plt.figure()
            plt.plot(range(row_max), sx)

            plt.plot(minima_x, [sx[i] for i in minima_x], 'r+')
            plt.show()

        imglist = []
        minima_x = np.insert(minima_x, 0, 0)
        minima_x = np.append(minima_x, row_max)

        #可以增加一项操作，如果有一个极小值点很接近原图的上下边界，则可以去除。
        for i in range(len(minima_x) - 1):
            imglist.append([minima_x[i], minima_x[i + 1]])
        imglist = remove_small_h(imglist)
        imglist = split_ajudst(imglist)
        imglist = remove_small_h(imglist)

    for i in imglist:
        imgs.append([img[i[0] + 10: i[1] - 10, 10 + left_lim: col_max//2 - 2], img[i[0] + 10: i[1] - 10, col_max//2 + 2: right_lim - 10]])
    if draw == True:
        res_drawer.split(img, (left_lim, right_lim), imglist)
    return imgs, imglist, (left_lim, right_lim)

def split_ajudst(imglist):
    delta_h = [i[1] - i[0] for i in imglist]
    #print(delta_h)
    med_h = np.median(delta_h[1: -1])
    #print(med_h)
    flag = [0] * len(delta_h)
    #print(flag)
    for index, h in enumerate(delta_h):
        if h - med_h > 40 and index != 0 and index != len(delta_h) - 1:
            flag[index] = -1
        elif h - med_h < -40 and index != 0 and index != len(delta_h) - 1:
            flag[index] = 1
    #print(flag)
    for i, f in enumerate(flag):
        if f == 1:
            d = abs(int(med_h - delta_h[i]))
            if abs(delta_h[i - 1] - med_h) <= 10 and delta_h[i + 1] > d + 50:
                imglist[i][1] += d
                imglist[i + 1][0] += d
            elif abs(delta_h[i + 1] - med_h) <= 10 and delta_h[i - 1] > d + 50:
                imglist[i - 1][1] -= d
                imglist[i][0] -= d
        elif f == -1 and flag[i - 1] != 1 and flag[i + 1] != 1:
            d = abs(int(med_h - delta_h[i]))
            if abs(delta_h[i - 1] - med_h) <= 10 and delta_h[i] > d + 50:
                imglist[i][1] -= d
                imglist[i + 1][0] -= d
            elif abs(delta_h[i + 1] - med_h) <= 10 and delta_h[i] > d + 50:
                imglist[i - 1][1] += d
                imglist[i][0] += d
        delta_h = [i[1] - i[0] for i in imglist]
    #print(delta_h)
    return imglist

def remove_small_h(imglist):
    for i in imglist:
        if i[1] - i[0] <= 50:
            imglist.remove(i)
    return imglist