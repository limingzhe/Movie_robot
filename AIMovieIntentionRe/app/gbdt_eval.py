import numpy as np
from tensorflow.contrib import learn
from gensim import models, similarities, corpora
from algorithm.src.config.config import Param
from sklearn.externals import joblib
from flask import request, make_response, json, Blueprint
import jieba

def delete_entity(text):
        cinema = Param.cinema
        movie = Param.movie
        for item in cinema:
            if item in text:
                text = text.replace(item, 'YY')
        for item in movie:
            if item in text:
                text = text.replace(item, 'XX')
        return text

def sim_eval(text, label_text):
        # label_test 为相似性模型建立的语料标签
        print('导入已训练相似性相关模型......')
        dictionary = corpora.Dictionary.load('./algorithm/resource/model/similarity/dict.txt')
        tfidf_model = joblib.load('./algorithm/resource/model/similarity/tfidf_model.mm')
        lsi = models.LsiModel.load('./algorithm/resource/model/similarity/lsi.mm')
        corpus_tfidf = joblib.load('./algorithm/resource/model/similarity/corpus_tfidf.mm')

        test_raw = []
        test_raw.append(list(jieba.cut(text)))
        # print(test_raw)
        test_corpus = [dictionary.doc2bow(item) for item in test_raw]
        test_corpus_tfidf = tfidf_model[test_corpus]
        test_corpus_lsi = lsi[test_corpus_tfidf]  # 计算lsi值
        # print(test_corpus_lsi)
        corpus_lsi = lsi[corpus_tfidf]
        similaritiy_lsi = similarities.Similarity('Similarity-LSI-index', corpus_lsi, num_features=200, num_best=2)
        query = similaritiy_lsi[test_corpus_lsi][0]

        if len(query) < 1:
            query = [(0, 0), (0, 0)]
        if label_text[query[0][0]] == label_text[query[1][0]]:
            sim_estimate = label_text[query[0][0]]
        else:
            sim_estimate = 'null'
        similarity_score = str(query[0][1])[0:5]

        print('相似性判断完成......')

        return sim_estimate, similarity_score

def evaluate_gbdt(text):
    print('gbdt模型的意图识别......')
    gbdt = joblib.load("./algorithm/resource/model/gbdt.m")
    vocab_path = './algorithm/resource/model/vocab'
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_raw = []
    sentence_new = " ".join(list(jieba.cut(text)))
    x_raw.append(sentence_new)
    x_test = list(vocab_processor.transform(x_raw))  # array类型的

    y_label = gbdt.predict(x_test)
    y_pred = gbdt.predict_proba(x_test)
    va = np.var(y_pred)

    return y_label[0], y_pred, va

def filter_predict(sim_pred, sim_score, gbdt_pred, gbdt_score):
    if float(sim_score) < 0.5:  # 过滤掉与语料不相关的句子/意图
        pred = 'null'
    elif float(sim_score) > 0.99:
        pred = sim_pred
    elif gbdt_score > Param.model_threshold[str(gbdt_pred)]:
        pred = gbdt_pred
    elif sim_pred is not 'null' and float(sim_score) > Param.sim_threshold[str(sim_pred)]:
        pred = sim_pred
    else:
        pred = 'null'
    return str(pred)

intention = Blueprint('intention', __name__)

@intention.route('/getIntention.json', methods=['POST'])
def intention_re():
    """
    查询、订票、电影推荐意图识别
    :return:
    """
    text = ''
    if request.method == 'POST':
        text = request.json.get('text')

    label = joblib.load("./algorithm/resource/data/corpus_label.data")
    jieba.load_userdict('./algorithm/resource/dict/movie_dict.txt')
    text = delete_entity(text)  # 去掉影院和电影名称实体
    sim_estimate, similarity_score = sim_eval(text, label)
    y_label, y_pred, va = evaluate_gbdt(text)
    # print(sim_estimate, similarity_score, y_label, va)
    pred = filter_predict(sim_estimate, similarity_score, y_label, va)
    result = {'intention': pred}
    response = make_response(json.dumps(result, ensure_ascii=False))
    return response