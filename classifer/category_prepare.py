#-*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import MeCab
import json
import sys
from konlpy.tag import Mecab

types = ["헤어스타일", "항공", "날씨", "방송", "교통", "동영상", "지도", "공공 데이터", "인물", "음식", "음악", "쇼핑", "영화 예매", "스포츠 경기", "환율", "주식", "로또 당첨 번호", "급식", "알바", "게임", "노래방", "놀이동산", "백과사전", "지식인", "블로그", "상담답변", "미분류"]

use_types = ["스포츠 경기", "날씨", "급식", "노래방", "놀이동산", "로또 당첨 번호", "백과사전"]

print_split_result = True
if print_split_result:
    fps = []
    for i in range(len(types)):
        fps.append(open('types'+str(i+1),'w'))

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

def truncate_list(cnt_dict, q_list, a_list, s_list):
    decoded_types = [x.decode('utf-8') for x in types]
    decoded_use_types = [x.decode('utf-8') for x in use_types]
    use_types_idx = [decoded_types.index(i)+1 for i in decoded_use_types]
    min_type_cnt = min([cnt_dict[x] for x in use_types_idx])
    new_cnt_dict = {x:0 for x in use_types_idx}
    trun_q_list = []
    trun_a_list = []
    trun_s_list = []
    idx = 0
    total_cnt = min_type_cnt * len(use_types_idx)
    print total_cnt
    while total_cnt > 0:
        if s_list[idx] in use_types_idx:
            if new_cnt_dict[s_list[idx]] < min_type_cnt:
                new_cnt_dict[s_list[idx]] += 1
                trun_q_list.append(q_list[idx])
                trun_a_list.append(a_list[idx])
                trun_s_list.append(s_list[idx])
                total_cnt -= 1
        idx += 1

    return trun_q_list, trun_a_list, trun_s_list

def init_list(filename):
    type_keywords = [
        ["hair"],
        [".air", "air.", "-air", "air-","airport"],
        ["kma.go.kr", "weather", "날씨"],
        ["news", "ytn", "sbs", "mbc", "kbs", "joins", "mbn", "jtbc", "chosun", "mt.co.kr", "mnet"],
        ["way", "road", "spatic", "gits", "its", "traffic", "molit", "metro", "bus", "smrt", "ti21", "korail"],
        ["video", "youtube", "동영상", "영상"],
        ["map", "local", "navi", "topis.go.kr"],
        ["data.", "data.go", "gov", "go.kr", "msip"],
        ["people"],
        ["food", "dining", "restaurant", "plate", "eat", "menupan", "음식", "맛집", "gugi", "pizza", "baskin", "vips", "outback"],
        ["music", "melon", "bugs"],
        ["shopping", "auction", "danawa", "gmarket", "mart", "market", "uniqlo", "kyobobook", "interpark", "ypbooks", "shinsegae", "mall", "homeplus"],
        ["cgv", "megabox", "cinus", "cinema", "movie", "kinex5"],
        ["sport", "score", "soccer", "ball", "uefa", "doosanbears", "giantsclub", "hanwhaeagles"],
        ["exchange", "TodayEx"],
        ["finance", "stock", "paxnet", "trade"],
        ["lotto","bokgwon", "로또", "복권"],
        ["hs.kr", "meal", "ms.kr", "es.kr", "yego"],
        ["alba"],
        ["game"],
        ["kumyoung", "tjmedia"],
        ["seoulland", "everland"],
        ["dic", "pedia", "100.", "encyclo", "pedia", "terms."],
        ["kin.", "tip."],
        ["blog"],
        ["상담답변"],
        []]
    decoded_type_keywords = [ [y.decode('utf-8') for y in x] for x in type_keywords]
    cnt_dict = {i+1:0 for i in xrange(len(types))}
    q_list = []
    a_list = []
    s_list = []
    with open(filename) as ifp:
        ifp.next()
        row_cnt = 0
        for line in ifp:
            try:
                if row_cnt % 100000 == 0:
                    print row_cnt
                sp_arr = line.split(',"{u')
                sp_arr2 = sp_arr[1].split('}",')
                q = sp_arr2[1].strip()
                a = ','.join(sp_arr[0].split(',')[1:-2]).strip()
                try:
                    s = json.loads('"'+sp_arr2[0].replace('"', "'").split("', u'adopted_flag'")[0].split("u'source': u'")[1]+'"').encode('utf-8')
                except:
                    s = sp_arr2[0].replace('"', "'").split("', u'adopted_flag'")[0].split("u'source': u'")[1].encode('utf-8')
                type_idx = len(types)
                decoded_s = s.decode('utf-8')
                for idx, item in enumerate(decoded_type_keywords):
                    if any([x in decoded_s for x in item]):
                        type_idx = idx+1
                        break
                q_list.append(add_space_mecab(q))
                a_list.append(a)
                s_list.append(type_idx)
                cnt_dict[type_idx] += 1
                if print_split_result:
                    fps[type_idx-1].write(q + '\n')
            except KeyboardInterrupt:
                print "user terminated"
                sys.exit()
            except Exception as ex:
                print "error : " + line
                print ex

            row_cnt += 1
            if len(sys.argv) >= 2 and row_cnt > int(sys.argv[1]):
                break

    for key in cnt_dict:
        if cnt_dict[key] > 0:
            print types[key-1] + " : " + str(cnt_dict[key])

    trun_q_list, trun_a_list, trun_s_list = truncate_list(cnt_dict, q_list, a_list, s_list)
    #return q_list, s_list
    return trun_q_list, trun_s_list

if __name__ == "__main__":
    q_list, s_list = init_list('jisiklog.csv')
    if print_split_result:
        for each in fps:
            each.close()

    print "parsing complete"
    vectorizer = CountVectorizer()
    #vectorizer = TfidfVectorizer(ngram_range=(1,2))
    x_list = vectorizer.fit_transform(q_list)
    print "vectorizer initialized"
    joblib.dump(vectorizer,'jisik_vectorizer.dat',compress=3)
    joblib.dump(x_list,'jisik_x_list.model',compress=3)
    joblib.dump(s_list,'jisik_s_list.model',compress=3)
    print "done"
