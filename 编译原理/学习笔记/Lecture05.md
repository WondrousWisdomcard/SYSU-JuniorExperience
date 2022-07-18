# 正归文法、正则表达式和有限自动机的相互转化

*  正规文法：左线性文法和右线性文法的总

* 正规表达式、正归文法、有限自动机（NFA，DFA）是等价的

回顾一下上下文无关文法：

* 终端符号集合、非终端符号集合、唯一的开始符号（非终端符号）、若干产生式。

---

首先求出右线性文法，然后转化为等价的正规方程组，最后解此方程组

右线性文法：（大写字母为非终结符号、小写字符表示终结符号）

$A \to aB$

$A \to a$

NFA to 右线性文法

* 为NFA中的每一个状态$i$，创造一个非终端符号$A_i$
* 如果状态$i$存在一个通过符号$a$到状态$j$的转化，新建一个表达式$A_i \to aA_j$，若是通过$\epsilon$到状态$j$的转化，则表达式写$A_i \to A_j$ 
* 如果$i$是一个终结状态，新建表达式$A_i \to \epsilon$
* 如果$i$是一个开始状态，$A_i$成为文法的开始符号

正规方程组的写法：

$\rightarrow$ 变成 $=$，$|$ 变成 $+$

求解方程组运算法则：

$A = aA+ bB + c \Longrightarrow A \to aA | bB | c \Longrightarrow A \to a^*(bB|c)$

$aA + bA = (a+b)A$ 

---

左线性文法和右线性文法的直接转换（S是开始符号）

$A \to aB \Rightarrow B \to Aa$

$A \to a \Rightarrow S \to Aa$

$A \to \epsilon \Rightarrow S \to A$

$S \to Aa \Rightarrow A \to a$

$S \to A \Rightarrow A \to \epsilon$

