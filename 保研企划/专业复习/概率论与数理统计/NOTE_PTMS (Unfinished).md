# 包烟复习：概率论与数理统计

【I just have a book】

## 第一章 基本概念

1. 随机现象、统计规律性、随机试验
2. 样本空间、随机事件：基本事件 必然事件 不可能事件、完备事件组
3. 事件的关系及运算：包含、相等、和、积、差、互斥事件、对立事件
4. 事件的运算律：交换、结合、分配、摩根
5. 概率：非负性、规范性、可列可加性、概率的运算性质
6. 古典概型（等可能概型）、几何概型
7. 条件概率：$P(B|A) = \frac{P(AB)}{P(A)}, P(A) > 0$
8. 乘法公式：$P(A_1...A_n) = P(A_n|A_1...A_{n-1})...P(A_3|A_1A_2)P(A_2A_1)P(A_1)$
9. 全概率公式：$P(A) = \sum_{i=1}^nP(B_i)P(A|B_i)$
10. **贝叶斯公式**：$P(B_i|A) = \frac{P(B_i)P(A|B_i)}{\sum_{j=1}^nP(B_j)P(A|B_j)}$
11. 独立性：$P(AB)=P(A)P(B)$、重复独立试验

## 第二章 随机变量及其分布

> 离散

1. 随机变量、离散型随机变量
2. 分布律：$P(X=x_k)=p_k(k=1,2,...)$
3. 离散随机变量的分布律与事件概率的关系：$P(a<X\le b) = \sum_{a<x_k\le b}p_k$
4. (0-1) 分布：$P(X = 1) = p, P(X = 0) = 1-p$
5. **二项分布**：设在 $n$ 重伯努利试验中事件 $A$ 出现的次数为 $X$，则 $P(X=k)=C_n^kp^{k}(1-p)^{n-k}, k=0,1,...$，称随机变量 $X$ 服从二项分布 $X \sim B(n,p)$
6. **泊松分布**：$P(X=k) = \frac{\lambda^ke^{-k}}{k!}$，记为 $X \sim P(\lambda)$
7. 泊松定理：当 $n$ 足够大时，二项分布可以用泊松分布近似，其中$\lim_{n\to\infty}np_n = \lambda > 0$
8. 超几何分布：$P(X=i) = \frac{C_M^iC_{N-M}^{n-i}}{C_N^n}$，记为 $X \sim H(N,M,n)$，意为从内含 M 件次品的 N 件物品中抽取 $n$ 件物品，$i$ 为抽中的次品数目
9. 几何分布：$P(X=i) = (1-p)^{i-1}p$，记为 $X \sim G(p)$，意为前 $i-1$ 次没有射中，第 $i$ 次才射中的概率
10. **随机变量的分布函数** $F(X) = P(X\le x)$：单调、有界、右连续，$P(a<x\le b)=P(X\le b)-P(x\le a) = F(b) - F(a)$

> 连续

1. 连续性随机变量的**概率密度** $f(x)$ 和**分布函数** $F(X)$：$F(x) = \int_{-\infty}^{x}f(t)dt$，$P(a<x\le b)=P(X\le b)-P(x\le a) = F(b) - F(a) = \int_a^bf(x)dx$
2. 均匀分布：$f(x) = \frac{1}{b-a}, \text{ for } a\le x\le b;f(x) = 0 \text{ for else}$
3. **指数分布**：$f(x) = \lambda e^{-\lambda x}, \text{ for } x > 0;f(x) = 0 \text{ for else}$
4. 指数分布的无记忆性 $\forall x,t > 0, P(X>s+t|X>s) = P(X>t)$
5. **正态分布**：$f(x) = \frac1{\sqrt{2\pi}\sigma}e^{_\frac{(x-\mu)^2}{2\sigma^2}}, x\in(-\infty, +\infty)$，记为 $X\sim N(\mu, \sigma)$，满足 $P(X\le\mu)=P(X>\mu)=\frac12$
6. 标准正态分布：$X\sim N(0,1), \varphi(x) = \frac1{\sqrt{2\pi}}e^{-\frac{x^2}2}$
7. 离散型随机变量的函数的分布计算：$Y=g(X), P(Y=y_j) = \sum_{g(x_k)=y_j}P(X=x_k)$

8. 连续性随机变量的函数的分布计算：
   * $Y = g(X), F_Y(y) = P(Y\le y) = P(g(X)\le y)=\int_{g(x)\le y}f_X(x)dx, f_Y(y)=F_Y'(y)$
   * $Y=g(X),f_Y(y)=f_X[h(y)]|h'(y)|$，$h(y)$ 是 $g(x)$ 的反函数（不严格的版本）

## 第三章 多维随机变量及其分布

