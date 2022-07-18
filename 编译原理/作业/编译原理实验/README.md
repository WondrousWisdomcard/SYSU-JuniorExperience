# 编译原理实验

**19335286 郑有为**

[toc]

## 〇. 文件说明

* **`code_la` 词法分析实验，含代码及实验报告**
* **`code_ga` 语法分析实验，含代码及实验报告**
* **`code_sa`语义分析及中间代码生成实验，含代码及实验报告**

​		三个文件的内容是递进关系，内容也不断完善。在写 sa 的时候，为了适应要求，会修改和完善不以前少 ga 和 la 的代码（例如 sa 阶段给语法分析树做了可视化图）

​		**最后的内容以sa的代码和报告为准。**（./sa_code/README.md）

* `resource` 一些参考资料
* `demo` 一些 Lec 和 Yacc 的Demo

## Ⅰ. 作业要求

* **词法分析实验**
  * 实验目的：为扩展TINY语言TINY+构造词法分析程序。
  * 实验内容：了解样例语言及编译器的实现，用C语言构造词法分析程序。
  * 实验要求：将TINY+源程序翻译成对应的TOKEN序列，并能检查一定的词法错误。
  * ![](image/词法分析实验.png)
  * **实验报告：[词法分析](./code_la/README.md)**
* **语法分析实验**
  * 实验目的：为扩展语言TINY+构造语法分析程序，从而掌握语法分析程序的构造方法。
  * 实验内容：用EBNF描述TINY+的语法，构造TINY+语法分析器。
  * 实验要求：将TOKEN序列转换成语法分析树，并能检查移动的语法错误。
  * ![](image/语法分析实验.png)
  * **实验报告：[语法分析](./code_ga/README.md)**
* **语义分析及中间代码生成实验**
  * 实验目的：构造TINY+的语义分析程序并生成中间代码。
  * 实验内容：构造符号表，构造TINY+语义分析器，构造TINY+的中间代码生成器。
  * 实验要求：能检查一定的语义错误，将TINY+程序转换为三地址中间代码。
  * 提交词法分析、语法分析和语义分析程序和中间代码生成的实验报告。
  * ![](image/语义分析和中间代码生成实验.png)
  * **实验报告：[语义分析及中间代码生成](./code_sa/README.md)**

## Ⅱ. 更新日志

**[20211203] 已经使用 Lex 对词法分析进行重写，接下来的语法分析实验将建立在这份重写的词法分析实验的基础上完成。**

**[20211210] 修改词法分析定义**：

* **区分字符和字符串**，分别用 string 和 char 表示，string 用双引号包住，char 用单引号包住
* 增加一个**取非标识符**：**not**，优先级高于与运算

**[20211212] 完成语法分析程序**

**[20211218] 修改语法分析程序**

* 修改语法树节点数据结构

* **逗号和分号**不再加入语法分析树中
* **语法分析树的可视化**（基于pydotplus，需要 python 环境）

**[20211218] 完成语义分析器**

**[20211219] 完成中间代码生成器**

**[20211220] 修改Goto指令的Bug**

## Ⅲ. 词法定义

参考C语言、老师的资料和华南理工的TINY+实验，以下给出TINY+的词法定义：

**关键字定义**如下，区分大小写，共 20 个。

| or         | and       | int      | float     | bool     | char      |
| ---------- | --------- | -------- | --------- | -------- | --------- |
| **while**  | **do**    | **if**   | **then**  | **else** | **end**   |
| **repeat** | **until** | **read** | **write** | **true** | **false** |
| **string** | **not**   |          |           |          |           |

**操作符定义**如下，也称为特殊符号，共 16 个。

