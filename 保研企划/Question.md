## 英文问答区

1. 为什么选择中山大学 Sun Yat-Sen University
   * Geographically appropriate
2. 什么是人工智能 ,Artificial In'telligence
   * Artificial intelligence leverages computers and machines to <u>mimic the problem-solving and decision-making capabilities</u> of the human mind.
3. 什么是计算机视觉 Computer Vision
   * Computer vision is a field of artificial intelligence (AI) that enables computers and systems to derive meaningful information from digital images, videos and other visual inputs
4. 什么是人脸检测 Face Detection
5. 什么是人脸识别 Face ,Recog'nition
   * Face recognition is a method of **identifying or verifying the identity of an individual** using their face.
6. 你最喜欢的 C++ 特性？封装 En,capsu'lation
   * With encapsulation, you can present any thing in the real world using the class and object, and you can define their relation and composition, it does help when u code for a large project.
7. 什么是元宇宙 'Metaverse
   * The Metaverse is a collective virtual open space, created by the convergence of virtually enhanced physical and digital reality.
8. 什么是虚拟现实 ,Virtual Re'ality
   * Virtual reality (VR) is a computer-based system that uses software, screens on each eye, and interactive controls to allow a person to enter a virtual, digital world. 
9. 边缘计算 Edge Computing
   * The term Edge computing refers to an architecture rather than a specific technology. Edge computing is <u>a **distributed computing paradigm** that brings computation and data storage closer to the sources of data.</u> 
10. 云计算 Cloud Computing
    * Cloud computing transforms IT **'infrastructure** into a **utility**: It lets you ‘plug into' infrastructure via the internet, and use computing resources <u>without in'stalling and maintaining them on-premises.</u>
11. 强化学习 ,Rein'forcement Learning
    * <u>Reinforcement Learning (RL) is the science of **decision making**. It is about learning the optimal behavior in an environment to obtain maximum reward.</u>
12. 知识图谱 Mapping Knowledge Domain
    * A knowledge graph represents a network of real-world 'entities and illustrates the relationship between them. This information is usually stored in a graph database and visualized as a graph structure, prompting the term knowledge “graph.”
13. 量子计算 Quantum computing
    * Quantum computing is a rapidly-emerging tech'nology that use the **laws of quantum me’chanics** to solve problems too complex for classical computers.

## 基础知识区

