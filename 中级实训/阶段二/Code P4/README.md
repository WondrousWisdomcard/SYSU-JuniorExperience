# Stage 2 : Part 4 Readme

**19335286 郑有为**

> 测试和代码评估的结果都在 Report.pdf 中



## ModifiedChameleonCritter

**说明**：在Chameleon类的基础上做的修改，让Chameleon在周围没有Actor时将自己的颜色变暗。

**重写**：重写了`processActors`和`makeMove`方法。

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part4_code/ModifiedChameleonCritter/ModifiedChameleonCritter.java ./projects/part4_code/ModifiedChameleonCritter/ModifiedChameleonCritterRunner.java

java -classpath .:gridworld.jar:./projects/part4_code/ModifiedChameleonCritter ModifiedChameleonCritterRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Pass



## ChemaleonKid

**说明**：继承自ChameleonCritter类，ChameleonKid只能根据正前方或正后方的Actor来改变颜色，如果周围没有Actor则其颜色会慢慢变暗。

**重写**：重写了`getActors`和`getLocationsInDirections`方法。

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part4_code/ChameleonKid/ChameleonCritter.java ./projects/part4_code/ChameleonKid/ChameleonKid.java ./projects/part4_code/ChameleonKid/ChameleonKidRunner.java

java -classpath .:gridworld.jar:./projects/part4_code/ChameleonKid ChameleonKidRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Pass



## RockHound

**说明**：继承自Critter类，能够吃掉周围的石头，其他行为与一般Critter一致。

**重写**：重写了`processActors`方法。

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part4_code/RockHound/RockHound.java ./projects/part4_code/RockHound/RockHoundRunner.java

java -classpath .:gridworld.jar:./projects/part4_code/RockHound RockHoundRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Pass



## BlusterCritter

**说明**：继承自Critter类，会根据周围两格范围内的Actor数来改变自己的颜色，当周围Actor小于c个时颜色变亮，大于等于c个时颜色变暗。

**重写**：重写了`getActors`和`processActors`方法。

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part4_code/BlusterCritter/BlusterCritter.java ./projects/part4_code/BlusterCritter/BlusterCritterRunner.java

java -classpath .:gridworld.jar:./projects/part4_code/BlusterCritter BlusterCritterRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Pass



## QuickCrab

**说明**：继承自CrabCritter类，只能横着走，捕食范围只有眼前三个方向（正前方，左前方，右前方）。QuickCrab一次能向左或向右移动一到二格，移动方向和步数都是随机的，不能越过非空格子，在左右都不能移动时会改变方向。

**重写**：重写了`getMoveLocation`方法。

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part4_code/QuickCrab/CrabCritter.java ./projects/part4_code/QuickCrab/QuickCrab.java ./projects/part4_code/QuickCrab/QuickCrabRunner.java

java -classpath .:gridworld.jar:./projects/part4_code/QuickCrab QuickCrabRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Pass



## KingCrab

**说明**：继承自CrabCritter类，只能横着走，捕食范围只有眼前三个方向（正前方，左前方，右前方），对于“捕食”，KingCrab首先会驱赶周围的Actor使其远离自己，当周围的Actor走投无路时才会被KingCrab吃掉。KingCrab一次能向左或向右移动一格，在左右都不能移动时会改变方向。

**重写**：重写了`processActors`方法。

**运行**：将该文件夹移入 GridWorldCode 的 projects 文件夹，执行以下命令。（也可以直接[下载](https://gitee.com/WondrousWisdomcard/se-training/tree/master/GridWorldCode)）

``` sh
javac -classpath .:gridworld.jar ./projects/part4_code/KingCrab/CrabCritter.java ./projects/part4_code/KingCrab/KingCrab.java ./projects/part4_code/KingCrab/KingCrabRunner.java

java -classpath .:gridworld.jar:./projects/part4_code/KingCrab KingCrabRunner
```

**运行测试**：请参考 Report.pdf

**Sonar测试**：Pass

