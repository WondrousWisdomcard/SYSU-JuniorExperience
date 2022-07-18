## Stage2 - Part2 Report of Coding Exercise

**郑有为 19335286**

> 运行截图请参考 Report.pdf
>
> 所有代码经过 Sonar 代码评估，评估结果请参考 Report.pdf

### 1. CircleBug 

* 命令行编译运行命令：（在GridWorldCode下执行，代码位于`/project/part2_code`）

  ``` sh
  javac -classpath .:gridworld.jar ./projects/part2_code/CircleBug/CircleBug.java ./projects/part2_code/CircleBug/CircleBugRunner.java
  java -classpath .:gridworld.jar:./projects/part2_code/CircleBug CircleBugRunner
  ```


### 2. SpiralBug

* 命令行编译运行命令：（在GridWorldCode下执行，代码位于`/project/part2_code`）

  ``` sh
  javac -classpath .:gridworld.jar ./projects/part2_code/SpiralBug/SpiralBug.java ./projects/part2_code/SpiralBug/SpiralBugRunner.java
  java -classpath .:gridworld.jar:./projects/part2_code/SpiralBug SpiralBugRunner
  ```

* 代码说明：通过以下代码生成一个没有边界的网格

  ``` java
  // @file: SpiralBug/SpiralBugRunner.java
  // @line: 14-15
  Grid<Actor> grid = new UnboundedGrid<Actor>();
  ActorWorld world = new ActorWorld(grid);
  ```


### 3. ZBug

* 命令行编译运行命令：（在GridWorldCode下执行，代码位于`/project/part2_code`）

  ``` sh
  javac -classpath .:gridworld.jar ./projects/part2_code/ZBug/ZBug.java ./projects/part2_code/ZBug/ZBugRunner.java
  java -classpath .:gridworld.jar:./projects/part2_code/ZBug ZBugRunner
  ```


### 4. DancingBug

* 命令行编译运行命令：（在GridWorldCode下执行，代码位于`/project/part2_code`）

  ``` sh
  javac -classpath .:gridworld.jar ./projects/part2_code/DancingBug/DancingBug.java ./projects/part2_code/DancingBug/DancingBugRunner.java
  java -classpath .:gridworld.jar:./projects/part2_code/DancingBug DancingBugRunner
  ```


### 5. Summar

向网格中添加一个 `BoxBug` 的三步骤：

1. 创建 BoxBug 对象：`BoxBug bug = new BoxBug(num)`
2. 为 Bug 对象设置属性，例如颜色：`bug.setColor(Color.xxx)`
3. 创建一个 Location 实例，将 Bug 对象添加到 ActorWorld 实例中： `world.add(new Location(num1, num2), bug);`
