import time

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import RandomSampler, DataLoader, TensorDataset, SequentialSampler


"""
RNN 模型
"""
class RNNModel(nn.Module):
    """
    * max_words 单词的编号的最大数
    * emb_size Embedding层的规模
    * hid_size RNN隐藏层的归模
    * emb_grad Bool 是否求 Embedding 层梯度，为 False 时标识 Embedding 层参数固定
    * emb_weight 二维矩阵，初始化Embedding层参数
    """
    def __init__(self, max_words, emb_size, hid_size, emb_grad=True, emb_weight=None):
        super().__init__()
        self.max_words = max_words
        self.emb_size = emb_size
        self.hid_size = hid_size
        self.emb_grad = emb_grad
        # Embedding层 - RNN层 - 全连接层
        self.Embedding = nn.Embedding(self.max_words, self.emb_size)
        self.RNN = nn.RNN(self.emb_size, self.hid_size, num_layers=1, batch_first=True)
        self.fc2 = nn.Linear(self.hid_size, 2)

        # 初始化 Embedding 层参数权值
        if emb_weight is not None:
            w = torch.Tensor(emb_weight)
            self.Embedding.weight = torch.nn.Parameter(w)

    def forward(self, x):
        if self.emb_grad:
            x = self.Embedding(x)
        else:
            with torch.no_grad():
                x = self.Embedding(x)

        x, _ = self.RNN(x)
        x = F.avg_pool2d(x, (x.shape[1], 1)).squeeze()
        out = self.fc2(x)
        return out


"""
LSTM 模型
"""
class LSTMModel(nn.Module):
    """
    * max_words 单词的编号的最大数
    * emb_size Embedding层的规模
    * hid_size LSTM隐藏层的归模
    * emb_grad Bool 是否求 Embedding 层梯度，为 False 时标识 Embedding 层参数固定
    * emb_weight 二维矩阵，初始化Embedding层参数
    * bidirectional 双向LSTM
    """
    def __init__(self, max_words, emb_size, hid_size, bidirectional=True, emb_grad=True, emb_weight=None):
        super().__init__()
        self.max_words = max_words
        self.emb_size = emb_size
        self.hid_size = hid_size
        self.emb_grad = emb_grad
        # Embedding层 - LSTM层 - 全连接层
        self.Embedding = nn.Embedding(self.max_words, self.emb_size)
        self.LSTM = nn.LSTM(self.emb_size, self.hid_size, num_layers=1, batch_first=True, bidirectional=bidirectional)
        if bidirectional:
          self.fc2 = nn.Linear(self.hid_size * 2, 2)
        else:
          self.fc2 = nn.Linear(self.hid_size, 2)

        # 初始化 Embedding 层参数权值
        if emb_weight is not None:
            w = torch.Tensor(emb_weight)
            self.Embedding.weight = torch.nn.Parameter(w)

    def forward(self, x):
        if self.emb_grad:
            x = self.Embedding(x)
        else:
            with torch.no_grad():
                x = self.Embedding(x)

        x, _ = self.LSTM(x)
        x = F.avg_pool2d(x, (x.shape[1], 1)).squeeze()
        out = self.fc2(x)
        return out


"""
GRU 模型
"""
class GRUModel(nn.Module):
    """
    * max_words 单词的编号的最大数
    * emb_size Embedding层的规模
    * hid_size GRU隐藏层的归模
    * dropout Droupout层Droupout的比例
    * emb_grad Bool 是否求 Embedding 层梯度，为 False 时标识 Embedding 层参数固定
    * emb_weight 二维矩阵，初始化Embedding层参数
    """
    def __init__(self, max_words, emb_size, hid_size, emb_grad=True, emb_weight=None):
        super().__init__()
        self.max_words = max_words
        self.emb_size = emb_size
        self.hid_size = hid_size
        self.emb_grad = emb_grad
        # Embedding层 - GRU层 - 全连接层
        self.Embedding = nn.Embedding(self.max_words, self.emb_size)
        self.GRU = nn.GRU(self.emb_size, self.hid_size, num_layers=1, batch_first=True)
        self.fc2 = nn.Linear(self.hid_size, 2)

        # 初始化 Embedding 层参数权值
        if emb_weight is not None:
            w = torch.Tensor(emb_weight)
            self.Embedding.weight = torch.nn.Parameter(w)

    def forward(self, x):
        if self.emb_grad:
            x = self.Embedding(x)
        else:
            with torch.no_grad():
                x = self.Embedding(x)

        x, _ = self.GRU(x)
        x = F.avg_pool2d(x, (x.shape[1], 1)).squeeze()
        out = self.fc2(x)
        return out


"""
* test 模型测试
* params:
  * model nn.Module 训练好的模型
  * train_loader DataLoader 可以通过 gen_data_loader 生成
  * optimizer 计算梯度
  * epoch Integer 训练的Epoch次数
  * device String 'cpu' or 'cuda'
* return:
  * losses [] of Double 训练过程中的损失函数
"""
def train(model, train_loader, optimizer, epoch, device, verbose=True):
    losses = []
    model.train()
    loss_func = nn.CrossEntropyLoss()
    for step, (x, y) in enumerate(train_loader):
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        y_ = model(x)
        loss = loss_func(y_, y)
        loss.backward()
        optimizer.step()

        if verbose and ((step + 1) % 10 == 0):
            print('Train Epoch:{} [{:0>5d}/{} ({:0>2.0f}%)]\tLoss:{:.6f}'.format(
                epoch, step * len(x), len(train_loader.dataset),
                100. * step / len(train_loader), loss.item()
            ))
            losses.append(loss.item())
    return losses


"""
* test 模型测试
* params:
  * model nn.Module 训练好的模型
  * test_loader DataLoader 可以通过 gen_data_loader 生成
  * device String 'cpu' or 'cuda'
* return:
  * acc Double 准确率
"""
def test(model, test_loader, device, verbose=True):
    model.eval()
    loss_func = nn.CrossEntropyLoss(reduction='sum')
    test_loss = 0.0
    acc = 0

    for step, (x, y) in enumerate(test_loader):
        x, y = x.to(device), y.to(device)
        with torch.no_grad():
            y_ = model(x)
        test_loss += loss_func(y_,y)
        pred = y_.max(-1, keepdim=True)[1]
        acc += pred.eq(y.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    if verbose:
      print('Test Average loss:{:.4f}, Accuracy:{:0>2.0f}% ({:0>5d}/{})'.format(
          test_loss, 100 * acc / len(test_loader.dataset), acc, len(test_loader.dataset)
      ))

    return acc / len(test_loader.dataset)


"""
* gen_data_loader 生成 DataLoader
* params:
  * data: [] of [] 样本数据
  * labels: [] of Interger 样本标签
* return:
  * loader: DataLoader
"""
def gen_data_loader(data, label, batch_size=128):
    data = pad_sequence([torch.from_numpy(np.array(x)) for x in data], batch_first=True).long()
    # 将数据转为 Tensor
    dataset = TensorDataset(torch.LongTensor(data), torch.LongTensor(label))
    sampler = RandomSampler(dataset)
    # 将数据放入 DataLoader
    loader = DataLoader(dataset, sampler=sampler, batch_size=batch_size)
    return loader



