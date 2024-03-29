# Lecture 06 Syntax Analysis I - CFG

* 语法分析的任务：
  * 从词法分析中获得每个属性字（token）在语句中，在整个程序中扮演什么样的角色
  * 检查语句或者程序是否符合程序语言的语法
  * 为解决上两个问题：需要明确一个程序中包含哪些语法成分，这些成分分别以什么方式构成程序
* 解析语法的两种策略：
  * 自顶向下：如何在多个候选项中选出唯一的项（？）
  * 自底向上：如何在句子中找到句柄（？）

* 语法的形式化：**上下文无关文法（CFG）** Content-Free Grammar

  * 四元组定义：$[T,N,S,X]$，分别表示终端符号集合、非终端符号集合、唯一的开始符号（$ S \in N$）、若干产生式（$X \to Y_1Y_2...Y_n, X \in N \cap Y_i \in T \cup N \cup {\epsilon}$）
  * 我们规定第一个产生式左端的非终结符号为开始符号
  * 推导式的简写：$A \to \alpha_1, A \to \alpha_2$可简写为$A \to \alpha_1 | \alpha_2$
  * 与正则表达式/正则文法区分开，CFG比正则表达式更强大

* **推导 Derivation**：从开始符号开始，每一步推导就是用一个产生式的右方取代左端的非终端符号，一直推到只含终端符号。

  * 文法的句子：将开始符号推导出来的只含有终端符号的串
  * $L(G)$ 由文法G定义出来的语言：这个文法的所有句子的集合
  * 最左推导 Leftmost 和最右推导 Rightmost：每步推导都替换最左/右边的非终端符号，可以理解为左结合和右结合

* **分析树 Parse Trees**

* 文法的二义性：一个文法能构造出两棵不同的分析树

  * 用分步（增加非终端符号）的方法来消除二义性，例如以下提升乘法优先级的例子：

    >$E \to E + E | E * E | (E) | id$
    >
    >Change to
    >
    >$E \to E + T | T$
    >
    >$T \to T * F | F$
    >
    >$F \to (E) | id$

  * 有些CFG的文法的二义性是不可消除的
  * 无法证明一个文法是否存在二义性

* **NFA to CFG** （右线性文法？）
  * 为NFA中的每一个状态$i$，创造一个非终端符号$A_i$
  * 如果状态$i$存在一个通过符号$a$到状态$j$的转化，新建一个表达式$A_i \to aA_j$，若是通过$\epsilon$到状态$j$的转化，则表达式写$A_i \to A_j$
  * 如果$i$是一个终结状态，新建表达式$A_i \to \epsilon$
  * 如果$i$是一个开始状态，$A_i$成为文法的开始符号

---

>  课上的例题，想想为什么第一眼想错：
>
> $L = \{0^n1^n|n \ge 1\}$：$S \to 0S1 | 0$1
>
> 01回文串：$S \to 0S0 | 1S1 | 1 | 0 | \epsilon$
>
> 括号匹配串：$S \to (S) | SS | \epsilon$

> 单箭头：产生式定义符号
>
> 双箭头：推导符号

> C语言语法原则：最长串匹配原则 和 就近原则 :fu:
>
> 1+++2 = 1++ + 2 = 3
>
> if then if the else = if then (if then else)

