import jieba
import warnings
from algorithm.src.config.config import Param, load_data
from sklearn.externals import joblib
from gensim import models, similarities, corpora

jieba.load_userdict('../resource/dict/movie_dict.txt')
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
# 参数
class_1_train = Param.train_file_1
class_2_train = Param.train_file_2
class_3_train = Param.train_file_3


# 导入数据
x_text, y = load_data(class_1_train, class_2_train, class_3_train)  # 训练集
x_new = []
for item in x_text:
    x_new.append(item.split())
# print(x_new)

joblib.dump(y, '../resource/data/corpus_label.data')
dictionary = corpora.Dictionary(x_new)
dictionary.save('../resource/model/similarity/dict.txt')  #保存生成的词典
# dictionary = corpora.Dictionary.load('dict.txt')#加载
corpus = [dictionary.doc2bow(text) for text in x_new]
# corpora.MmCorpus.serialize('../resource/model/similarity/corpuse.mm',corpus)  #保存生成的语料
# corpus = corpora.MmCorpus('../resource/model/similarity/corpuse.mm')  #加载
tfidf_model = models.TfidfModel(corpus)
tfidf_model.save('../resource/model/similarity/tfidf_model.mm')

corpus_tfidf = tfidf_model[corpus]
joblib.dump(corpus_tfidf, '../resource/model/similarity/corpus_tfidf.mm')

lsi = models.LsiModel(corpus_tfidf)
lsi.save('../resource/model/similarity/lsi.mm')

corpus_lsi = lsi[corpus_tfidf]
similarity_lsi = similarities.Similarity('../resource/model/similarity/Similarity-LSI-index', corpus_lsi, num_features=250,num_best=2)

test = 'A啊啊啊啊啊分期'
test_raw = list(jieba.cut(test))
test_corpus = dictionary.doc2bow(test_raw)
test_corpus_tfidf = tfidf_model[test_corpus]

lsi = models.LsiModel.load('../resource/model/similarity/lsi.mm')
test_corpus_lsi = lsi[test_corpus_tfidf]  # 4.计算lsi值
print(test_corpus_lsi)
query_lsi = similarity_lsi[test_corpus_lsi]
print(query_lsi)
