#-*- coding: utf-8 -*-
from sklearn.externals import joblib
import MeCab
from konlpy.tag import Mecab
import sys
import evaluator as ev

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

def predict_sentence(model, att_words, sentence):
    words = remove_tags_mecab(replace_num(sentence))
    best_att_val = {x : None for x in att_words}
    best_att_key = {x : "" for x in att_words}
    d = {'question' : sentence, 'result' : {}}
    for each in words:
        for att in att_words:
            try:
                val = model.similarity(att_words[att], each)
                if best_att_val[att] == None or best_att_val[att] < val:
                    best_att_val[att] = val
                    best_att_key[att] = each
            except KeyboardInterrupt:
                print "user terminated"
                sys.exit()
            except Exception as ex:
                print 'error : ' + each.encode('utf-8')

    for each in best_att_key:
        d['result'][each] = best_att_key[each]
    return d

def simulate(model_filename, att_words, test_filename = None):
    model = joblib.load(model_filename)
    if test_filename != None:
        return ev.evaluate_fscore(test_filename, lambda x: predict_sentence(model, att_words, x))
    else:
        while True:
            sentence = raw_input("question>")
            d = predict_sentence(model, att_words, sentence)
            res = d['result']
            print res
            for att in res:
                print str(att) + ': ' + res[att].encode('utf-8')
            print d
