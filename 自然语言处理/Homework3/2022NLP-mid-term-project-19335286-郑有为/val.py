import sys
import pandas as pd
import os
from model import *
from data_utils import *
from visual_utils import *

with open('./output_val.txt', 'w') as f:
    # 将输出重定向到文件中
    sys.stdout = f

    # 预处理 IMDB 文件
    path= "./"
    imdb_file = path + "IMDB Dataset.csv"
    imdb_pp_file = path + "IMDB Dataset Preprocessed.csv"
    img_dir = path + "Image/"
    model_dir = path + "Model/"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    if os.path.exists(imdb_pp_file):
        print(imdb_pp_file, "already exists.")
    else:
        save_preprocess_imdb(src_file=imdb_file, tar_file=imdb_pp_file)

    # 基本参数
    BATCH_SIZE = 256
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("Device: ", DEVICE)
    # CUDA_LAUNCH_BLOCKING = 1 # 强制串行

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


    # 超参测试 - Min_times 对模型的影响（仅使用 RNN 模型进行验证）
    min_times_list = [5, 10, 30, 50]
    EMB_SIZE = 150
    HID_SIZE = 300

    acc_list = []
    for min_times in min_times_list:
        t = time.time()
        dir, max_words = load_preprocess_imdb(tar_file=imdb_pp_file, min_times=min_times)
        max_words += 1

        x_train = dir["data_train"]
        x_val = dir["data_val"]
        y_train = dir["label_train"]
        y_val = dir["label_val"]
        train_loader = gen_data_loader(x_train, y_train, BATCH_SIZE)
        test_loader = gen_data_loader(x_val, y_val, BATCH_SIZE)

        model = RNNModel(max_words, EMB_SIZE, HID_SIZE, emb_grad=True).to(DEVICE)
        print(model, "\n")
        optimizer = optim.Adam(model.parameters())
        best_acc = 0.0
        for epoch in range(1, 21):
            train(model, train_loader, optimizer, epoch, DEVICE, verbose=False)
            acc = test(model, test_loader, DEVICE, verbose=False)
            if best_acc < acc:
                best_acc = acc
            print("Min_times: {} Epoch: {} Test Acc: {:.4f}, Best Test Acc：{:.4f}".format(min_times, epoch, acc, best_acc))
        acc_list.append(best_acc)
        print("Cost: %.3f s\n" % (time.time() - t))
    show_curve(train=acc_list, xtick=["5", "10", "30", "50"], xlabel="Min_times", ylabel="Acc", path=img_dir, name="min_times_acc")

    # 设计 10 个不同规模的网络: 每个网络都基于W2V模型
    """
        模型     Emb Hid Epo W2V TestAcc ValAcc
    1   RNN     150 300  20  S
    2   RNN     150 300  20  D
    3   RNN     300 500  20  D
    4   LSTM    150 300  20  S
    5   LSTM    150 300  20  D
    6   LSTM    300 500  20  D
    7   BiLSTM  300 300  20  D
    8   GRU     150 300  20  S
    9   GRU     300 300  20  D
    10  GRU     300 500  20  D
    * 注 (S:静态,D:动态)
    """

    # 读取经预处理的数据集
    dir, MAX_WORDS = load_preprocess_imdb(tar_file=imdb_pp_file, min_times=10)
    MAX_WORDS += 1
    x_train = dir["data_train"]
    x_test = dir["data_val"]
    y_train = dir["label_train"]
    y_test = dir["label_val"]

    # 生成DataLoader
    train_loader = gen_data_loader(x_train, y_train, BATCH_SIZE)
    test_loader = gen_data_loader(x_test, y_test, BATCH_SIZE)

    # 结果保存
    model_names = ["RNN1", "RNN2", "RNN3", "LSTM1", "LSTM2", "LSTM3", "BiLSTM", "GRU1", "GRU2", "GRU3"]
    train_acc_list = []
    test_acc_list = []
    loss_list = []

    # 训练函数
    def model_val(model, train_loader, test_loader, optimizer, epoch, device, name):
        print("\nModel:", name)
        train_acc = []
        test_acc = []
        losses = []
        t = time.time()
        best_acc = 0.0
        for e in range(1, epoch + 1):
            losses += train(model, train_loader, optimizer, e, device)
            print("\n")

            t_acc = test(model, train_loader, device)
            acc = test(model, test_loader, device)
            train_acc.append(t_acc)
            test_acc.append(acc)
            if best_acc < acc:
                best_acc = acc
                torch.save(model.state_dict(), (model_dir + name + ".pth"))

            print("Train Acc: {:.4f}".format(t_acc))
            print("Test Acc: {:.4f}, Best Test Acc：{:.4f}\n".format(acc, best_acc))
        print("Total Cost: %.3f s" % (time.time() - t))

        show_curve(train=train_acc, test=test_acc, xlabel="epoch", ylabel="acc", path=img_dir, name=name + "acc")
        show_curve(train=losses, xlabel="epoch", ylabel="loss", path=img_dir, name=name + "loss")

        print("Train Acc:", train_acc)
        print("Test Acc:", test_acc)
        print("Loss:", losses)

        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        loss_list.append(losses)



    # RNN1模型
    model = RNNModel(MAX_WORDS, 150, 300, emb_grad=False, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "RNN1")


    # RNN2模型
    model = RNNModel(MAX_WORDS, 150, 300, emb_grad=True, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "RNN2")


    # RNN3模型
    model = RNNModel(MAX_WORDS, 300, 500, emb_grad=True, emb_weight=emb_weight_300).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "RNN3")


    # LSTM1模型
    model = LSTMModel(MAX_WORDS, 150, 300, emb_grad=False, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "LSTM1")


    # LSTM2模型
    model = LSTMModel(MAX_WORDS, 150, 300, emb_grad=True, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "LSTM2")


    # LSTM3模型
    model = LSTMModel(MAX_WORDS, 300, 500, emb_grad=True, emb_weight=emb_weight_300).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "LSTM3")


    # BiLSTM模型
    model = LSTMModel(MAX_WORDS, 300, 300, emb_grad=True, emb_weight=emb_weight_300, bidirectional=True).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "BiLSTM")


    # GRU1模型
    model = GRUModel(MAX_WORDS, 150, 300, emb_grad=False, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "GRU1")


    # GRU2模型
    model = GRUModel(MAX_WORDS, 150, 300, emb_grad=True, emb_weight=emb_weight_150).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "GRU2")


    # GRU3模型
    model = GRUModel(MAX_WORDS, 300, 500, emb_grad=True, emb_weight=emb_weight_300).to(DEVICE)
    print(model, "\n")
    optimizer = optim.Adam(model.parameters())
    model_val(model, train_loader, test_loader, optimizer, 20, DEVICE, "GRU3")


    show_curves(train=train_acc_list, test=test_acc_list, labels=model_names, xlabel="epoch", ylabel="acc", path=img_dir, name="acc")
    show_curves(train=loss_list, labels=model_names, xlabel="epoch", ylabel="loss", path=img_dir, name="loss")