| >     | <=    | >=    | <     | {     | }     | **=** | :=    |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **+** | **-** | ***** | **/** | **(** | **)** | **,** | **;** |

**其他词法**

| 标识       | 正则表达式（Lex语法）                           | 注释                                                     |
| ---------- | ----------------------------------------------- | -------------------------------------------------------- |
| DIGIT      | `[0-9]`                                         |                                                          |
| LETTER     | `[A-Za-z]`                                      |                                                          |
| DIGITS     | `[0-9][0-9]*`                                   |                                                          |
| **ID**     | `{LETTER}({LETTER}|{DIGIT})*`                   | 标识符，以字母开头，可包含数字                           |
| **INT**    | `[+-]?({DIGIT})+`                               | 整数，如+0，-5，100                                      |
| **FLOAT**  | `[+-]?{DIGITS}"."{DIGITS}`                      | 浮点数，如-0.14                                          |
| **CHAR**   | `'[^']'`                                        | 字符，如`'a'`                                            |
| **STRING** | `\"[^\n\"]*\"`                                  | 如`"Hi"`，不可跨行，不可嵌套                             |
| **注释**   | `"/*".*"*/"`或`"/*"([^\n"*/"]*\n)*"*/"		` | 如 `/*Hi*/` ，可跨行，不可嵌套，其内容会被词法分析器忽略 |

## Ⅳ. 语法定义

* TOKEN列表（%left 约束了优先级，越在后面的优先级越高）：

  ```
  %token INT FLOAT CHAR STRING BOOL ID
  %token WHILE DO IF THEN ELSE END REPEAT UNTIL
  %token READ WRITE
  %token TRUE FALSE
  %token TYPE
  %token LE GE ASSIGN
  %token ',' ';' '(' ')' '{' '}' '<' '>'
  
  %left '+' '-'
  %left '*' '/'
  
  %left OR
  %left AND
  %left NOT
  ```

* EBNF描述语法（Yacc格式）：

  | 编号 | 产生式                                                       | 注释                                                         |
  | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | 1    | **program**: declarations stmt \| stmt                       | **程序（program）**<br >由**声明部分（declarations）**和**语句部分（stmt）**组成，变量声明需要在语句部分之前完成。 |
  | 2    | **declarations**: declaration ';' \| declaration ';' declarations | **声明部分（declarations）**<br >由若干条**声明（declaration）**组成，声明部分可以为空。 |
  | 3    | **declaration**: TYPE varlist                                | **声明（declaration）**<br >由**变量类型（TYPE）**和**变量列表（varlist）**组成。 |
  | 4    | **varlist**: ID \| ID ',' varlist                            | **变量列表（variable_list）**<br >由若干个**标识符（ID）**组成，标识符之间由**逗号（,）**隔开。 |
  | 5    | **stmt**: xstmt ';' \|  xstmt ';' stmt                       | **语句序列（stmt）<br >**由若干**语句块（xstmt）**组成，标识符之间由**分号（;）**隔开。 |
  | 6    | **xstmt**: WHILE boolexp DO stmt END                         | **循环语句块（while-stmt）<br >**有固定格式，包含关键字 ***while***，条件判断表达式和关键字 ***do***、***end*** |
  | 7    | **xstmt**: IF boolexp THEN stmt ELSE stmt END \| IF boolexp THEN stmt END | **条件判断语句块（if-stmt）<br >**有固定格式，包含关键字 ***if***，条件判断表达式和关键字 ***then***、***end***，其中***else***是可选项。 |
  | 8    | **xstmt**: REPEAT stmt UNTIL boolexp                         | **重复语句块（repeat-stmt）<br >**有固定格式，包含关键字 ***repeat***， ***until*** 和条件判断表达式，逻辑上类似于C语言的 *do while* 。 |
  | 9    | **xstmt**: ID ASSIGN exp                                     | **赋值环语句块（assign-stmt）<br >**由**标识符（ID）**、**赋值符号（:=）**、**表达式（exp）**组成。 |
  | 10   | **xstmt**: READ ID                                           | **读入语句块（read-stmt）**<br >从某个地方读入一个**标识符（ID） ** |
  | 11   | **xstmt**: WRITE exp                                         | **写入语句块（write-stmt）**<br >写入一个**表达式（exp）**   |
  | 12   | **exp**: arithmeticexp \| boolexp \| strexp                  | **表达式（exp）<br >**有三种不同的类型**（x-exp）**，包括算术表达式、布尔表达式和字符串表达式。 |
  | 13   | **arithmeticexp**: INT \| FLOAT \| ID \| '(' arithmeticexp ')' \| arithmeticexp '+' arithmeticexp \| arithmeticexp '-' arithmeticexp \| arithmeticexp '*' arithmeticexp \| arithmeticexp '/' arithmeticexp | **算术表达式（arithmetric_exp）**<br >可以是整形、浮点数、标识符，也可以是加减乘除运算。 |
  | 14   | **boolexp**: BOOL \| comparison \| '(' boolexp ')' \| NOT boolexp \| boolexp AND boolexp \| boolexp OR boolexp | **布尔表达式（bool_exp）**<br >定义为比较表达式，布尔型遍历或逻辑与或非运算。 |
  | 15   | **comparison**: arithmeticexp '>' arithmeticexp \| arithmeticexp '<' arithmeticexp \| arithmeticexp '=' arithmeticexp \| arithmeticexp GE arithmeticexp \| arithmeticexp LE arithmeticexp | **比较表达式（comparison）**<br >含小于、等于、大于、小于等于、大于等于。 |
  | 16   | **strexp**: CHAR \| STRING                                   | **字符表达式（strexp）**<br >为字符变量或字符串变量          |

