#This program is not stabilized
#-*- coding: utf-8 -*-
import numpy as np
import sys
import gc
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib

def iter_minibatches(chunksize, x_train, y_train):
    # Provide chunks one by one
    chunkstartmarker = 0
    indices = np.random.permutation(x_train.shape[0])
    while chunkstartmarker < x_train.shape[0]:
        chunkrows = indices[chunkstartmarker:chunkstartmarker+chunksize]
        x_chunk = x_train[chunkrows]
        y_chunk = [y_train[x] for x in chunkrows]
        yield x_chunk, y_chunk
        chunkstartmarker += chunksize

def learn_with_SGD(x_list, s_list):
    indices = np.random.permutation(x_list.shape[0])
    cnt_test = 100
    x_train = x_list[indices[:-cnt_test]]
    print "truncation1"
    s_train = [s_list[x] for x in indices[:-cnt_test]]
    print "truncation2"
    x_test = x_list[indices[-cnt_test:]]
    print "truncation3"
    s_test = [s_list[x] for x in indices[-cnt_test:]]
    del x_list
    del s_list
    print "truncation complete"
    clf = SGDClassifier(loss='log', n_jobs=4, warm_start=False)
    classes = np.unique(s_train)
    if 1:
        n_iter = 1
        for i in range(n_iter):
            print 'iter : ' + str(i)
            batcherator = iter_minibatches(chunksize=1000, x_train=x_train, y_train=s_train)
            gc.collect()
            batch_cnt = 0
            for x_batch_train, s_batch_train in batcherator:
                batch_cnt += 1
                print batch_cnt
                clf.partial_fit(x_batch_train, s_batch_train,classes=classes)
    else:
        clf.fit(x_train, s_train)
    print clf.coef_
    print 'score : ' + str(clf.score(x_test, s_test))
    joblib.dump(clf,'jisik_classify_SGD.model',compress=3)

if __name__ == "__main__":
    np.random.seed(0)
    x_list = joblib.load('jisik_x_list.model')
    s_list = joblib.load('jisik_s_list.model')
    print "load complete"
    gc.collect()
    print "garbage collection complete"
    learn_with_SGD(x_list, s_list)
