# Stage3 - MazeBug README

**19335286 郑有为**

> **实验要求、实现说明、运行效果、测试结果等请参考 Report.pdf**

### 文件说明

```
 .
 ├── MazeBug.java  MazeBug实现类
 ├── MazeBugRunner.java
 ├── README.md
 └── Report.pdf
```

### 编译运行

本过程涉及girdworld.jar的打包，使用命令行操作。

* **第一步：打包 jar**

  * 用 MazeBug 文件夹下的 WorldFrame.java 和” WorldFrameResources.properties 替换 GridWorldCode/framework/info/gridworld/gui 下面的对应的文件

  * 将我们编写好的 MazeBug.java 加入到 framework/info/gridworld/maze/ 文件夹中

    * 注意 gridworld 文件夹本来是没有 maze 文件夹的，需要自己创建。

    * 同时确保 MazeBug.java（**编写完成的代码**） 文件包含 package 信息，即文件第一行：

      ``` java
      package info.gridworld.maze;
      ```

    * 这时候我们没有必要把 Runner 文件放进 jar 里

  * 在 GridWorldCode 文件夹下打开命令行，输入 `ant clean` 清空之前的生成结果，在使用`ant`生成 gridworld.jar 文件，新生成的 gridworld.jar 文件保存在 GridWorldCode/dist/GridWorldCode/ 文件夹里， 我们将他替换掉 GridWorldCode/ 下的 gridworld.jar（编译运行时会使用该 jar 文件）

* **第二步：安放Runner文件**

  * 将 MazeBugRunner 放在 projects/maze 文件夹下，在这里，我们删去了它的 package 信息，即删掉：

    ```
    package info.gridworld.maze;
    ```

    因为不将它打包进 jar 里，路径也不对，没必要。

* **第三步：编译运行**

  * 在 GridWorldCode 文件夹下打开命令行，执行：

    ``` java
    javac -classpath .:gridworld.jar ./projects/maze/MazeBugRunner.java 
    java -classpath .:gridworld.jar:./projects/maze MazeBugRunner
    ```

* **第四步：修改代码**

  * 若修改了 MazeBug.java 需要重新完成第一步、第三步骤。
