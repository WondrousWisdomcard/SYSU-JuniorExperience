% tensorflow_version
1.4
.0
import tensorflow as tf
import matplotlib.pyplot as plt
import time

print(tf.__version__)

from tensorflow.examples.tutorials.mnist import input_data

# 加载MNIST数据集，通过设置 one_hot=True 来使用独热编码标签
# 独热编码：对于每个图片的标签 y，10 位中仅有一位的值为 1，其余的为 0。
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


# 权重正态分布初始化函数
def weight_variable(shape):
    # 生成截断正态分布随机数,shape表示生成张量的维度，mean是均值(默认=0.0)，stddev是标准差。
    # 取值范围为 [ mean - 2 * stddev, mean + 2 * stddev ]，这里为[-0.2, 0.2]
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


# 偏置量初始化函数
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)  # value=0.1, shape是张量的维度
    return tf.Variable(initial)


if __name__ == "__main__":

    # 为训练数据集的输入 x 和标签 y 创建占位符
    x = tf.placeholder(tf.float32, [None, 784])  # None用以指代batch的大小，意即输入图片的数量不定，一张图28*28=784
    y = tf.placeholder(tf.float32, [None, 10])
    # 意思是每个元素被保留的概率，keep_prob=1即所有元素全部保留。大量数据训练时，为了防止过拟合，添加Dropout层，设置一个0~1之间的小数
    keep_prob = tf.placeholder(tf.float32)

    # 创建神经网络第1层，输入层，激活函数为relu
    W_layer1 = weight_variable([784, 500])
    b_layer1 = bias_variable([500])
    h1 = tf.add(tf.matmul(x, W_layer1), b_layer1)  # W * x + b
    h1 = tf.nn.relu(h1)
    # 创建神经网络第2层，隐藏层，激活函数为relu
    W_layer2 = weight_variable([500, 1000])
    b_layer2 = bias_variable([1000])
    h2 = tf.add(tf.matmul(h1, W_layer2), b_layer2)  # W * h1 + b，h1为第1层的输出
    h2 = tf.nn.relu(h2)
    # 创建神经网络第3层，隐藏层，激活函数为relu
    W_layer3 = weight_variable([1000, 300])
    b_layer3 = bias_variable([300])
    h3 = tf.add(tf.matmul(h2, W_layer3), b_layer3)  # W * h2 + b，h2为第2层的输出
    h3 = tf.nn.relu(h3)
    # 创建神经网络第4层，输出层，激活函数为softmax
    W_layer4 = weight_variable([300, 10])
    b_layer4 = bias_variable([10])
    predict = tf.add(tf.matmul(h3, W_layer4), b_layer4)  # W * h3 + b，h3为第3层的输出
    y_conv = tf.nn.softmax(tf.matmul(h3, W_layer4) + b_layer4)
    # 计算交叉熵代价函数
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predict, labels=y))
    # 使用Adam下降算法优化交叉熵代价函数
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    # 预测是否准确的结果存放在一个布尔型的列表中
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))  # argmax返回的矩阵行中的最大值的索引号
    # 求预测准确率
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))  # cast将布尔型的数据转换成float型的数据；reduce_mean求平均值

    # 初始化
    init_op = tf.global_variables_initializer()

    time_start = time.time()
    i_list = []
    train_acc_list = []
    test_acc_list = []

    with tf.Session() as sess:
        sess.run(init_op)
        for i in range(550):  # 训练样本为55000，分成550批，每批为100个样本
            batch = mnist.train.next_batch(100)
            if i % 50 == 0:  # 每过50批，显示其在训练集上的准确率和在测试集上的准确率
                train_accuracy = accuracy.eval(feed_dict={x: batch[0], y: batch[1], keep_prob: 1.0})
                test_accuracy = accuracy.eval(feed_dict={x: mnist.test.images, y: mnist.test.labels})
                print('step %d, training accuracy %g, test accuracy %g' % (i, train_accuracy, test_accuracy))

                if i != 0:
                    i_list.append(i)
                    train_acc_list.append(train_accuracy)
                    test_acc_list.append(test_accuracy)

            # 每一步迭代，都会加载100个训练样本，然后执行一次train_step，并通过feed_dict，用训练数据替代x和y张量占位符。
            sess.run(train_step, feed_dict={x: batch[0], y: batch[1], keep_prob: 0.5})
        # 显示最终在测试集上的准确率
        print(
            'test accuracy %g' % accuracy.eval(feed_dict={x: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0}))

    time_end = time.time()

    plt.plot(i_list, train_acc_list, label="train accuracy")
    plt.plot(i_list, test_acc_list, label="test accuracy")
    plt.legend()
    plt.show()

    print('Totally cost is', time_end - time_start, "s")