import numpy as np
from skimage.measure import label,regionprops
from skimage.morphology import binary_erosion, disk
import res_drawer

def get_regions(binary):
    labels = label(binary, connectivity=2)
    props = regionprops(labels)
    return props

def classifier_vertical(props, binary, name =''):
    flag = 0
    #temp_binary = np.zeros_like(binary)
    xs = []
    for r in props:
        #print('r', r.area)
        #print('area:', r.area, 'ecctr', r.eccentricity, 'orit', r.orientation *180/np.pi)
        if abs(r.orientation * 180/np.pi) > 45:
            p = logistic_h(r.area, r.eccentricity, 3)
            x = r.centroid[1]
            if p >= 0.4 and x > 60 and x < binary.shape[1] - 60 and r.area > 700 or r.area > 10000:
                print('纵', r.area, r.eccentricity, r.orientation * 180/np.pi)
                print('prob', p)
                print('x', x)

                if p >= 0.8 or r.area > 10000:
                    d_flag = 1
                else:
                    d_flag = 0.5

                flag_x = 1
                for i in xs:
                    if np.abs(x - i) <= 50:
                        flag_x = 0
                        break
                if flag_x == 1:
                    xs.append(x)
                    flag += d_flag
                    #for i in r.coords:
                        #temp_binary[i[0], i[1]] = 1
    #res_drawer.binary_single(temp_binary)
    #print('sum', np.sum(temp_binary))
    #binary_shining = binary_erosion(temp_binary * binary_shining, disk(0))
    return flag

def classifier_horizon(props, name):
    flag = 0
    for r in props:
        #print(r.area, r.eccentricity)
        #print('r', r.area)
        #print('area:', r.area, 'ecctr', r.eccentricity, 'orit', r.orientation *180/np.pi)
        '''
        if abs(r.orientation * 180/np.pi) <= 30:
            if r.area * np.power(r.eccentricity, 13) > 760:
                #print('r', r.area, r.eccentricity, r.orientation *180/np.pi)
                if r.area < 1000:
                    print(r.area, r.eccentricity, 1)
                flag = 1
            else:
                if r.area > 1000:
                    print(r.area, r.eccentricity, 0)
        '''
        if abs(r.orientation * 180 / np.pi) <= 45:
            p = logistic_h(r.area, r.eccentricity, 3)
            if p >= 0.5 and r.area > 700 or r.area > 10000:
                print('横', r.area, r.eccentricity, r.orientation *180/np.pi)
                print('prob', p)
                flag = 1
    return flag


def classifier(binary, name):
    props = get_regions(binary)
    flag_v = classifier_vertical(props, binary, name)
    #res_drawer.binary_single(binary_shining)
    flag_h = classifier_horizon(props, name)
    #flag_b = classifier_bulk(props)
    #shinging_a = shining_area(binary_shining)
    return (flag_v, flag_h)

def cut_vertical_odd(flag_vertical):

    '''
    f_col = np.sum(flag_vertical, 0)
    #print(f_col)
    if f_col[0] == 1:
        flag_vertical[:, 0] = 0
    if f_col[1] == 1:
        flag_vertical[:, 1] = 0
    '''
    '''
    if np.sum(flag_vertical) < 1:
        return np.zeros_like(flag_vertical)
    '''
    f_col = np.sum(flag_vertical.astype(np.bool), 0)
    if f_col[0] >= 3:
        idx = np.where(flag_vertical[:, 0] > 0)
        if np.max(idx) - np.min(idx) >= 4:
            flag_vertical[idx, 0] -= 1
    if f_col[1] >= 3:
        idx = np.where(flag_vertical[:, 1] > 0)
        if np.max(idx) - np.min(idx) >= 4:
            flag_vertical[idx, 1] -= 1
    return flag_vertical

def map_feature(x1, x2, degree):
    n = degree + 1
    out = np.ones((1, n*(n + 1)//2))
    count = 1
    for i in range(1, degree+1):
        for j in range(0, i+1):
            out[:, count] = np.power(x1, i - j) * np.power(x2, j)
            count += 1
    return out

def logistic_h(area, eccentricity, degree=3):
    #degree is 4
    '''
    theta =\
    [-13.8205664414719,
    0.635387559491512,
    1.02832031448641,
    -0.578939848754416,
    1.07906004070390,
    1.42586583327415,
    -0.263324056987809,
    -0.427329275669310,
    1.46212293261547,
    1.82582780474332,
    -0.0841240498291415,
    -0.215943528910584,
    -0.297991246025421,
    1.79196542014552,
    2.21464227580691]
    '''
    theta =\
    [
        -2.05169929005595,
        1.30149938088806,
        1.17740089030928,
        0.0599576360735711,
        1.45808611225043,
        1.36051683075630,
        - 0.0230185467907434,
        0.102799555432432,
        1.58564062414904,
        1.53476548146382
    ]
    '''
    mu = [0, 541.897243107769,	0.689637085522261,	3421456.23809524,	485.268742675312,	0.513118847317045,	40854262155.5965,	3299072.14394621,	446.300872833460,	0.403129401147594,	601237324373498,	39891549951.3325,	3195048.92987446,	417.170046252123,	0.329751966270763]
    sigma  = [1, 1769.29896750723,	0.193780567757027,	24290407.1692612,	1721.05715431195,	0.257908092562363,	409742064113.533,	23852032.2679347,	1681.15655789928,	0.279046064590182,	7.47318040596747e+15,	403817000728.070,	23462040.1886201,	1646.98808888336,	0.283868191108957]
    '''
    mu = [0, 2129.34161490683,	0.874426260901398,	15637701.6024845,	1979.36833096125,	0.781711279763270,	199454978269.429,	15020229.5677264,	1858.82074320575,	0.710649613252181]
    sigma = [1, 3342.60428802452,	0.131136594708828,	54634244.3736692,	3260.53932044923,	0.208708320717665,	1024864551191.59,	53890609.4163464,	3192.19791618929,	0.256115025592608]
    x = map_feature(area, eccentricity, degree)
    x = (x - mu) / sigma

    h = np.dot(x,theta)
    p = 1/(1 + np.exp(-h))
    return p