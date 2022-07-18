# Stage1 代码说明

**郑有为 19335286**

### 文件目录

``` 
 ├── HelloWorld
 │   └── src 		// 源代码文件夹
 │   └── lib 		// 编译运行所需类库
 │   └── test 		// 生成类文件夹
 │   └── build.xml	// Ant 自动编译XML文件
 │   └── sonar-project.properties // Sonar 代码评估配置文件
 ├── Calculator
 │   └── src 		// 源代码文件夹
 │   └── lib 		// 编译运行所需类库
 │   └── test 		// 生成类文件夹
 │   └── build.xml	// Ant 自动编译XML文件
 │   └── sonar-project.properties // Sonar 代码评估配置文件
 ├── README.md
```

### HelloWorld程序

* 程序功能：在命令行输出"HelloWorld"
* 程序组成：`HelloWorld.java`类和测试类`TestHelloWorld.java`
* 编译运行说明：
  * 编译：进入文件夹`/HelloWorld`命令行输入`ant compile`，自动通过`ant`进行编译
  * 编译并运行：进入文件夹`/HelloWorld`命令行输入`ant run`，自动通过`ant`进行运行
  * 单元测试：进入文件夹`/HelloWorld`命令行输入`ant test`，自动通过`ant`进行单元测试，测试框架为 JUnit
  * 代码评估：安装 SonarQube 和 SonarScanner，配置 SONAR_HOME 和 PATH 环境变量，启动 SonarQube 服务器后修改`/HelloWorld`中`sonar-project`文件中的账号和密码，命令行输入`sonar-scanner`来进行代码评估，评估结果位于`localhost:9000`。

### Calculator程序

* 程序功能：创建一个简单的图形界面计算器，进行加减乘除的计算并输出结果
* 程序组成：`Calculator.java`类和测试类`Calculator.java`
* 编译运行说明：
  * 编译：进入文件夹`/Calculator`命令行输入`ant compile`，自动通过`ant`进行编译
  * 编译并运行：进入文件夹`/Calculator`命令行输入`ant run`，自动通过`ant`进行运行
  * 单元测试：进入文件夹`/Calculator`命令行输入`ant test`，自动通过`ant`进行单元测试，测试框架为 JUnit
  * 代码评估：安装 SonarQube 和 SonarScanner，配置 SONAR_HOME 和 PATH 环境变量，启动 SonarQube 服务器后修改`/Calculator`中`sonar-project`文件中的账号和密码，命令行输入`sonar-scanner`来进行代码评估，评估结果位于`localhost:9000`。

