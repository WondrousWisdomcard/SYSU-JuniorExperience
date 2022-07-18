# Bilibili is future - 4 语法分析

看视频的截图，助理解

[toc]

## 一、自顶向下

### 1. 最右推导和最左规约

![9c3e2b93450f4a32b75b21ef5387c69](Bilibili04.assets/1.png)

### 2. 左递归的问题所在

![a3e79855fa73b1b6eeebd6d0a8d6b51](Bilibili04.assets/2.png)

### 3. 消除左递归的直观理解

![e478b6bd2671aa0b4f2a46516f5256b](Bilibili04.assets/3.png)

### 4. 消除间接左递归

![9a7b39ac318e92b4bfeb236243131ca](Bilibili04.assets/4.png)

### 5. 提取左公因子来推迟决定

![3a374d95abe37c1e0a209c47640cb66](Bilibili04.assets/5.png)

### 6. S 文法（不重要）

![9a561fcb7012078382c127a461b6d8c](Bilibili04.assets/6.png)

### 7. 自顶向下推导例子

![57457a696f06901987bf6135727a6af](Bilibili04.assets/7.png)

### 8. Q 文法（不重要）

![ee4b47796996e913805232f9dfffb11](Bilibili04.assets/8.png)

### 9. FIRST / FOLLOW / SELECT 三件套

![83a166edb93227ce793e1d6e3e65e3f](../../../AppData/Local/Temp/WeChat Files/83a166edb93227ce793e1d6e3e65e3f.png)

### 10. LL(1) 文法的定义

![b04cd2fc66f4b070cb9b144d1c5f9cb](Bilibili04.assets/10.png)

### 11. 计算 FIRST 集合

![99d415eb4cf5b49aed13ab3fa8baca5](Bilibili04.assets/11.png)

### 12. 计算 FOLLOW 集合

![7f87c4ca536b68a24e1069faf95dd79](Bilibili04.assets/12.png)

### 13. 计算 SELECT 集

![f3f25a207b83cb7a7c4e5788ca694c0](Bilibili04.assets/13.png)

### 14. 做一个预测分析表

![9aad690596a63aff7b55fba379d89a8](Bilibili04.assets/14.png)

### 15. 递归预测分析法

![](Bilibili04.assets/15.png)

### 16. 非递归预测分析法

![12e4989fd4be7c4fddaf5db48b83b24](Bilibili04.assets/16-1.png)

![f958799e4a07e331d84dfecc1e73765](Bilibili04.assets/16-2.png)

### 17. 预测分析实现步骤

![de221079f601f186ad4c309827beddf](Bilibili04.assets/17.png)

### 18. 预测分析法的错误恢复和实例

![2f826b30449f35f52c974b5e77e04e9](Bilibili04.assets/18-1.png)

![cb7c6c922c324a0e99cb502aacb61e5](Bilibili04.assets/18-2.png)

![86e2d3a861913dcd744b0dda7a1e682](Bilibili04.assets/18-3.png)

## 二、自底向上

### 1. 自底向上的语法分析概述

![9b77abdf1a4bd40ad0035968d278957](Bilibili04.assets/19.png)

### 2. 移入-规约分析举例

![64f433dbe43e2a03aa117a39f7e5ea8](Bilibili04.assets/20.png)

![b597040c92f259858b4a64093180741](Bilibili04.assets/20-2.png)

### 3. LR分析概述

![3daaaf665b4306534e8a9a2b753795a](Bilibili04.assets/21.png)

### 4. LR分析法的状态

![54b13d538a132b01715f514c25e3668](Bilibili04.assets/22.png)

### 5. LR分析法的结构：ACTION + GOTO

![3a6aeca04f44f9a436777c432911199](Bilibili04.assets/23.png)

### 6. LR分析器的工作过程（注意符号栈状态栈的动态变化）

![491327787a6f4d1eed9702fd17f3cd7](Bilibili04.assets/24.png)

![8c9ae3312c87c5a808f67d8ca0ff6c0](Bilibili04.assets/24-2.png)

![7f940bcc7bbc3b9da7b3aadc7b6b547](Bilibili04.assets/24-3.png)

![3c1abf4fa4a114395b9b72522defbd3](Bilibili04.assets/24-4.png)

### 7. LR(0)中项目的概念

![a14c7e0d6297905ede92d722dc9e121](Bilibili04.assets/25.png)

### 8. 增广文法

![29e6cff1da244918527b097d49756f7](Bilibili04.assets/26.png)

### 9. LR(0) 文法中的项目

![96581609fee278574f9850fdaa49270](Bilibili04.assets/27.png)

![9804c906e5cf8e3b4ee9d21f2cefb64](Bilibili04.assets/27-2.png)

![1db4acd14bc3c167a10d944f6ed2c0b](Bilibili04.assets/27-3.png)

### 10. 计算 CLOSURE() 函数

![e8b5e6a8019e3a6256c6ec303070470](Bilibili04.assets/28.png)

### 11. 计算 GOTO() 函数

![0616d1ffc6760bccd62eee9b4c4229c](Bilibili04.assets/29.png)

### 12. 构造规范 LR(0) 项集族

![ ](Bilibili04.assets/30.png)

### 13. 构造 LR(0) 分析表

![e8f98a8de9ce088635576905f4e2635](Bilibili04.assets/31.png)

### 14. 移入/规约冲突和规约/规约冲突

![5f2bb16a6aacb1d362f22ade5c72da2](Bilibili04.assets/32.png)

### 15. SLR分析法基本思想（FOLLOW）

![fabcb0afddefe9f2f9bd9c2eaea3b95](Bilibili04.assets/33.png)

### 16. 构造 SLR 分析表

![73bdb5983383477b0426306a1887aba](Bilibili04.assets/34.png)

### 17. LR(1) 项目

![8cbffd6cfdc6265d26994c098c88fbb](Bilibili04.assets/35.png)

![79cc482f5ddc01e875306d7a76d4954](Bilibili04.assets/35-2.png)

![fb3a910bad799bf67aa8412b187135f](Bilibili04.assets/35-3.png)

![0a7ebc8f2aa2cbee2f3a3590ca629ab](Bilibili04.assets/35-4.png)

### 18. LALR 规约-规约冲突

![db81f8a84007c08ad1c9b2548aaafd2](Bilibili04.assets/36.png)

### 19. 恐慌模式与短语层析错误恢复

![89189d38e9f3e1ec9b0a55cf497a00a](Bilibili04.assets/37.png)

![c20601fa871cd75cd9737625b37691b](Bilibili04.assets/37-2.png)

![bdda19c37dc5cd243d316ff26fb309b](Bilibili04.assets/37-3.png)

![808843cf2634bc50d7814153abd586b](Bilibili04.assets/37-4.png)

![c3886e2af908f1442c9af42f396f224](Bilibili04.assets/37-5.png)

