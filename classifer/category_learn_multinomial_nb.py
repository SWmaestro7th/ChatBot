#This program is not stabilized
#-*- coding: utf-8 -*-
import numpy as np
import sys
import gc
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

def iter_minibatches(chunksize, x_train, y_train):
    # Provide chunks one by one
    chunkstartmarker = 0
    indices = np.random.permutation(x_train.shape[0])
    while chunkstartmarker < x_train.shape[0]:
        chunkrows = indices[chunkstartmarker:chunkstartmarker+chunksize]
        x_chunk = x_train[chunkrows]#[x_train[x] for x in indices]
        y_chunk = [y_train[x] for x in chunkrows]
        yield x_chunk, y_chunk
        chunkstartmarker += chunksize

def learn_with_multinomial_nb(x_list, s_list):
    indices = np.random.permutation(x_list.shape[0])
#number of test data
    cnt_test = 100
    x_train = x_list[indices[:-cnt_test]]#[x_list[x] for x in indices[:-cnt_test]]
    s_train = [s_list[x] for x in indices[:-cnt_test]]
    x_test = x_list[indices[-cnt_test:]]#[x_list[x] for x in indices[-cnt_test:]]
    s_test = [s_list[x] for x in indices[-cnt_test:]]
    del x_list
    del s_list
    gc.collect()
    print "garbage collection complete"
    clf = MultinomialNB()
    classes = np.unique(s_train)
    if 1:
        n_iter = 10
        for i in range(n_iter):
            print "iter : " + str(i)
            batcherator = iter_minibatches(chunksize=1, x_train=x_train, y_train=s_train)
            batch_cnt = 0
            for x_batch_train, s_batch_train in batcherator:
                print x_batch_train.shape
                batch_cnt += 1
                print batch_cnt
                clf.partial_fit(x_batch_train, s_batch_train, classes=classes)
    else:
        clf.fit(x_train, s_train)
    print clf.coef_
    print 'score : ' + str(clf.score(x_test, s_test))
    joblib.dump(clf,'jisik_classify_multinomial_nb.model',compress=3)

if __name__ == "__main__":
    np.random.seed(0)
    x_list = joblib.load('jisik_x_list.model')
    s_list = joblib.load('jisik_s_list.model')
    print "load complete"
    learn_with_multinomial_nb(x_list, s_list)