1. **数学：数分、离散、概统、线代**
   1. **数分**：
      1. 极限：设 $x_n$ 是一数列，$a$ 是一实数，若对于任意给定的正数 $\epsilon$ ，存在正整数 $N$，当 $n > N$ 时，都有 $|x_n - a| < \epsilon$，则称 $a$ 是数列 $\{x_n\}$ 趋于无穷时的极限
      2. 无穷小量：极限为 0 的数列
      3. 拉格朗日中值定理（微分中值定理）：若 $f(x)$ 在闭区间 $[a,b]$ 上连续，在开区间 $(a,b)$ 上可导，则在 $(a,b)$ 中存在 $\epsilon$ ，使得 $f'(\epsilon) = \frac{f(b) - f(a)}{b - a}$
      4. 微商（极限 $\lim_{\Delta x \to 0}\frac{\Delta y}{\Delta x}$ 存在）、微分（$\Delta y = A\Delta x + o(\Delta x), \Delta x\to 0$）、不定积分（全体原函数）、定积分（黎曼和的极限）、泰勒公式（用多项式近似曲线）
      5. 实数连续性：确界定理（有上界的数集有上确界）、有限覆盖定理（闭区间的覆盖存在有限子覆盖）、紧致性定理（有界数列必有收敛子数列）；实数完备性：柯西收敛原理（$x_n - x_m < \varepsilon$）;可积性
      6. 连续和一致连续：连续（对于一个点：$\lim_{x\to x_0}f(x) = f(x_0)$）；一致连续（对于一个区间：$|x_1-x_2|< d, |f(x_1)-f(x_2)|< \varepsilon$）
      7. 数项级数：无穷项函数相加（正项级数，一般项级数）
      8. 柯西收敛原理：级数收敛的充要条件 $|\sum_{i=1}^pu_{n+i}|<\varepsilon$
      9. 绝对收敛和条件收敛：在 $\sum_{n=1}^\infty u_n$ 收敛的情况下，前者 $\sum_{i=1}^\infty |u_n|$ 也收敛，后者绝对值不收敛
      10. 广义积分（积分区间为无限的积分）、瑕积分（开区间积分，开区间点处函数值无界）
          1. 函数项级数：函数序列（$\{f_n(x)\}$）、一致收敛（$|f_n(x)-f(x)|<\varepsilon$）、和函数（数项级数的和函数）、幂级数（$\sum_{n=0}^\infty a_n(t-t_0)^n$）、傅里叶级数（$\frac{a_0}2 + \sum_{i=1}^\infty(a_n\cos nx+b_n \sin nx)$）
      11. 偏导数（多元函数对一个变量求导）、全微分（$dz|_{p_0} = A\Delta x+B\Delta y$）
      12. 重积分：$\int\int f(x,y)dxdy$
   2. **离散：命题逻辑、一阶逻辑、证明方法、集合、关系、计数与组合、图和树**
      1. 笛卡尔积：$A\times B = \{<a,b>|a\in A \wedge b\in B\}$
      2. 自反（$\forall a \in A, <a,a>\in R$）、反自反（$\forall a \in A, <a,a>\notin R$）、对称、反对称、传递
      3. 闭包：关系的闭包是包含一个关系且满足某个性质的最小关系
      4. 等价关系：自反、对称、传递
      5. 偏序关系：自反、反对称、传递
   3. **概统**：
      1. 贝叶斯公式：$P(B_i|A) = \frac{P(B_i)P(A|B_i)}{\sum_{j=1}^nP(B_j)P(A|B_j)}$
      2. 期望 $E(X) = \sum_kx_kp_k$；方差 $D(X)=E(X-E(X))^2=E(X^2)-E(X)^2$；协方差 $Cov(X,Y)=E(XY)-E(X)E(Y))$
      3. 分布函数 $F(X) = P(X\le x)$、联合分布 $F(x,y)=P(X\le x, Y\le y)$ 、边缘分布 $F_X(x) = lim_{y\to\infty}F(x,y)=F(x,+\infty)$
      4. 大数定理：$\lim_{n\to\infty}(|\frac1n\sum_{i=1}^nX_i -\frac1n\sum_{i=1}^nE(X_i
         )|<\epsilon) = 1$
      5. 中心极限定理：$lim_{n\to\infty}P\{\frac{\sum X_i - n\mu}{\sqrt n \sigma}\le x\} = \Phi(x)$（独立同分布的中心极限定）
      6. 参数估计：（不懂）
         1. 最大似然估计：$L(x_1,x2,...x_n,\theta) = \prod_{i=1}^n p(x_i;\theta)$，计算偏导方程组 $\frac{\part ln(L)}{\part\theta_i} = 0$
      7. 假设验证：（不懂）
      8. 均值和期望的区别：前者针对样本，后者针对随机变量
   4. **线代**：
      1. 向量空间（满足加法封闭和数乘封闭）、列空间（列向量生成的子空间）、零空间（$A x= 0$ 的解组成的空间）
      2. 矩阵的秩：非零子式的最高阶数，矩阵线性独立的纵列的最大数
      3. 线性无关（零空间仅有零向量，秩为阶数）、线性相关
      4. 基：向量空间中一组线性无关的列向量，可生成表示整个向量空间
      5. 行列式：物理意义是列向量长成的盒子的体积*
      6. 特征值、特征向量：满足 $Ax = \lambda x$ 的 $\lambda$/满足 $Ax = \lambda x$ 的 $x$
      7. 正交化：从一组线性无关的向量中求得一组标准正交向量
      8. 对角化：$A = S\Lambda S^{-1}$，$S$ 是特征向量作为列向量组成的矩阵，$\Lambda$ 是对角矩阵（每一个对角元素都是一个特征值）
      9. 投影矩阵、对称矩阵、正定矩阵（特征值均为正数的矩阵）、相似矩阵（$B = M^{-1}AM$）
2. **专必：数据结构、机组、操作系统、计算机网络、数据库**
   1. 操作系统：
      1. 进程：具有独立功能的程序在一个数据集合上运行的过程，他是系统进行资源分配和调度的一个的独立单位。
      2. 线程：线程是轻量级的进程，是一个基本的 CPU 执行单元，也是程序执行流的最小单元。
      3. 同步：亦称直接制约关系，指为了完成某个任务而建立的两个或多个进程，因为需要在某些位置上协调他们的工作次序而等待、传递信息所产生的制约关系。
      4. 互斥：亦称间接制约关系，当一个进程进入临界区时，另一个进程必须等待，直至占用临界资源的进程退出。
      5. 死锁：指多个进程因竞争资源而造成的一种僵局（互相等待），若无外力作用，这些进程将无法向前推进。四个条件：互斥，不剥夺，请求并保持，循环等待
3. **专选：编译原理、区块链、人工智能、NLP、数据挖掘**