1. 二维随机变量
2. **联合分布函数**：$F(x,y)=P(X\le x, Y\le y)$，有$P(x_1\le X\le x_2, y_1 \le Y \le y_2) = F(x_2,y_2)-F(x_1, y_2)-F(x_2, y_1)+F(x_1, y_1)$
3. 二维离散型随机变量：$P(X=x_i,Y=y_i) = p_{ij}$，二维连续型随机变量：$F(x,y) = \int_{-\infty}^x\int_{-\infty}^y f(u,v)dudv$
4. **边缘分布函数**：$F_X(x) = lim_{y\to\infty}F(x,y)=F(x,+\infty)$、$F_Y(y) = lim_{x\to\infty}F(x,y)=F(+\infty,y)$
5. 边缘分布律：$p_{i\cdot}=\sum_{j=1}^\infty p_{ij}=P(X=x_i)$；边缘概率密度：$f_X(x) = \infty_{-\infty}^{+\infty}f(x,y)dy$
6. 二维均匀分布：$f(X,Y)=\frac1A, (x,y)\in G;\text{ else } f(X,Y)=0$
7. 二维正态分布：$(X,Y)\sim N(\mu_1,\sigma_1^2; \,u_2,\sigma_2^2; \rho)$
8. 条件分布律：$P_{X|Y}(i|j) = p(X=x_i|Y=y_j)=\frac{p_{ij}}{p_{\cdot j}}, p_{\cdot j}>0$；条件概率密度：$f_{X|Y}(x|y)=\frac{f(x,y)}{f_Y(y)}$（在 $Y=y$ 条件下随机变量 $X$ 的条件分布）
9. 随机变量相互独立：$F(x,y)=F_X(x)F_Y(y)$，离散型：$p_{ij}=p_{i\cdot}p_{\cdot j}$；连续性：$f(x,y)=f_X(x)f_Y(y)$
10. 二维随机变量的函数的分布

## 第四章 随机变量数字特征

1. **数学期望**：离散型 $E(X) = \sum_kx_kp_k$，要求级数绝对收敛；连续型：$E(X) = \int_{-\infty}^{+\infty}xf(x)dx$，要求积分绝对收敛
2. **方差**：$D(X)=E(X-E(X))^2=E(X^2)-E(X)^2$
3. 二项分布$X\sim B(n,p)$ 数学期望：$E(X)=np$，方差：$np(1-p)$
4. 泊松分布 $X\sim P(\lambda)$，$E(X)=D(X)=\lambda$
5. 几何分布 $E(X)=\frac1p$，$D(X)=\frac{1-p}{p^2}$
6. 正态分布 $X\sim N(\mu, \sigma^2)$，$E(X)=\mu$，$D(X)=\sigma^2$
7. 指数分布 $E(X) = \frac1\lambda$，$D(X)=\frac1{\lambda^2}$
8. 均匀分布 $E(X)=\frac{a+b}2$，$D(X)=\frac{(b-a)^2}{12}$
9. **协方差**：$Cov(X,Y)=E(XY)-E(X)E(Y))$，$D(X\pm Y)=D(X)+D(Y)\pm 2 Cov(X,Y)$
10. **相关系数**：$\rho_{XY}=\frac{Cov(X,Y)}{\sqrt{D(X)}\sqrt{D(Y)}}$，反映了两个随机变量的线性相关程度，范围从-1到1。
    * 若相关系数为 0，则X 和 Y 是不相关的。
    * 若 X 和 Y 相互独立，则相关系数为 0
11. 原点矩：$E(X^kY^l)$ 为 $X$ 和 $Y$ 的 $k+l$ 阶混合原点矩，随机变量 $X$ 的一阶原点矩就是其数学期望
12. 中心距：$E((X-E(X))^k(Y-E(Y))^l)$为 $X$ 和 $Y$ 的 $k+l$ 阶混合中心矩，随机变量 $X$ 的二阶中心矩就是其方差
13. **协方差矩阵**：设 $(X_1,...X_n)$ 为 $n$ 维随机变量，记 $C_{i,j} = Cov(X_i,X_j)$，则矩阵 $C$ 为协方差矩阵

## 第五章 大数定理与中心极限定理

1. **切比雪夫不等式**：对于随机变量 $X$，对任意的 $\epsilon > 0$ 有：
   $$
   P(|X-E(X)|\ge \epsilon) \le \frac{D(X)}{\epsilon^2}
   $$

2. **切比雪夫大数定理**：如果随机变量序列相互独立，各随机变量和方差都有限，而且方差有公共上界，则对任意的 $\epsilon > 0$ 有：
   $$
   \lim_{n\to\infty}(|\frac1n\sum_{i=1}^nX_i -\frac1n\sum_{i=1}^nE(X_i
   )|<\epsilon) = 1
   $$
   定理说明：当 $n$ 充分大时， $n$ 个独立随机变量的平均数的离散程度很小。

3. **中心极限定理**

   

## 第六章 样本及抽样分布



## 第七章 参数估计



## 第八章 假设验证