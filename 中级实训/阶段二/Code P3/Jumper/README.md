# Stage 2 - Part 3 Jumper

* 文件布局

  > * Jumper
  >   * README.md
  >   * Jumper.java       		         // 继承了Actor的类
  >   * JumperRunner.java           // 使用 Jumper 类的程序案例
  >   * JumperTest.java                 // Jumpter 的 JUnit 单元测试代码
  >   * sonar-project.properties  // Sonar 代码检查配置文件

* 将该文件夹移入 GridWorldCode/projects，并在GridWorldCode文件夹启动命令行执行以下命令可以对 Jumper 进行编译运行

  ``` sh
  javac -classpath .:gridworld.jar ./projects/part3_code/Jumper/Jumper.java ./projects/part3_code/Jumper/JumperRunner.java
  
  java -classpath .:gridworld.jar:./projects/part3_code/Jumper JumperRunner
  ```

* 在安装并安装 Sonarqube 和 安装 sonar-scanner 的情况下，将 sonar-project.properties 文件的 login 和 password 修改为你的账户和密码，进入 Jumper 文件夹执行 `sonar-scanner`即可上传到 Sonar 上进行代码评估。
* 代码评估 和 单元测试 结果全部在 testreport.md 文件中。

