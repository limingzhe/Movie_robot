"""
文件路径和参数配置
"""

class Param:

    # 各类别训练文件
    train_file_1 = "../resource/data/seg_0查询影票"
    train_file_2 = "../resource/data/seg_1影票预订"
    train_file_3 = "../resource/data/seg_2电影推荐"

    cinema = ['成龙影院', '保利国际影城', '中影国际影城']
    movie = ['我不是药神', '邪不压正']
    # 各类别阈值设置
    # 后期调参主要集中在相似度阈值和模型预测阈值部分
    model_threshold = {
        "0": 0.22,
        "1": 0.22,
        "2": 0.22
    }
    sim_threshold = {
        "0": 0.8,
        "1": 0.8,
        "2": 0.8
    }

def load_data(class_1_file, class_2_file, class_3_file):
    """
        导入数据集及对应的标签
        :param class_?_file:
        :return: 所有训练数据集标签的集合
    """
    print("Loading...")
    class_1 = list(open(class_1_file, encoding="utf8").readlines())
    class_1 = [sentence.strip() for sentence in class_1]
    class_2 = list(open(class_2_file, encoding="utf8").readlines())
    class_2 = [sentence.strip() for sentence in class_2]
    class_3 = list(open(class_3_file, encoding="utf8").readlines())
    class_3 = [sentence.strip() for sentence in class_3]

    x_text = class_1 + class_2 + class_3
    y = []
    for _ in class_1:
        y.append(0)
    for _ in class_2:
        y.append(1)
    for _ in class_3:
        y.append(2)

    return x_text, y

if __name__ == "__main__":
    class_1_file = "../" + Param.train_file_1
    class_2_file = "../" + Param.train_file_2
    class_3_file = "../" + Param.train_file_3
    x_text, y = load_data(class_1_file, class_2_file, class_3_file)
    print(len(x_text), len(y))