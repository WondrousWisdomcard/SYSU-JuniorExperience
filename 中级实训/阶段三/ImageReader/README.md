# Stage3 - ImageReader README

**19335286 郑有为**

> **实现说明、运行效果、测试结果请参考 Report.pdf**

### 文件说明

```
 .
 ├── bmptest 测试图片集
 ├── lib
 ├── ImageProcessorTest.java
 ├── ImplementImageIO.java
 ├── ImplementImageProcessor.java
 ├── MyGrayFilter.java
 ├── MyRGBFilter.java
 ├── ImageReader.jar
 ├── README.md
 └── Report.md
```

* **ImplementImageIO.java** 继承 ImageIO 接口，实现`myWrite`和`myRead`方法；
* **ImplementImageProcessor.java** 继承 ImageProcessor 接口，实现`showChanelR`、`showChaelG`、`showChanelB`、`showGray`四个方法；
* **ImageProcessorTest.java** 使用JUnit4的单元测试类，测试`showChanelR`、`showChaelG`、`showChanelB`、`showGray`的生成结果是否与预期一致；
* **MyGrayFilter.java** 过滤器类，继承自 RGBImageFilter 类；
* **MyRGBFilter.java** 过滤器类，继承自 RGBImageFilter 类。

### 编译运行

* 命令行运编译行程序：进入 ImageReader 文件夹输入命令：

  ``` sh
  javac -classpath .:ImageReader.jar ./MyGrayFilter.java ./MyRGBFilter.java ./ImplementImageIO.java ./ImplementImageProcessor.java ./ImageReaderRunner.java
  
  java -classpath .:ImageReader.jar:./ ImageReaderRunner
  ```

* 可以使用 Eclipse 运行程序或运行测试程序。

