<center><h1>期中作业：IMDB电影评论文本分类</h1></center>

| 课程：自然语言处理 | 年级专业：19级软件工程 |
| ------------------ | ---------------------- |
| 姓名：郑有为       | 学号：19335286         |

[toc]

## 一、实验总览

IMDB 数据集包含了 50000 条电影评论和它们对应的情感标签（积极或消极），在本实验中，我们的任务是训练出一个结合 Word2Vec 的循环神经网络模型，对电影评论进行文本分类。

**算法的流程**包括以下步骤：

1. **数据预处理部分**
   1. **文本清洗**：操作包括删除乱码、标点、Html标签、数字等与文本情感无关的噪音。
   2. **文本预处理**：操作包括统一字母的大小写，进行词形还原，删除停用词和进行拼写校对。
   3. **创建Word2Vec字典**：统计数据集出现的词汇，筛除少见词，对词语进行编号，并通过Word2Vec模型计算出对应的词向量。
2. **模型验证部分**
   1. 对删除少见词时引入的超参数 Min_times 进行验证。
   2. 我们给出了 10 个不同规模的网络，通过在验证集上验证，我们为每一个网络选出合适的 Epoch，避免模型过拟合，并效选出效果最为出色的网络模型。
3. **模型测试部分**：使用测试集数据测试模型的效果。

**运行环境**：Cuda。神经网络代码基于 Pytorch 库。

**项目文件说明**：

* `/Image` 文件夹，保存所有可视化结果
* `/Model` 文件夹，保存训练好的模型参数
* `data_utils.py` 数据预处理封装代码
* `visual_utils.py` 数据可视化封装代码
* `model.py` 神经网络模型代码
* `val.py` 验证代码
* `test.py` 测试代码
* `output_val.txt` 验证程序输出结果
* `output_test.py` 测试程序输出结果

注：由于 IMDB 数据集比较大，所有中间处理结果文件（包括文本清洗后的文件、Word2Vec编码文件）并没有提交，但可以通过代码重新生成这些文件。

## 二、数据预处理

### 2.1 文本清洗

文本清洗的内容包括：

* 限定编码方式为 ASCII ，删除乱码、中文、Emoji 等；
* 删除 Html 标签和 换行标签`<br />`，Html 标签考虑：`<...>` 和 `<\...>` 两种格式；
* 删除 @ 指定，例如 @ZhangSan，显然 @ 他人不包含情绪信息；
* 删除 # 标签，例如 #Movie；
* 删除 URL，考虑以 `https://` 和 `www.` 开头的 URL；
* 删除缩写，例如删除 `you're` 保留 `you`，`I'll` 保留 `I；`
* 删除标点符号；
* 删除数字，和删除标点符号做到删除日期、时间；
* 删除开头、结尾的空格和中间连续的空格。

文本清洗实现：`data_utils.py` 的 `data_clean(s)` 函数

文本清洗举例：

``` python
from data_utils import data_clean
s = "Hello, 你好 @China, Today is 2022.5.19, it's a nice day ⭐ #HelloMorning !!!!    "
print(data_clean(s))
```

* 输入："Hello, 你好 @China, Today is 2022.5.19, it's a nice day ⭐ #HelloMorning !!!!    "
* 输出："Hello Today is it a nice day"

### 2.2 文本预处理

文本预处理的内容包括：

* 统一字母大小写
* 拼写校对：基于 TextBlob 库的 `correct` 函数，耗时较长
* 词形还原：例如将动词的过去式和过去分析替换为动词一般时态
* 删除停用词：基于 nltk 库的停用词集合，通过`nltk.download('stopwords')` 下载

文本预处理实现：`data_utils.py` 的 `data_preprocess(s, spell_check=True, lemmatization=True, del_stopwords=True)` 函数

* 其中 `spell_check`，`lemmatization`，`del_stopwords` 是可选参数，即拼写校对、词形还原、停用词删除都是可选选项。

文本预处理举例：

``` python
from data_utils import data_clean, data_preprocess
s = "Hello, 你好 @China, Today is 2022.5.19, it's a nice day ⭐ #HelloMorning !!!! I did nothing last day, and cats are so cutee!"
print(data_preprocess(data_clean(s)))
```

