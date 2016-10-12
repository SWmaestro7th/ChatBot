#-*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import MeCab
import json
import sys
from konlpy.tag import Mecab

types = ["공기질", "날씨", "교통", "동영상", "지도", "공공 데이터", "인물", "음식", "음악", "쇼핑", "영화 예매", "스포츠 경기", "환율", "주식", "뉴스", "로또 당첨 번호", "급식", "알바", "게임", "노래방", "놀이동산", "백과사전", "지식인", "블로그", "상담답변", "미분류"]

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

def init_list(filename, get_a_list=False):
    type_keywords = [
        ["cleanair", "air", "aqicn"],
        ["kma.go.kr", "weather", "날씨"],
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
        ["news", "ytn", "sbs", "mbc", "kbs", "joins", "mbn", "jtbc", "chosun", "mt.co.kr"],
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
    if get_a_list:
        a_list = []
    s_list = []
    with open(filename) as ifp:
        ifp.next()
        row_cnt = 0
        for line in ifp:
            try:
                if row_cnt % 100000 == 0:
                    print row_cnt
                '''
        0,힘내세요  힘드신일이있으면 언제든지 지식맨에게 질문해주시면 24시간답변나갑니다 ^^,1,3,"{u'status': u'N', u'update_date': u'2007-04-30T21:19:24.000Z', u'dislike_cnt': 0, u'user_id': 2, u'reg_date': u'2007-04-30T21:19:24.000Z', u'jisikman_flag': 1, u'like_cnt': 0, u'source': u'', u'adopted_flag': 1, u'old_jisikman_rid': 1177967964370, u'type': u'A', u'id': 1, u'recency_score': -1177967964}",힘들다
                '''
                sp_arr = line.split(',"{u')
                sp_arr2 = sp_arr[1].split('}",')
                q = sp_arr2[1].strip()
                a = ','.join(sp_arr[0].split(',')[1:-2]).strip()
                try:
                    s = json.loads('"'+sp_arr2[0].replace('"', "'").split("', u'adopted_flag'")[0].split("u'source': u'")[1]+'"').encode('utf-8')
                except:
                    s = sp_arr2[0].replace('"', "'").split("', u'adopted_flag'")[0].split("u'source': u'")[1].encode('utf-8')
                found_type = len(types)
                decoded_s = s.decode('utf-8')
                for idx, item in enumerate(decoded_type_keywords):
                    if any([x in decoded_s for x in item]):
                        found_type = idx+1
                        break

                q_list.append(add_space_mecab(q))
                if get_a_list:
                    a_list.append(a)
                s_list.append(s)
                cnt_dict[found_type] += 1
                # if found_type == len(types) and s != "" and "naver" not in s:
                #    print q + ' : ' + s
            except:
                print "error : " + line

            row_cnt += 1
            if len(sys.argv) >= 2 and row_cnt > int(sys.argv[1]):
                break
    if get_a_list:
        return q_list, a_list, s_list
    else:
        return q_list, s_list

if __name__ == "__main__":
    q_list, s_list = init_list('jisiklog.csv')
    print "parsing complete"
    vectorizer = CountVectorizer()
    x_list = vectorizer.fit_transform(q_list)
    joblib.dump(vectorizer,'jisik_vectorizer.dat',compress=3)
    joblib.dump(x_list,'jisik_x_list.model',compress=3)
    joblib.dump(s_list,'jisik_s_list.model',compress=3)
    print "vectorizer initialized"
    print "done"
