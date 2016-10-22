#-*- coding: utf-8 -*-
from sklearn.externals import joblib
import sys
import numpy as np
import json
import random

types = ["헤어스타일", "항공", "날씨", "방송", "교통", "동영상", "지도", "공공 데이터", "인물", "음식", "음악", "쇼핑", "영화 예매", "스포츠 경기", "환율", "주식", "로또 당첨 번호", "급식", "알바", "게임", "노래방", "놀이동산", "백과사전", "지식인", "블로그", "상담답변", "미분류"]

def get_q_list(filename):
    q_list = []
    with open(filename,'r') as fp:
        for line in fp:
            q_list.append(line)
    random.shuffle(q_list)
    return q_list

def get_attr_list():
    cnt = 0
    attr_list = []
    while True:
        try:
            cnt += 1
            attrname = raw_input('핵심 정보' + str(cnt) + ': ')
            attr_list.append(attrname)
        except:
            break

    return attr_list

if __name__ == '__main__':
    #np.random.seed(0)
    if sys.argv[1].isdigit():
        x = sys.argv[1]
    else:
        decoded_types = [x.decode('utf-8') for x in types]
        for i in range(types):
            if sys.argv[1] in types[i].decode('utf-8'):
                x = str(i+1)
                break
    filename = 'types' + x
    q_list = get_q_list(filename)
    attr_list = get_attr_list()
    fp = open(filename+ '_testcase', 'w')

    cnt = 1
    for each in q_list:
        try:
            skip_case = False
            print unicode(cnt) + u': ' + each.decode('utf-8')
            d = {'question' : each, 'result' : {}}
            for att in attr_list:
                val = raw_input(att + u': ')
                if val == 'n':
                    skip_case = True
                    break
                d['result'][att] = val
            if skip_case:
                continue
            print json.dumps(d)
        except KeyboardInterrupt:
            print "Exit..."
            break
        except Exception as ex:
            print "error : " + str(ex)
            continue

        cnt += 1
        fp.write(json.dumps(d) + '\n')
        if cnt >= 100:
            break
    print str(cnt) + ' Complete!'
    fp.close()
