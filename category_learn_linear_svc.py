#-*- coding: utf-8 -*-
import numpy as np
import sys
import gc
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.externals import joblib

def learn_with_linear_svc(x_list, s_list):
    svc_param = {'C':np.logspace(-2, 0, 20)}
    gs_svc = GridSearchCV(LinearSVC(),svc_param,cv=5,n_jobs=4)
    gs_svc.fit(x_list, s_list)
    print gs_svc.best_params_
    print 'score : ' + str(gs_svc.best_score_)
    clf = LinearSVC(C=gs_svc.best_params_['C'])
    clf.fit(x_list, s_list)
    print 'model initialized. dump running'
    joblib.dump(clf,'jisik_classify_linear_svc.model',compress=3)
    print 'done'

if __name__ == "__main__":
    np.random.seed(0)
    x_list = joblib.load('jisik_x_list.model')
    s_list = joblib.load('jisik_s_list.model')
    print "load complete"
    cnt = x_list.shape[0]
    indices = np.random.permutation(cnt)
    x_list = x_list[indices[:int(200000)]]
    s_list = [s_list[x] for x in indices[:int(200000)]]
    print "truncation complete"
    gc.collect()
    print "garbage collection complete"
    learn_with_linear_svc(x_list, s_list)
