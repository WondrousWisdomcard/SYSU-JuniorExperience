import sys
import pandas as pd
import os
from model import *
from data_utils import *
from visual_utils import *

with open('output_test.txt', 'w') as f:
    # 将输出重定向到文件中
    sys.stdout = f

    # 预处理 IMDB 文件
    path= "./"
    imdb_file = path + "IMDB Dataset.csv"
    imdb_pp_file = path + "IMDB Dataset Preprocessed.csv"
    img_dir = path + "Image/"
    model_dir = path + "Model/"
    if os.path.exists(imdb_pp_file):
        print(imdb_pp_file, "already exists.")
    else:
        save_preprocess_imdb(src_file=imdb_file, tar_file=imdb_pp_file)

    # 基本参数
    BATCH_SIZE = 256
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("Device: ", DEVICE)
    CUDA_LAUNCH_BLOCKING = 1

    # 生成 Word2Vec 结果，并将结果保存至文件中
    file1 = path + "IMDB Word2Vec m10v150.csv"
    file2 = path + "IMDB Word2Vec m10v300.csv"
    t = time.time()
    if os.path.exists(file1):
        print(file1, "already exists.")
    else:
        word2vec_imdb(src_file=imdb_pp_file, tar_file=file1, min_times=10, vec_size=150)

    if os.path.exists(file2):
        print(file2, "already exists.")
    else:
        word2vec_imdb(src_file=imdb_pp_file, tar_file=file2, min_times=10, vec_size=300)
    print("Generate Word2Vec Cost: %.3f s" % (time.time() - t))

    # 载入 Word2Vec 编码结果
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)
    emb_weight_150 = data1.values
    emb_weight_300 = data2.values

    # 读取经预处理的数据集
    dir, MAX_WORDS = load_preprocess_imdb(tar_file=imdb_pp_file, min_times=10)
    MAX_WORDS += 1
    x_train = dir["data_train"]
    x_test = dir["data_test"]
    y_train = dir["label_train"]
    y_test = dir["label_test"]

    # 生成DataLoader
    train_loader = gen_data_loader(x_train, y_train, BATCH_SIZE)
    test_loader = gen_data_loader(x_test, y_test, BATCH_SIZE)

    def model_test(model, test_loader, device, name):
        print("\nModel:", name)
        best_acc = 0.0
        acc = test(model, test_loader, device)
        print("Test Acc: {:.4f}\n".format(acc, best_acc))


    # RNN1模型
    model = RNNModel(MAX_WORDS, 150, 300, emb_grad=False, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "RNN1.pth"))
    model_test(model, test_loader, DEVICE, "RNN1")


    # RNN2模型
    model = RNNModel(MAX_WORDS, 150, 300, emb_grad=True, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "RNN2.pth"))
    model_test(model, test_loader, DEVICE, "RNN2")


    # RNN3模型
    model = RNNModel(MAX_WORDS, 300, 500, emb_grad=True, emb_weight=emb_weight_300).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "RNN3.pth"))
    model_test(model, test_loader, DEVICE, "RNN3")


    # LSTM1模型
    model = LSTMModel(MAX_WORDS, 150, 300, emb_grad=False, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "LSTM1.pth"))
    model_test(model, test_loader, DEVICE, "LSTM1")


    # LSTM2模型
    model = LSTMModel(MAX_WORDS, 150, 300, emb_grad=True, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "LSTM2.pth"))
    model_test(model, test_loader, DEVICE, "LSTM2")


    # LSTM3模型
    model = LSTMModel(MAX_WORDS, 300, 500, emb_grad=True, emb_weight=emb_weight_300).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "LSTM3.pth"))
    model_test(model, test_loader, DEVICE, "LSTM3")


    # BiLSTM模型
    model = LSTMModel(MAX_WORDS, 300, 300, emb_grad=True, emb_weight=emb_weight_300, bidirectional=True).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "BiLSTM.pth"))
    model_test(model, test_loader, DEVICE, "BiLSTM")


    # GRU1模型
    model = GRUModel(MAX_WORDS, 150, 300, emb_grad=False, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "GRU1.pth"))
    model_test(model, test_loader, DEVICE, "GRU1")


    # GRU2模型
    model = GRUModel(MAX_WORDS, 150, 300, emb_grad=True, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "GRU2.pth"))
    model_test(model, test_loader, DEVICE, "GRU2")


    # GRU3模型
    model = GRUModel(MAX_WORDS, 300, 500, emb_grad=True, emb_weight=emb_weight_300).to(DEVICE)
    print(model, "\nLoad Params...")
    model.load_state_dict(torch.load(model_dir + "GRU3.pth"))
    model_test(model, test_loader, DEVICE, "GRU3")
