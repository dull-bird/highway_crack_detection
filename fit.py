import numpy as np
import scipy.linalg
import cv2
from skimage.morphology import disk, binary_erosion, binary_closing, binary_opening
from skimage.filters import threshold_yen, threshold_triangle, threshold_isodata, try_all_threshold, gaussian
from skimage.filters.rank import mean_bilateral, median
import res_drawer
import matplotlib.pyplot as plt


def fit2d(image, delete_mask=None):
    #image = cv2.medianBlur(image, 7)
    rows, cols = image.shape
    #生成图像3d点序列
    xv, yv = np.meshgrid(np.arange(0, cols), np.arange(0, rows))
    xv = xv.flatten()
    yv = yv.flatten()
    data = np.c_[np.transpose(yv), np.transpose(xv), image.flatten()]
    #print(data)
    #print(data.shape)
    #删去疑似裂纹的点
    if delete_mask is not None:
        delete_mask += get_extreme_mask(image)
    else:
        delete_mask = get_extreme_mask(image)
    #res_drawer.binary(image, delete_mask)
    delete_mask_flatten = delete_mask.flatten()
    delete_idx = np.where(delete_mask_flatten != 0)
    data = np.delete(data, delete_idx, 0)
    #delte_idx = np.where(image.flatten() < 50)
    #data = np.delete(data, delte_idx, 0)
    #print(data.shape)
    #print(data)

    #对data采样，适当减少计算量
    #rand = np.random.randint(0, data.shape[0], 19 * data.shape[0]//20)
    #rand1 = np.random.randint(0, data.shape[0], data.shape[0] // 5)
    #print('减少了', len(rand))
    #data = data[rand1]
    #print(data.shape)

    # regular grid covering the domain of the data
    X,Y = np.meshgrid(np.arange(0, rows), np.arange(0, cols))
    XX = X.flatten()
    YY = Y.flatten()

    # best-fit quadratic curve
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])

    # evaluate it on a grid
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)
    return np.transpose(Z)


def get_extreme_mask(image):
    mask = image >= 210
    return mask

def adjust_extreme(image, delta):
    mask = (image < 230).astype(np.uint8)
    mask = binary_erosion(mask, disk(1))

    #print(mask)
    out = mask * delta
    #out = median(image, selem=disk(5))
    return out

def fit_partitions(image, delete_mask=None):
    #image = cv2.medianBlur(image, 7)

    rows, cols = image.shape
    #print(rows, cols)
    row_half = rows//2
    col_half = cols//2
    images = [image[0: row_half, 0: col_half],
              image[0: row_half, col_half: cols],
              image[row_half: rows, 0: col_half],
              image[row_half: rows, col_half: cols]]
    if delete_mask is not None:
        masks = [delete_mask[0: row_half, 0: col_half],
                 delete_mask[0: row_half, col_half: cols],
                 delete_mask[row_half: rows, 0: col_half],
                 delete_mask[row_half: rows, col_half: cols]]
    #对每一部分分别进行拟合

        zs = [fit2d(img, masks[idx]) for idx, img in enumerate(images)]
    else:
        zs = [fit2d(i) for i in images]
    #对拟合结果进行合并
    z1 = np.hstack((zs[0], zs[1]))
    z2 = np.hstack((zs[2], zs[3]))
    z = np.vstack((z1, z2))
    return z



def cal_delta_abs(image, z):
    delta = image - z
    delta = adjust_extreme(image, delta)
    balance = (300 + delta).astype(np.uint16)
    #cv2.imwrite('127.jpg' ,(127 + delta).astype(np.uint8))
    #cv2.imshow('balance', balance)
    #blur = gaussian(balance, 1).astype(np.uint8)
    #g_kernel = cv2.getGaussianKernel(5, 1)
    #blur = cv2.filter2D(balance, 0, g_kernel)
    #blur = cv2.medianBlur(balance, 11)

    blur = median(balance, selem=disk(7))
    blur = mean_bilateral(blur, disk(13))
    abs = np.abs(blur - 300.0).astype(np.uint8)
    #cv2.imshow('abs', abs)
    #cv2.waitKey()
    return abs


