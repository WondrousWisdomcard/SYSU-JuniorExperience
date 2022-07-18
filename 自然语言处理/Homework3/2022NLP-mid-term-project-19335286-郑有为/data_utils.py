import re
import time

import numpy as np
import pandas as pd
from textblob import TextBlob
from textblob import Word
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
Stopwords = set(stopwords.words('english'))  # nltk 英文停用词
from gensim.models import Word2Vec

"""
* data_clean 文本数据清洗
* Params:
    * s: String 输入文本串
* Returns:
    * s: String 数据清洗并分词的字符串
"""
def data_clean(s):

    s = s.encode(encoding='ascii', errors='ignore').decode()  # 删除 乱码

    s = re.sub(r"<br />", " ", s)  # 删除 换行标签 <br />
    s = re.sub(r"<\\*\w+>", " ", s)  # 删除 Html 标签
    s = re.sub(r"@\S+", " ", s)  # 删除 @someone
    s = re.sub(r"#\S+", " ", s)  # 删除 #Hashtag
    s = re.sub(r"https://\S+", " ", s)  # 删除 https://website
    s = re.sub(r"www\.\S+", " ", s)  # 删除 www.website
    s = re.sub(r"\'\w+", " ", s)  # 删除 '缩写

    s = re.sub(r"[!~$%^&*()-=_`+{}<>|\[\];:',./?\"\\]+", " ", s)  # 删除 标点符号
    s = re.sub(r"\d+", " ", s)  # 删除 数字
    s = re.sub(r"\s{2,}", " ", s)  # 删除 连续空格
    s = s.strip()  # 删除 两端空格

    return s


"""
* data_preprocess 文本预处理
* Params:
    * s: String 字符串
    * spell_check: Bool 是否进行拼写校对，耗时较长
    * lemmatization: Bool 是否进行词形还原
    * del_stopsword: Bool 是否删除停用词
* Returns:
    * s_list: List(String) 预处理后的字符串列表
"""
def data_preprocess(s, spell_check=True, lemmatization=True, del_stopwords=True):

    # 统一大小写
    s = s.lower()

    # 拼写校对 Spell-check
    if spell_check:
        # t = time.time()
        s = str(TextBlob(s).correct())
        # print("Cost Time of Spell Check: %.3f s" % (time.time() - t))

    s_list = s.split()

    # 词性还原 Lemmatization
    if lemmatization:
        # t = time.time()
        for i in range(len(s_list)):
            s_list[i] = Word(s_list[i]).lemmatize('v')
        # print("Cost Time of Stemming: %.3f s" % (time.time() - t))

    # 删除停用词 Stopwords
    if del_stopwords:
        # t = time.time()
        s_list_wdsw = []
        for word in s_list:
            if word not in Stopwords:
                s_list_wdsw.append(word)
        s_list = s_list_wdsw
        # print("Cost Time of Deleting Stopwords: %.3f s" % (time.time() - t))

    return s_list


"""
* save_data_preprocess  对 IMDB 数据集进行数据清洗和预处理
* Params:
    * src_file: String 原文件路径
    * tar_file: String 保存的目标文件路径
* Returns:
    * tar_file: String 保存的目标文件路径
"""
def save_preprocess_imdb(src_file=None, tar_file=None):
    if tar_file is None:
        tar_file = "./IMDB Dataset Preprocessed.csv"
    if src_file is None:
        src_file = "./IMDB Dataset.csv"

    df = pd.read_csv(src_file)

    def preprocess(s):
        s = data_clean(s)
        # 拼写检查太慢了，实际上没有做
        s_list = data_preprocess(s, spell_check=False, lemmatization=True, del_stopwords=True)
        s = " ".join([word for word in s_list])
        return s

    t = time.time()
    df["sentiment"] = df["sentiment"].map(lambda x: 1 if x == "positive" else 0)
    df["review"] = df["review"].map(preprocess)

    df.to_csv(tar_file, index=False)
    print("Preprocess IMDB File to .csv: %.3f s" % (time.time() - t))
    return tar_file


