#-*- coding: utf-8 -*-
import json

def evaluate_fscore(test_filename, predict_function):
    tn = 0
    tp = 0
    fn = 0
    fp = 0
    with open(test_filename) as tfp:
        for line in tfp:
            test_dict = json.loads(line)
            my_dict = predict_function(test_dict['question'])
            test_result = test_dict['result']
            my_result = my_dict['result']
            for att in test_result:
                print str(att) + ': answer: ' + test_result[att].encode('utf-8') + ' /predict: '  + my_result[att].encode('utf-8')
                if test_result[att] == "":
                    if my_result[att] == "":
                        tn += 1
                    else:
                        fp += 1
                else:
                    if test_result[att] in my_result[att]:
                        tp += 1
                    else:
                        fn += 1

    precision = float(tp) / float(tp + fp)
    recall = float(tp) / float(tp + fn)
    fscore = 2 * precision * recall / (precision + recall)
    return {'precision' : precision, 'recall' : recall, 'fscore' : fscore}
