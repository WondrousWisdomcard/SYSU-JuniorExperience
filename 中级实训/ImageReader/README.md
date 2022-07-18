# Stage 03 - ImageReader README

> **实现说明、运行效果、测试结果请参考 Report.pdf**

### 文件说明

```
 .
 ├── ImageProcessorTest.java
 ├── ImplementImageIO.java
 ├── ImplementImageProcessor.java
 ├── MyGrayFilter.java
 ├── MyRGBFilter.java
 ├── sonar-
 ├── README.md
 └── Report.md
```



### 

### 编译运行

* 命令行运编译行程序：进入 ImageReader 文件夹输入命令：

  ``` sh
  javac -classpath .:ImageReader.jar ./MyGrayFilter.java ./MyRGBFilter.java ./ImplementImageIO.java ./ImplementImageProcessor.java ./ImageReaderRunner.java
  
  java -classpath .:ImageReader.jar:./ ImageReaderRunner
  ```

* 可以使用 Eclipse 运行程序或运行测试程序。

