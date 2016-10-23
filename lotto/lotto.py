#-*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))) + '/common')
import simulator as sm

if __name__ == '__main__':
    att_words = {
        u'date' : u'오늘',
        u'purpose' : u'번호'
    }
    result = sm.simulate('lotto_word2vec.model', att_words, 'lotto_testcase')
    print result
