import cv2
import numpy as np
import split
import fit
import region
import edge
import classifier
import res_drawer
import os
import edge
import statistic
import skimage.io as io
import warnings
from  skimage.filters import try_all_threshold

class pic_result():
    flags_vertical = None
    flags_horizon = None
    flags_bulk = None
    shining_a = None
    flag_not_sure = 0


def sub_handler(sub_image, name):
    sub_image = cv2.resize(sub_image, (sub_image.shape[1] // 2, sub_image.shape[0] // 2))
    #cv2.imwrite('sub.jpg', sub_image)
    # print('---------------')
    z = fit.fit_partitions(sub_image)

    abs = fit.cal_delta_abs(sub_image, z)

    abs = region.mean_anchor(abs, 5.5)
    # cv2.imwrite('sub.jpg', sub_image)
    #cv2.imwrite('.jpg', z)
    # cv2.imwrite('abs.jpg', abs)


    # bi_once = region.thr_abs(abs, draw=0)
    # io.imsave('bi_1.jpg', bi_once * 255)

    delete_mask = abs > 20
    z = fit.fit_partitions(sub_image, delete_mask)

    abs = fit.cal_delta_abs(sub_image, z)

    # z1 = fit.fit2d(abs, delete_mask=delete_mask)
    # abs = np.abs(abs - z1).astype(np.uint8)
    abs = region.mean_anchor(abs, 5.5)
    #cv2.imwrite('abs.jpg', abs)

    bi_region = region.thr_abs(abs, draw=0)

    bi_edge = edge.Canny(abs, draw=0)
    bi = bi_region | bi_edge
    bi = region.hole(bi, draw=0)

    #io.imsave('binary_r.jpg', bi_region * 255)
    #try_all_threshold(abs)

    # bi_shining = region.shining(sub_image, z, bi)
    # print(np.sum(bi_shining))
    # res_drawer.binary_single(bi_shining)
    flags = classifier.classifier(bi, name)
    return flags


def pic_handler(dir, name):
    flags = pic_result()
    if '.jpg' not in name:
        name = name + '.jpg'
    print(name)
    image = cv2.imread(dir + name, 0)
    if type(image) != np.ndarray:
        flags.flag_not_sure = 1
        return flags
    # image = cv2.resize(image, (1242, 3010))
    images2d, img_list, limits = split.split_x(image, draw=0, plot=0)

    if images2d[0][0].shape[1] < 400 or images2d[0][1].shape[1] < 400:
        flags.flag_not_sure = 1
        return flags
    # 初始化结果
    flags.flags_vertical = np.zeros((len(images2d), 2))
    flags.flags_horizon = np.zeros((len(images2d), 2))
    # flags.flags_bulk = np.zeros((len(images2d), 2))
    # flags.shining_a = np.zeros((len(images2d), 2))

    for i in range(len(images2d)):
        for j in range(2):
            (sub_flag_v, sub_flag_h) = sub_handler(images2d[i][j], name)
            flags.flags_vertical[i][j] = sub_flag_v
            flags.flags_horizon[i][j] = sub_flag_h
            # flags.flags_bulk[i][j] = sub_flag_b
            # flags.shining_a[i][j] = shining_a
    return flags


def main_loop(dir, name_list):
    res = []
    details_vertical = []
    details_horizon = []
    for name in name_list:
        flags = pic_handler(dir, name)
        print('纵:\n\r', flags.flags_vertical, sep='')
        print('横:\n\r', flags.flags_horizon, sep='')
        # print('块:\n\r', flags.flags_bulk, sep='')
        # print('闪:\n\r', flags.shining_a, sep='')

        if flags.flag_not_sure == 0:
            flag = classifier.cut_vertical_odd(flags.flags_vertical)
            # flag = flags.flags_vertical
            if (flag >= 1).any():
                # print(flag)
                res.append(name + '纵\n')
                details_vertical.append((name ,(flag >= 1).astype(np.uint8)))
                print(name, '纵裂')

            flag = flags.flags_horizon
            if (flag >= 1).any():
                res.append(name + '横\n')
                details_horizon.append((name, (flag >= 1).astype(np.uint8)))
                print(name, '横裂')
        else:
            res.append(name + '不确定\n')
            print(name, 'not sure')
    return res, details_vertical, details_horizon


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    for i in range(0, 3):
        print(str(i) + ' ：' + 'E:\\pics\\IMG0\\')
    dir = 'E:\\pics\\IMG'
    dir_num = input('请选择图像集，若需指定地址请输入-1：\n')
    if dir_num == '-1':
        dir = input('请输入地址，如：E:\\\\pics\\\\IMG0\\\\\n')
    else:
        dir += (dir_num + '\\')
    print('选择的图像集地址为：\n' + dir)
    img_num0 = input('从第几张图像开始？(从0编号)\n')
    img_num1 = input('测试多少张图像？\n')
    log_name = input('请输入结果文本的名称：\n')
    imglist = [name for name in os.listdir(dir) if len(name.split('.')) == 2 and name.split('.')[1] == 'jpg']
    imglist = imglist[int(img_num0): int(img_num0) + int(img_num1)]
    res, details_vertical, details_horizon = main_loop(dir, imglist)

    with open('E:\File\python\proj3\\log\\' + log_name + '.txt', 'w+') as f:
        f.writelines(res)
    f.close()

    with open('E:\File\python\proj3\\log\\' + log_name + '纵裂位置.txt', 'w+') as f:
        for i in details_vertical:
            f.write(str(i[0]) + '\n')
            for j in range((i[1].shape)[0]):
                f.write(str((i[1])[j][0]) + ' ' + str((i[1])[j][1]) + '\n')
    f.close()

    with open('E:\File\python\proj3\\log\\' + log_name + '横裂位置.txt', 'w+') as f:
        for i in details_horizon:
            f.write(str(i[0]) + '\n')
            for j in range((i[1].shape)[0]):
                f.write(str((i[1])[j][0]) + ' ' + str((i[1])[j][1]) + '\n')
    f.close()

