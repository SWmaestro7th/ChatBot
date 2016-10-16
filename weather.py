#-*- coding: utf-8 -*-
from sklearn.externals import joblib
import MeCab
from konlpy.tag import Mecab
import sys
import gensim, logging
import Cython

remove_list = ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JC", "JX", "EP", "EF", "EC", "ETN","ETM", "XPN", "XSN", "XSV", "XSA", "XR", "SF", "SE", "SS", "SP", "SO", "SW"]
def replace_num(s):
    t = s[:]
    for ch in '0123456789':
        t = t.replace(ch, 'd')
    return t

mecab = Mecab()
def remove_tags_mecab(s):
    if type(s) is not unicode:
        t = s.decode('utf-8')
    else:
        t = s
    p = mecab.pos(t)
    return [x[0] for x in p if x[1] not in remove_list]

if __name__ == "__main__":
    model = joblib.load(sys.argv[1] + '_word2vec.model')
    while True:
        word = raw_input("Weather question>")
        words = remove_tags_mecab(replace_num(word))
        best_tm = None
        best_pl = None
        for each in words:
            tm = model.similarity(u'오늘', each)
            pl = model.similarity(u'서울', each)
            if best_tm == None or best_tm < tm:
                best_tm = tm
                best_tm_key = each
            if best_pl == None or best_pl < pl:
                best_pl = pl
                best_pl_key = each
        print '시간 : ' + best_tm_key.encode('utf-8') + ' : ' + str(best_tm)
        print '장소 : ' + best_pl_key.encode('utf-8') + ' : ' + str(best_pl)
