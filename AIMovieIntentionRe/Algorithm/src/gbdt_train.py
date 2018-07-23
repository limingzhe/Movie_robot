import numpy as np
from tensorflow.contrib import learn
from algorithm.src.config.config import Param, load_data
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.externals import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


# 参数
class_1_train = Param.train_file_1
class_2_train = Param.train_file_2
class_3_train = Param.train_file_3

# 导入数据
x_text, y = load_data(class_1_train, class_2_train, class_3_train)  # 训练集
# 词典
max_sentence_length = max([len(x.split(" ")) for x in x_text])  # 语料中最长句子的长度
# print(max_sentence_length)
vocab_processor = learn.preprocessing.VocabularyProcessor(max_sentence_length)
vocab_processor.save("../resource/model/vocab")
x = np.array(list(vocab_processor.fit_transform(x_text)))  # 类似于词袋模型

# 分割训练/测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=21)
gbdt_model = GradientBoostingClassifier(loss='deviance',learning_rate=0.05, n_estimators=1500,
                                        subsample=0.9, criterion='friedman_mse', min_samples_split=3,
                                        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=3,
                                        random_state=None, max_features=0.9, verbose=0, max_leaf_nodes=None,
                                        warm_start=False, presort='auto')

gbdt_model.fit(x, y)
# print(len(x[1]))  # 28
gbdt_pred = gbdt_model.predict(x_test)
joblib.dump(gbdt_model, "../resource/model/gbdt.m")
report = classification_report(y_test, gbdt_pred)
cm = confusion_matrix(y_test, gbdt_pred)
acc = accuracy_score(y_test, gbdt_pred)
print(report)
print(cm)
print(acc)

"""

if __name__ == "__main__":
    param_test = {
        'subsample': [i/10 for i in range(7,10)],
        'max_features': [i/10 for i in range(7,10)]

    }
    grid_gbdt = GridSearchCV(
        estimator=GradientBoostingClassifier(loss='deviance', learning_rate=0.05, n_estimators=1500,
                                             subsample=0.9, criterion='friedman_mse', min_samples_split=3,
                                             min_samples_leaf=1, max_features=0.9,
                                             min_weight_fraction_leaf=0.0, max_depth=4, random_state=None,
                                             verbose=0, max_leaf_nodes=None, warm_start=False, presort='auto'),
        param_grid=param_test, cv=5, n_jobs=8)
    grid_gbdt.fit(x, y)
    print(grid_gbdt.best_estimator_, grid_gbdt.best_params_, grid_gbdt.best_score_)

 

"""