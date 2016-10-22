#-*- coding: utf-8 -*-
import sys
from sklearn.externals import joblib
import MeCab
from konlpy.tag import Mecab

types = ["헤어스타일", "항공", "날씨", "방송", "교통", "동영상", "지도", "공공 데이터", "인물", "음식", "음악", "쇼핑", "영화 예매", "스포츠 경기", "환율", "주식", "로또 당첨 번호", "급식", "알바", "게임", "노래방", "놀이동산", "백과사전", "지식인", "블로그", "상담답변", "미분류"]

mecab = Mecab()
def add_space_mecab(s):
    if type(s) is not unicode:
        t = s.decode('utf-8')
    else:
        t = s
    p = mecab.pos(t)
    result = []
    for each in p:
        result.append(each[0])
    return ' '.join(result)

if __name__ == "__main__":
    vectorizer = joblib.load('jisik_vectorizer.dat')
    clf = joblib.load('jisik_classify_linear_svc.model')

    print "load complete"
    while True:
        line = raw_input('any question>')
        spaced_sentence = add_space_mecab(line)
        print spaced_sentence
        test_x = vectorizer.transform([spaced_sentence])
        print test_x.shape
        predict_list = clf.predict(test_x)
        print predict_list
        print types[predict_list[0]-1]
