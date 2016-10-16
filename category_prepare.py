#-*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import MeCab
import json
import sys
from konlpy.tag import Mecab

types = ["헤어스타일", "항공", "날씨", "방송", "교통", "동영상", "지도", "공공 데이터", "인물", "음식", "음악", "쇼핑", "영화 예매", "스포츠 경기", "환율", "주식", "로또 당첨 번호", "급식", "알바", "게임", "노래방", "놀이동산", "백과사전", "지식인", "블로그", "상담답변", "미분류"]
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

def init_list(filename, get_a_list=False):
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
                s_list.append(found_type)
                cnt_dict[found_type] += 1
                if print_split_result:
                    fps[found_type-1].write(q + ' ::: ' + s + '\n')
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
            print str(key) + " : " + str(cnt_dict[key])
    if get_a_list:
        return q_list, a_list, s_list
    else:
        return q_list, s_list

if __name__ == "__main__":
    q_list, s_list = init_list('jisiklog.csv')
    if print_split_result:
        for each in fps:
            each.close()

    print "parsing complete"
    #vectorizer = CountVectorizer()
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    x_list = vectorizer.fit_transform(q_list)
    joblib.dump(vectorizer,'jisik_vectorizer.dat',compress=3)
    joblib.dump(x_list,'jisik_x_list.model',compress=3)
    joblib.dump(s_list,'jisik_s_list.model',compress=3)
    print "vectorizer initialized"
    print "done"
