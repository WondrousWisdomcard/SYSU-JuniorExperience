# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import os
import requests
import lxml
from bs4 import BeautifulSoup
import jieba
from gensim.models import Word2Vec


# 网页爬虫，提取并返回网页的标题和正文
def crawl_news(url=None):
    if url is None:
        url = "https://news.ifeng.com/c/8EOcnBCpJir"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    f = requests.get(url, headers=headers)
    soup = BeautifulSoup(f.content, 'lxml')
    h1_title = soup.find('h1')
    p_content = soup.find_all('p')

    title = h1_title.string
    content = ""
    for i in p_content:
        content += i.string

    return title, content


# 分词程序，返回用词组列表
def tokenization(text):
    seg_text = jieba.cut(text, cut_all=False)
    return list(seg_text)


# 处理正文内容，划分句子，删除标点符号，生成有以句子为单位的二维数组
def gen_sentences(token_list):
    sentences = []
    sentence = []
    for token in token_list:
        if token == "。":
            sentences.append(sentence)
            sentence = []
        else:
            if token != "、" and token != "“" and token != "”" and token != "，":
                sentence.append(token)
    return sentences


if __name__ == "__main__":

    # 载入自定义字典
    jieba.load_userdict("dict.txt")

    # 获取网页文本
    url = "https://news.ifeng.com/c/8EOcnBCpJir"
    title, content = crawl_news(url)

    # 对标题正文进行分词
    token_title = tokenization(title)
    token_list = tokenization(content)

    # 处理正文内容，划分句子，删除标点符号
    sentences = gen_sentences(token_list)

    # Word2Vec 模型训练
    model = Word2Vec(sentences=sentences, vector_size=50, window=5, min_count=1, workers=4)
    # 增加 Epoch 可以提高相似概率
    model.train(sentences, total_examples=len(sentences), epochs=50)

    # 保存 Word2Vec 训练结果词向量到字典中
    w2v_dir = {}
    for sentence in sentences:
        for word in sentence:
            vec = model.wv[word]
            w2v_dir[word] = vec

    # 保存 Word2Vec 训练结果至 ./word2vec_result.txt
    with open("./word2vec_result.txt", "w+", encoding='utf8') as file:
        for word_key in w2v_dir:
            word_vec = ""
            t = False
            for v in w2v_dir[word_key]:
                if t:
                    word_vec += ", "
                word_vec += str(v)
                t = True
            file.write(word_key + ": " + word_vec + "\n")

    # 查询与 ‘乌克兰’ 最近的十个词
    word = '乌克兰'
    sims = model.wv.most_similar(word, topn=10)

    # 保存最近十词和概率至 ./sim10_result.txt
    with open("./sim10_result.txt", "w+", encoding='utf8') as file:
        for w, p in sims:
            file.write(w + ": " + str(p) + "\n")