* 输入："Hello, 你好 @China, Today is 2022.5.19, it's a nice day ⭐ #HelloMorning !!!! I did nothing last day, and cats are so cutee!"
* 输出：['hello', 'today', 'nice', 'day', 'nothing', 'last', 'day', 'cat', 'cut']，这里删除了停用词 `is`、`it`、`a`、`so` 等，将`cats`变为了单数、`cutee`改成了`cut`。

### 2.2 Word2Vec

Word2Vec采用`gensim.models`库的`Word2Vec`跟据数据集文本生成词向量，并将生成的词向量按找每一个词的索引依次拼接在一起，组成一个矩阵保存在文件中，该矩阵可以用来直接替换循环神经网络中的 Embedding 层，也可以作为 Embedding 层参数的初始化，训练时进行梯度计算。

实现于`data_utils.py`的`word2vec_imdb(src_file=None, tar_file=None, min_times=50, vec_size=100)`函数，可以指定词向量的长度`vec_size`，和少用词剔除的参数`min_times`，生成结果保存在`tar_file`文件中。

生成结果举例：

源文本：

```c
s = “one”
```

生成的词向量（vec_size=150, min_times=150）: 

```c
[-1.921392560005188,2.9480791091918945,1.182746171951294,-1.9803478717803955,-1.2230794429779053,...,-0.795309841632843]
```

## 三、模型训练

### 3.1 Min_times 超参测试

我们在预处理时对单词进行了少见词剔除，即单词在数据集中出现次数少于 Min_times 的单词被剔除，以除去错别字、西语等非英语单词。为了找到较为合适的 Min_times 值，我们选择 5， 10， 30， 50 进行测试，测试基于 Embedding Size = 100，Hidden Size = 200 的 RNN 网络。

测试结果如下图所示，实验表明在 Min_times = 10 时训练效果最好。输出结果储存在`_output.py`中。

![](./Image/min_times_acc.jpg)

### 3.2 网络结构设计

网络结构如下：

```
Model(
  (Embedding): 嵌入层，用词向量矩阵填充，大小为[max_word, emb_size]
  (RNN/LSTM/GRU)：循环神经层，大小为[emb_size, hid_size]
  (avg_pool)：平均池化层
  (fc2): 全连接层，大小为[hid_size, 2]
) 
```

梯度计算采用：Adam 方法；Batch Size：256；Epochs：20。

为了对比不同模型的效果，给出以下一共十个网络进行验证测试。其中，我们在 RNN 1、LSTM 1、GRU 1三个网络中不对 Embedding 层进行梯度计算，即固定该层的值为 Word2Vec 矩阵，其他网络则对 Embedding 曾进行梯度计算。验证网络分为两种规模：Emb_size，Hid_size 为 [150, 300] 和 [300, 500]。

| 模型 | Embedding Size | Hidden Size | Grad For Embedding |
| ---- | -------------- | ----------- | ------------------ |
| **RNN 1** | 150      | 300     | False       |
| **RNN 2** | 150      | 300     | True        |
| **RNN 3** | 300      | 500     | True        |
| **LSTM 1** | 150      | 300     | False       |
| **LSTM 2** | 150      | 300     | True        |
| **LSTM 3** | 300      | 500     | True        |
| **BiLSTM** | 300      | 300     | True        |
| **GRU 1** | 150      | 300     | False       |
| **GRU 2** | 300      | 300     | True        |
| **GRU 3** | 300      | 500     | True |

### 3.3 网络训练结果

在实验时我们发现使用Word2Vec模型来初始化Embedding层能够明显加快收敛速度。

我们选用数据集前三万条作为训练集，再选择第三万到四万条作为验证集，得到的训练结果如下；输出结果储存在`_output.py`中。

注：下表 Train Acc 值 Val Acc 取得最高时的 Train Acc

| 模型       | Train Acc | Best Val Acc | Best Epoch | Train Time Per Epoch |
| ---------- | --------- | ------------ | ---------- | -------------------- |
| **RNN 1**  | 0.8556    | 0.8494       | 6          | 12.47秒              |
| **RNN 2**  | 0.9140    | **0.8772**   | 4          | 12.53秒              |
| **RNN 3**  | 0.8852    | 0.8618       | 2          | 22.45秒              |
| **LSTM 1** | 0.9463    | 0.8848       | 4          | 40.82秒              |
| **LSTM 2** | 0.9448    | 0.8888       | 4          | 42.16秒              |
| **LSTM 3** | 0.9754    | **0.8963**   | 5          | 91.30秒              |
| **BiLSTM** | 0.9884    | 0.8830       | 7          | 48.10秒              |
| **GRU 1**  | 0.8957    | 0.8861       | 6          | 20.85秒              |
| **GRU 2**  | 0.9247    | 0.8957       | 3          | 21.29秒              |
| **GRU 3**  | 0.9784    | **0.8975**   | 4          | 50.23秒              |