"""
* load_data_preprocess  载入预处理后的 IMDB 数据集并划分数据
* Params:
    * tar_file: String 数据集路径
    * min_times: Integer 对单词进行编码时，我们将删除出现次数少于 min_times 的单词
* Returns:
    * dir: {}
        * dir["data_train"]  30000 训练样本
        * dir["label_train"] 30000 训练标签
        * dir["data_val"]    10000 验证样本
        * dir["label_val"]   10000 验证标签
        * dir["data_test"]   10000 测试样本
        * dir["label_test"]  10000 测试标签
    * index: Interger 为单词编号的个数
"""
def load_preprocess_imdb(tar_file=None, min_times=50):
    if tar_file is None:
        tar_file = "./IMDB Dataset Preprocessed.csv"
    df = pd.read_csv(tar_file)

    def spilt(s):
        return s.split()
    df["review"] = df["review"].map(spilt)

    wordcount = {}
    for i in range(len(df["review"])):
        for word in df["review"][i]:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1

    word2index = {}
    index = 1

    for key in wordcount:
        if wordcount[key] >= min_times:
            word2index[key] = index
            index += 1

    str_list = list(df["review"])
    w2i_list = []
    for s in str_list:
        index_list = []
        for word in s:
            if word in word2index:
                index_list.append(word2index[word])
        w2i_list.append(index_list)

    dir = {}
    dir["data_train"] = w2i_list[:30000]
    dir["label_train"] = list(df["sentiment"][:30000])
    dir["data_val"] = w2i_list[30000:40000]
    dir["label_val"] = list(df["sentiment"][30000:40000])
    dir["data_test"] = w2i_list[40000:]
    dir["label_test"] = list(df["sentiment"][40000:])
    return dir, index


"""
* word2vec_imdb 生成指定规模的词向量字典，以文件的形式保存
    >>> word2vec_imdb(src_file="./IMDB Dataset Preprocessed.csv", tar_file = "./IMDB Word2Vec m50v300.csv", min_times=50, vec_size=300)
* params:
    * src_file: String 目标文件路径
    * tar_file: String 保存文件路径，以 index，vector 二元组保存每一个单词的词向量
    * min_times: Integer 单词的最小出现次数，若单词出现次数小于 min_times 则被舍弃
    * vec_size: Integer 词向量的长度 
"""
def word2vec_imdb(src_file=None, tar_file=None, min_times=50, vec_size=100):
    if src_file is None:
        src_file = "./IMDB Dataset Preprocessed.csv"
    df = pd.read_csv(src_file)

    if tar_file is None:
        tar_file = "./IMDB Word2Vec.csv"

    def spilt(s):
        return s.split()
    df["review"] = df["review"].map(spilt)

    # 将每一行的评论以 [] of words 的形式存储
    reviews = []
    for r in df["review"]:
        reviews.append(r)

    # 计算所有出现过的单词的词向量
    model = Word2Vec(sentences=reviews, vector_size=vec_size, window=5, min_count=1, workers=4)
    w2v_dir = {}
    for review in reviews:
        for word in review:
            vec = model.wv[word]
            w2v_dir[word] = vec

    # 找出所有出现次数大于 min_times 的词
    wordcount = {}
    for i in range(len(df["review"])):
        for word in df["review"][i]:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1

    # 将候选词的编码序号和对应词向量保存以 [] 形式保存
    word2index = []
    word2vec = []
    index = 1
    for key in wordcount:
        if wordcount[key] >= min_times:
            word2index.append(index)
            word2vec.append(w2v_dir[key])
            index += 1

    # 将候选词结果保存在文件 tar_file 中
    s_vec = []
    z = pd.Series(np.zeros(vec_size))
    s_vec.append(z)
    for w2v in word2vec:
        s_vec.append(pd.Series(w2v))

    data = pd.concat(s_vec, axis=1)
    data = data.T
    print(data.head())
    print(data.shape)
    data.to_csv(tar_file, index=False)
