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

def learn_word(filename):
    sentences = []
    cnt = 0
    with open(filename) as ifp:
        if cnt % 10000 == 0:
            print cnt
        cnt += 1
        for line in ifp:
            no_num_line = replace_num(line)
            sentences.append(remove_tags_mecab(no_num_line))
    my_min_count = int(len(sentences)/200) or 1
    model = gensim.models.Word2Vec(sentences, min_count=my_min_count, size=100000, workers=12)
    joblib.dump(model,filename + '_word2vec.model',compress=3)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    print sys.argv[1] + 'learning start'
    learn_word(sys.argv[1])
