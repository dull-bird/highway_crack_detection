def get_set():
    s1 = set()
    s2 = set()
    s_not_sure = set()
    with open('E:\File\python\proj3\\log\\IMG0_5_5.txt', 'r') as f1:
        for line in f1.readlines():
            #if '不' not in line:
            #if '闪' not in line and '块' not in line:
            #if '纵' in line or '不确定': #in line or '纵' in line or '块' in line:
            #if '闪' in line:
            #if '不确定' in line or '纵' in line or '闪' in line:
            #print(line)
            #s1.add(line.split('.jpg')[0])
            if line.split('.jpg')[0] < '0000'+'2000'+'0000':
                if '不确定' in line:
                    s_not_sure.add(line.split('.jpg')[0] + '.jpg')
                    #s1.add(line.split('.jpg')[0] + '.jpg')
                else:
                    if '纵' in line:
                        s1.add(line.split('.jpg')[0] + '.jpg')
                        #s1.pop('')

    with open('E:\\pics\\IMG0\\output.txt', 'r') as f2:
        for line in f2.readlines():
            if ('纵' in line) :
            #if ('横' in line):
            #if ('横' in line or '纵' in line or '块' in line) and '修' not in line:
            #print(f2.readlines()[2].split(','))
                for name in line.split(','):
                    if '.jpg' in name and name.split('.')[0] < '0000'+'2000'+'0000' and name.split('.')[0] >= '0000'+'0000'+'0000':
                        name1 = name.split('.')[0] + '.jpg'
                        #print(name1+'..')
                        s2.add(name1)

    s2 -= s_not_sure
    f1.close()
    f2.close()
    return s1, s2, s_not_sure


def calcu_result(s1, s2, s_not_sure):

    print(len(s1))
    sc = s1 & s2
    s3 = s1 - s2
    s4 = s2 - s1

    precision = len(sc) / len(s1)
    recall = len(sc) / len(s2)
    print('precision', precision)
    print('recall', recall)
    f1_score = 2 * precision * recall / (precision + recall)
    print('误检：', s3)
    print('漏检：', s4)

    print('匹配的裂纹数：', len(sc))
    print('找到的疑似裂纹数：', len(s1))
    print('标记的裂纹数', len(s2))

    print('误检数目：', len(s3))
    print('误检率：%.2f' % (1- precision))

    print('漏检数目：', len(s4))
    print('漏检率：%.2f' % (1- recall))
    print('不确定的数目：', len(s_not_sure))
    print('f1_score', f1_score)

if __name__ == '__main__':
    s1, s2, s_not_sure = get_set()
    calcu_result(s1, s2, s_not_sure)