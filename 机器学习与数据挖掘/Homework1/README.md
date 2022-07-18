# Readme

## 文件内容

### Code

* ./Classifiers
  * ./softmax_classifier.py 实现线性和非线性分类器
  * ./kernel.py 提供几个简单的基函数
* ./data_utils.py 实现扫描数据文件并进行预处理
* ./visual_utils.py 实现实验结果的可视化工具
* ./test_utils.py 实现交叉验证等测试代码
* ./main.py 主函数，注释代码对应进行相关的测试

### Datasets

* DryBean 数据集 http://archive.ics.uci.edu/ml/datasets/Dry+Bean+Dataset  
* Obesity 数据集  https://archive.ics.uci.edu/ml/datasets/Estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition+#  
* WineQuality 数据集 http://archive.ics.uci.edu/ml/datasets/Wine+Quality  

### Report.pdf

* 实验报告

## 作业要求

**作业题目：**实现并对比线性分类器与非线性分类器

**作业要求：**

1. 实现Lecture 2线性分类器（多类分类采用softmax函数）

2. 通过基函数非线性化步骤1的线性分类器，得到不含正则化的非线性分类器（基函数的选择不限）

3. 通过L1和L2范数分别对步骤2的非线性分类器进行正则化，正则化系数λ=1，分别得到含L1和L2正则化的非线性分类器。

4. 在UCI Machine Learning Repository（https://archive.ics.uci.edu/ml/datasets.php）找到自己认为合适的数据集对比：线性分类器、不含正则化的非线性分类器、含L1正则化的非线性分类器、含L2 正则化的非线性分类器。

5. 对比指标采用分类精度，即报告每一个分类器在测试集$\{(f(\mathbf{x}^{(i)}),y^{(i)}), i=1,\dots,m\}$上得到的ACC

$$
ACC = \frac1m\sum_{i=1}^{m}\delta(f(\mathbf{x}^{(i)}),y^{(i)})
$$

其中$\delta(f(\mathbf{x}^{(i)}),y^{(i)}) = 1$，若$f(\mathbf{x}^{(i)}) = y^{(i)}$；否则为$0$。

6. 提交代码+数据集+详细实验报告及分析（编程语言不限、报告字数不限，需要透彻分析），压缩包提交：学号+姓名。

7. 提交日期：4月8日。提交邮箱：sysumldm2022@163.com