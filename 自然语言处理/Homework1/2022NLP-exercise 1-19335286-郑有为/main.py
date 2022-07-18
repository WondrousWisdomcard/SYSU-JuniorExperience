import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup
import jieba


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


# 分词程序，返回用"/"号隔开的分词文本
def tokenization(text):
    seg_text = jieba.cut(text, cut_all=False)
    return "/".join(seg_text)


if __name__ == "__main__":

    # 载入自定义字典
    jieba.load_userdict("dict.txt")

    # 获取网页文本
    url = "https://news.ifeng.com/c/8EOcnBCpJir"
    title, content = crawl_news(url)

    # 对标题正文进行分词
    token_title = tokenization(title)
    token_content = tokenization(content)

    # 将结果保存在文件 result.xlsx 中
    data = pd.DataFrame({
        "URL": [url],
        "Title": [token_title],
        "Content": [token_content]
    })
    data.to_excel("./result.xlsx", index=False)


