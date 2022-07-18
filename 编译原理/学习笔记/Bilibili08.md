# 第八章 代码优化

[toc]

#### 基本块

![image-20211230135154516](Bilibili08.assets/image-20211230135154516.png)

一个基本块的指令要么都不执行，要么全部执行。

![image-20211230135429736](Bilibili08.assets/image-20211230135429736.png)

![image-20211230135410627](Bilibili08.assets/image-20211230135410627.png)

#### 流图

![image-20211230135605472](Bilibili08.assets/image-20211230135605472.png)

![image-20211230135741009](Bilibili08.assets/image-20211230135741009.png)

### 代码优化

![image-20211230135852123](Bilibili08.assets/image-20211230135852123.png)

![image-20211230135901364](Bilibili08.assets/image-20211230135901364.png)

#### 删除公共子表达式

![image-20211230135945795](Bilibili08.assets/image-20211230135945795.png)

#### 删除无用代码

![image-20211231001958308](Bilibili08.assets/image-20211231001958308.png)

#### 常量合并 Constant Folding

![image-20211231002213660](Bilibili08.assets/image-20211231002213660.png)

#### 代码移动

![image-20211231002302819](Bilibili08.assets/image-20211231002302819.png)

#### 强度削弱 Strength Reduction

![image-20211231002450807](Bilibili08.assets/image-20211231002450807.png)

#### 删除归纳变量 Induction Variable

![image-20211231002728788](Bilibili08.assets/image-20211231002728788.png)

### 基本块的优化（局部优化）

#### 基本块的DAG表示

![image-20211231003801104](Bilibili08.assets/image-20211231003801104.png)

#### 基于基本块的DAG删除无用代码

![image-20211231100632467](Bilibili08.assets/image-20211231100632467.png)

#### DAG：数组元素赋值指令的表示

![image-20211231100917719](Bilibili08.assets/image-20211231100917719.png)

![image-20211231100955259](Bilibili08.assets/image-20211231100955259.png)

#### DAG重构基本块

![image-20211231101342620](Bilibili08.assets/image-20211231101342620.png)

#### 例题

![image-20211231101639136](Bilibili08.assets/image-20211231101639136.png)

![image-20211231101957514](Bilibili08.assets/image-20211231101957514.png)

### 数据流分析（全局优化）

![image-20211231102131790](Bilibili08.assets/image-20211231102131790.png)

![image-20211231102252021](Bilibili08.assets/image-20211231102252021.png)

![image-20211231102558190](Bilibili08.assets/image-20211231102558190.png)

#### 到达定值分析

![image-20211231102737452](Bilibili08.assets/image-20211231102737452.png)

![image-20211231103239738](Bilibili08.assets/image-20211231103239738.png)

![image-20211231103404340](Bilibili08.assets/image-20211231103404340.png)

#### 到达定值方程的传递函数和数据流方程

![image-20211231103606020](Bilibili08.assets/image-20211231103606020.png)

![image-20211231103716800](Bilibili08.assets/image-20211231103716800.png)

![image-20211231103908020](Bilibili08.assets/image-20211231103908020.png)

![image-20211231104104871](Bilibili08.assets/image-20211231104104871.png)

![image-20211231104306615](Bilibili08.assets/image-20211231104306615.png)

![image-20211231105100828](Bilibili08.assets/image-20211231105100828.png)

![image-20211231105128489](Bilibili08.assets/image-20211231105128489.png)

#### 引用定值链 UD链 Use-Definition

![image-20211231105330054](Bilibili08.assets/image-20211231105330054.png)

#### 活跃变量分析 

![image-20211231110558337](Bilibili08.assets/image-20211231110558337.png)

![image-20211231111006092](Bilibili08.assets/image-20211231111006092.png)

![image-20211231111046710](Bilibili08.assets/image-20211231111046710.png) 

#### 活跃变量的传递函数和数据流方程

![image-20211231111255626](Bilibili08.assets/image-20211231111255626.png)

![image-20211231111657453](Bilibili08.assets/image-20211231111657453.png)

![image-20211231111851019](Bilibili08.assets/image-20211231111851019.png)

![image-20211231111903463](Bilibili08.assets/image-20211231111903463.png)

![image-20211231112610528](Bilibili08.assets/image-20211231112610528.png)

![image-20211231112659144](Bilibili08.assets/image-20211231112659144.png)

#### 定值-引用链 DU链 Definition Use

![image-20211231113002885](Bilibili08.assets/image-20211231113002885.png)

#### 可用表达式的分析

![image-20211231113220402](Bilibili08.assets/image-20211231113220402.png)

（区分语句、变量、表达式）

![image-20211231113351680](Bilibili08.assets/image-20211231113351680.png)

![image-20211231113554524](Bilibili08.assets/image-20211231113554524.png)

#### 可用表达式的传递函数和数据流方程

![image-20211231113813093](Bilibili08.assets/image-20211231113813093.png)

![image-20211231114143289](Bilibili08.assets/image-20211231114143289.png)

![image-20211231114234170](Bilibili08.assets/image-20211231114234170.png)

![image-20211231114723971](Bilibili08.assets/image-20211231114723971.png)

![image-20211231114736328](Bilibili08.assets/image-20211231114736328.png)

#### 支配节点

![image-20211231115244586](Bilibili08.assets/image-20211231115244586.png)

![image-20211231115501184](Bilibili08.assets/image-20211231115501184.png)

![image-20211231115601398](Bilibili08.assets/image-20211231115601398.png)

#### 支配节点的数据流方程

![image-20211231115745046](Bilibili08.assets/image-20211231115745046.png)

![image-20211231115824157](Bilibili08.assets/image-20211231115824157.png)

![image-20211231120146245](Bilibili08.assets/image-20211231120146245.png)

#### 回边

![image-20211231120254323](Bilibili08.assets/image-20211231120254323.png)

#### 自然循环及识别

![image-20211231134119593](Bilibili08.assets/image-20211231134119593.png)

![image-20211231135433421](Bilibili08.assets/image-20211231135433421.png)

![image-20211231135825166](Bilibili08.assets/image-20211231135825166.png)

![image-20211231140024487](Bilibili08.assets/image-20211231140024487.png)

### 全局优化的几种实现方法

#### 删除全局公共子表达式

![image-20211231140910986](Bilibili08.assets/image-20211231140910986.png)

#### 删除复制语句

![image-20211231141233757](Bilibili08.assets/image-20211231141233757.png)

#### 代码移动

![image-20211231141620601](Bilibili08.assets/image-20211231141620601.png)

![image-20211231141703578](Bilibili08.assets/image-20211231141703578.png)

![image-20211231142413678](Bilibili08.assets/image-20211231142413678.png)

![image-20211231142504130](Bilibili08.assets/image-20211231142504130.png)

![image-20211231142613352](Bilibili08.assets/image-20211231142613352.png)

![image-20211231142704817](Bilibili08.assets/image-20211231142704817.png)

#### 作用于归纳变量的强度削弱

![image-20211231143113649](Bilibili08.assets/image-20211231143113649.png)

![image-20211231143241573](Bilibili08.assets/image-20211231143241573.png)

![image-20211231143358737](Bilibili08.assets/image-20211231143358737.png)

![image-20211231144036961](Bilibili08.assets/image-20211231144036961.png)

#### 归纳变量的删除

![image-20211231144240666](Bilibili08.assets/image-20211231144240666.png)

![image-20211231144455820](Bilibili08.assets/image-20211231144455820.png)

（测试是判断的意思，例如判断他是否大于十）

![image-20211231144640406](Bilibili08.assets/image-20211231144640406.png)
