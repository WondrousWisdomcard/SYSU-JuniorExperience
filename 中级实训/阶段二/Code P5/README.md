# Stage 2 : Part 5 Readme

**19335286 郑有为**

> 测试和代码评估的结果都在 Report.pdf 中



## 1 - SparseBoundedGrid

**说明**：使用稀疏矩阵实现一个有界网格，稀疏矩阵由一个行数组组成，行数组每一个元素是该行的一个非空格子，每一行的非空单元信息以链表的形式连接在一起。（详细说明和问题回答请参考 Report.pdf）

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part5_code/1/SparseGridNode.java ./projects/part5_code/1/SparseBoundedGrid.java ./projects/part5_code/1/SparseBoundedGridRunner.java

java -classpath .:gridworld.jar:./projects/part5_code/1 SparseBoundedGridRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Passed



## 2 - SparseBoundedGrid (HashMap)

**说明**：使用一格哈希表结构来储存非空的格子，实现方式与UnboundedGrid大体一致，在UnboundedGrid的基础上对行数和列数进行了约束。（详细说明和问题回答请参考 Report.pdf）

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part5_code/2/SparseBoundedGrid.java ./projects/part5_code/2/SparseBoundedGridRunner.java

java -classpath .:gridworld.jar:./projects/part5_code/2 SparseBoundedGridRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Passed



## 3 - DynamicUnboundedGrid

**说明**：使用数组来实现无界网格（要求行和列的索引大于等于0），策略是首先创建一个16*16的网格，如果在插入时超出这个范围，则扩大网格，重新分配一个行数和列数都为原来的两倍的网格。（详细说明和问题回答请参考 Report.pdf）

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part5_code/3/DynamicUnboundedGrid.java ./projects/part5_code/3/DynamicUnboundedGridRunner.java

java -classpath .:gridworld.jar:./projects/part5_code/3 DynamicUnboundedGridRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Passed