* 语法分析树举例：

  ![](code_sa/out/tree7.png)

## Ⅴ. 语义说明

* **生成符号表**：根据变量声明部分的内容构建一个符号表
* **变量检查**：所有变量必须在使用前声明，且每个变量只能声明一次
* **类型检查**：声明变量、变量赋值和做比较时，要考虑运算符两边变量类型是否一致。
* **强制类型转换**：必要时进行强制类型转换。（INT -> FLOAT）

## Ⅵ. 三地址码定义

| 序号 | 指令形式              | 注释                                                |
| ---- | --------------------- | --------------------------------------------------- |
| 1    | ***x = y op z***      | 双目运算符赋值指令                                  |
| 2    | ***x = op y***        | 单目运算符赋值指令                                  |
| 3    | ***x = y***           | 值复制指令                                          |
| 4    | ***goto L***          | 跳转指令，下一步从标号为 ***L*** 的指令开始执行     |
| 5    | ***if-not x goto L*** | 条件转移指令（为了简化实现选用了 if-not 而不是 if） |
| 6    | ***read x***          | 输入 ***x***                                        |
| 7    | ***write x***         | 写出 ***x***                                        |
| 8    | ***Label L***         | 声明一个标号 ***L***                                |

## Ⅶ. 语义规则(含中间代码生成)

* **相关属性：**

  ```c
  enum SymbolType type;   // 节点类型 
  // 中间代码生成
  int t_id; // 临时变量编号 （ID的临时编号为-1）
  char code[BUF_SIZE];
  int next; // L 属性
  ```

以下为伪代码，具体实现参考 `ga.y`。

* `program: declarations stmt | program: stmt`

  ```c
  strcpy($$->code, $2->code);
  UpdateNext(root, root->code); // root 是数根节点
  ```

* **变量声明部分**：

  * `declarations: declaration ';' | declaration ';' declarations `

    ``` c
    // Do nothing
    ```

  * `declaration: TYPE varlist`

    ```c
    // 生成符号表
    updateSymbolTable($$);
    ```

  * `varlist: ID | ID ',' varlist `

    ``` c
    // Do Nothing
    ```

* **条件循环语句**：

  * `stmt: xstmt ';'`

    ``` c
    $$->code = $1->code;
    ```

  * `stmt: xstmt ';' stmt`

    ``` c
    $1->next = newLabel(); // L 属性赋初始值的地方
    $$->code = $1->code || Label $1->next || $3->code
    ```

  * **`xstmt: IF boolexp THEN stmt ELSE stmt END`**

    ``` c
    int fabegin = newLabel();
    $$->code = $2->code || "If-not _t($2->t_id) Goto Label fabegin" || $4->code || Goto $$->next || Label fabegin || $6->code
    ```

  * **`stmt: IF boolexp THEN stmt END `**

    ``` c
    $$->code = $2->code || "If-not _t($2->t_id) Goto Label $$->next" || $4->code
    ```

  * **`stmt: WHILE boolexp DO stmt END`**

    ``` c
    int begin = newLabel();
    $$->code = Label begin || $2->code || "If-not _t($2->t_id) Goto Label $$->next" || $4->code || Goto begin
    ```

  * **`stmt: REPEAT stmt UNTIL boolexp`**

    ``` c
    int begin = newLabel();
    $$->code = Label begin || $2->code || $4->code || "If-not _t($4->t_id) Goto $$->next || Goto Label begin"
    ```

  * **`stmt: ID ASSIGN exp`**

    ```c
    checkID($1); // 检查 ID 是否在符号表中
    checkType($1, $3, 2); // 检查类型是否匹配
    
    $$->code = $3->code || "$1->name = $3->name"
    ```

  * **`stmt: READ ID`**

    ``` C
    checkID($2); // 检查 ID 是否在符号表中
     $$->code = "Read $2->name"
    ```

  * **`stmt: WRITE exp`**

    ``` c
    $$->code = $2->code || "Write $2->name"
    ```