|      | RNN 1 (20 Epochs)         | RNN 2 (20 Epochs)         | RNN 3 (20 Epochs)         |
| ---- | ------------------------- | ------------------------- | ------------------------- |
| Acc  | ![](./Image/RNN1acc.jpg)  | ![](./Image/RNN2acc.jpg)  | ![](./Image/RNN3acc.jpg)  |
| Loss | ![](./Image/RNN1loss.jpg) | ![](./Image/RNN2loss.jpg) | ![](./Image/RNN3loss.jpg) |

|      | LSTM 1 (15 Epochs)         | LSTM 2 (10 Epochs)         | LSTM 3 (10 Epochs)         | BiLSTM (10 Epochs)          |
| ---- | -------------------------- | -------------------------- | -------------------------- | --------------------------- |
| Acc  | ![](./Image/LSTM1acc.jpg)  | ![](./Image/LSTM2acc.jpg)  | ![](./Image/LSTM3acc.jpg)  | ![](./Image/BiLSTMacc.jpg)  |
| Loss | ![](./Image/LSTM1loss.jpg) | ![](./Image/LSTM2loss.jpg) | ![](./Image/LSTM3loss.jpg) | ![](./Image/BiLSTMloss.jpg) |

|      | GRU 1 (10 Epochs)         | GRU 2 (10 Epochs)         | GRU 3 (10 Epochs)         |
| ---- | ------------------------- | ------------------------- | ------------------------- |
| Acc  | ![](./Image/GRU1acc.jpg)  | ![](./Image/GRU2acc.jpg)  | ![](./Image/GRU3acc.jpg)  |
| Loss | ![](./Image/GRU1loss.jpg) | ![](./Image/GRU2loss.jpg) | ![](./Image/GRU3loss.jpg) |

通过观察上述十个网络的损失函数和准确率变化，我们得到以下结论：

1. 对 Embedding 层进行梯度计算的效果优于直接用 Word2Vec 固定 Embedding 层，且多出的时间开销可接受。
2. 对于参数同规模的三种类型网络，耗时最高的是 LSTM，其次是 GRU，RNN 计算最快。
3. RNN 的最佳准确率在 88% 以下，而LSTM 和 GRU 能够高于 88%，但都低于 90%
4. RNN 在训练过程中表现出不稳定，容易产生较大的波动，导致准确率突降。
5. 对比 RNN2、RNN3，发现模型越大效果不一定越好。RNN2b 的参数虽然只是 [Emb size:150, Hid: 300]，但训练结果优于 RNN3（[Emb size:300, Hid: 500]），并且在时间上快出一倍。
6. 相比于 RNN， LSTM 和 GRU 能够更快地达到收敛、过拟合，经过 20 个 Epoch 的训练，LSTM 和 GRU 能几乎完全拟合训练集，达到近 100% 的准确率，但在第 3 - 5 个 Epoch 已经开始出现过拟合。

## 四、实验结果分析

跟据验证集结果调整超参，最后在 RNN / LSTM / GRU 中选出三个性能较好的网络，将数据集的第 40000 - 50000 个样本作为测试集，在测试集上进行测试，结果如下表所示。输出结果储存在`_output_test.py`中。

| 模型       | Embedding Size | Hidden Size | Grad For Embedding | Test Acc   |
| ---------- | -------------- | ----------- | ------------------ | ---------- |
| **RNN 2**  | 150            | 300         | True               | **0.8817** |
| **LSTM 3** | 300            | 500         | True               | **0.9017** |
| **GRU 3**  | 300            | 500         | True               | **0.8988** |

## 五、实验总结

本次实验围绕 IMDB 数据集情感分类问题，我们掌握并实现了文本数据集的数据清洗方法和文本预处理策略，结合 Word2Vec 模型和循环神经网络训练出几个分类模型，初步体验神经网络训练、验证和测试过程。实验最后选取三个不同类型（RNN、LSTM、GRU）、不同规模的网络，分别能达到 88.17%、90.17%、89.88% 的正确率。

