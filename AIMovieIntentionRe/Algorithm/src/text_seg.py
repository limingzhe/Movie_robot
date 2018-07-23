import jieba
from algorithm.src.config.config import Param

path = '../resource/data'
# 导入字典
jieba.load_userdict('../resource/dict/movie_dict.txt')

# 逐个文件读取并分词，写入新的文件中。
file_name = ['0查询影票',
             '1影票预订',
             '2电影推荐'
             ]

cinema = Param.cinema
movie = Param.movie

for file in file_name:
    file_fill = path + '/' + file
    seg_text = []
    with open(file_fill, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines:
            # 讲影院和电影名称替换为YY和XX
            for item in cinema:
                if item in line:
                    line = line.replace(item, 'YY')
            for item in movie:
                if item in line:
                    line = line.replace(item, 'XX')

            seg_list = list(jieba.cut(line))
            seg_text.append(seg_list)

    with open(path + '/seg_' + file, 'w', encoding='utf-8') as fp2:
        for line in seg_text:
            line = ' '.join(line)
            fp2.write(line)