* **算术运算：**

  * **`arithmeticexp: INT | FLOAT`** 

    ``` c
    setNodeType($$, st_int); // 设置节点类型(FLOAT 时为 st_float)
    $$->t_id = newTempID();	// 申请一个临时变量
    sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
    ```

  * **`arithmeticexp: ID`**

    ``` c
    checkID($1); // 检查 ID 是否在符号表中
    setNodeType($$, $1->type); // 设置节点类型
    ```

  * **`arithmeticexp: '(' arithmeticexp ')' `**

    ``` c
    setNodeType($$, $2->type); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
    $$->code = $2->code || "$$->t_id = $2->t_id" 
    ```

  * **`arithmeticexp: arithmeticexp '+' arithmeticexp`** (加减乘除)

    ``` c
    checkType($1, $3, 1); // 检查类型是否匹配
    setNodeType($$, $1->type); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
    $$->code = $3->code || $1->code || "$1->t_id + $3->t_id"
    ```

* **条件运算**：

  * `boolexp: BOOL`

    ``` c
    setNodeType($$, st_bool); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
    sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
    ```

  * `boolexp: comparison `

    ``` c
    setNodeType($$, st_bool); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
    $$->code = $1->code || "$$->t_id = $1->t_id" 
    ```

  * `boolexp: '(' boolexp ')' `

    ``` c
    setNodeType($$, st_bool); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
    $$->code = $2->code || "$$->t_id = $2->t_id" 
    ```

  * `boolexp: NOT boolexp `

    ``` c
    setNodeType($$, st_bool); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
    $$->code = $2->code || "$$->t_id = not $2->t_id" 
    ```

  * `boolexp: boolexp AND boolexp | boolexp OR boolexp `

    ``` c
    setNodeType($$, st_bool); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
     $$->code = $1->code || $3->code || "$$->t_id = $1->t_id AND(OR) $3->t_id" 
    ```

* **比较运算**：

  * `arithmeticexp '>' arithmeticexp` （包括小于，等于，大于，大于等于，小于等于）

    ``` c
    setNodeType($$, st_bool); // 设置节点类型
    $$->t_id = newTempID();	// 申请一个临时变量
    $$->code = $1->code || $3->code || "$$->name = $1->name > $3->name" 
    ```

* **字符和字符串：**

  * `strexp: CHAR | STRING`

    ``` c
    $$->t_id = newTempID(); // 申请一个临时变量
    sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
    ```

## Ⅷ. 实验心得

​		终于完成了编译原理的三次实验，通过实验，更加深刻的理解了正则表达式、EBNF和语义规则的设计，整个过程是一个循循渐进的过程，在已完成的代码的基础上进行完善，不断修改。

​		因为老师没有给一份”固定“的TINY+，而是要我们自己优化，所以我结合多方资料和自己的理解，进行了词法、语法、语义、中间代码的设计，相比于一般的程序设计语言还是差别很多，首先没有考虑数组、函数调用、变量显示类型转化等等。

​		最开始，我没有使用 Lex 而是手写词法分析实验，考虑到之后写语法分析和语义分析实验要基于以前的代码，于是我就学 Lex 和 Yacc 并重写了代码。使用 Lex 和 Yacc 比直接编写方便太多，而且它们还提供各种方便的实现，例如定义优先级和异常检测上，简化了编程。

​		虽然使用 Yacc 写语法分析和语义分析方便太多，但自己还是写了1k行的代码，钻研过程耗费了不少时间。

