# 词法分析实验（重做）

**19335286 郑有为**

> 说明：**之前是用 C语言 自己写的，可能还有不少潜在的 BUG，感觉不可靠，故使用 Lex 来重写词法分析程序，因为是 Lex 生成的代码，简单可靠，同时可以配合 Yacc 完成语法分析实验与语义分析和中间代码生成实验。**

[toc]

## Ⅰ. 词法定义

参考C语言、老师的资料和华南理工的TINY+实验，以下给出TINY+的词法定义：

**关键字定义**如下，区分大小写，共 19 个。

| KEY    | KEY   | KEY  | KEY   | KEY  | KEY   |
| ------ | ----- | ---- | ----- | ---- | ----- |
| or     | and   | int  | float | bool | char  |
| while  | do    | if   | then  | else | end   |
| repeat | until | read | write | true | false |
| string | not    |      |       |      |       |

**操作符定义**如下，也称为特殊符号，共 17 个。

| SYM  | SYM  | SYM  | SYM  | SYM  | SYM  | SYM  | SYM  |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| >    | <=   | >=   | ,    | {    | }    | ;    | :=   |
| +    | -    | *    | /    | (    | )    | <    | =    |

**其他词法**

| 标识       | 正则表达式（Lex语法）                           | 注释                                                     |
| ---------- | ----------------------------------------------- | -------------------------------------------------------- |
| DIGIT      | `[0-9]`                                         |                                                          |
| LETTER     | `[A-Za-z]`                                      |                                                          |
| DIGITS     | `[0-9][0-9]*`                                   |                                                          |
| ASCII      | `[\x00-\x7f]`                                   |                                                          |
| **ID**     | `{LETTER}({LETTER}|{DIGIT})*`                   | 标识符，以字母开头，可包含数字                           |
| **INT**    | `[+-]?({DIGIT})+`                               | 整数，如+0，-5，100                                      |
| **FLOAT**  | `[+-]?{DIGITS}"."{DIGITS}`                      | 浮点数，如-0.14                                          |
| **CHAR**   | `'[^']'`                                        | 字符，如`'a'`                                            |
| **STRING** | `\"[^\n\"]*\"`                                  | 如`"Hi"`，不可跨行，不可嵌套                             |
| **注释**   | `"/*".*"*/"`或`"/*"([^\n"*/"]*\n)*"*/"		` | 如 `/*Hi*/` ，可跨行，不可嵌套，其内容会被词法分析器忽略 |

## Ⅱ. 错误检测

1. **非法字符检错**：碰到非法字符（**我们视语法中不出现的字符，包括非ASCII符号为非法字符**）回在终端输出保存信息和错误所在行数，词法分析会继续进行

   ```
   [^0-9a-zA-Z\n \t">""<""="",""'""{""}""/"";"":""+""-""*""("")"] { printf("Error at Line %d: 非法符号 %s\n", Line,  yytext); }
   ```

2. **注释和字符串的边界符号匹配**：如果检测到缺少`"`或`/*`或`*/`，回报错，返回错误所在行数。

   ```
   '			{ printf("Error at Line %d: 字符缺少 %s\n", Line, yytext); }
   \"			{ printf("Error at Line %d: 字符串缺少 %s\n", Line, yytext); }
   "/*"		{ printf("Error at Line %d: 注释缺少 */\n", Line); }
   "*/"		{ printf("Error at Line %d: 注释缺少 /*\n", Line); }
   ```

### 运行说明

编译和运行：Linux 环境，首先使用 apt-get 安装 flex，安装完后执行以下代码即可

``` sh
flex la.l
gcc -o la.exe lex.yy.c -lfl
./la.exe
```

需要按照提示输入词法文件地址。

## Ⅲ. 测试部分

测试输入文件位于 ***in/***，输出文件位于 ***out***/ 中，以下是三个测试的命令行输出结果，其中测试 - 3 是展示了词法分析过程的错误检测部分。

### 测试 - 1

```
/* -- test1 -- */

or and int bool char
while do if then else not
end repeat until read write
, ; := + -
* / ( ) <
= > >= <= a2c 123 'E' "ABC"
/*
hey
*/
```

```
Input File: 
in/t1.txt
Output File: 
out/t1.txt
Find 注释 at Line 1


Find (KEY, or)
Find (KEY, and)
Find (KEY, int)
Find (KEY, bool)
Find (KEY, char)

Find (KEY, while)
Find (KEY, do)
Find (KEY, if)
Find (KEY, then)
Find (KEY, else)
Find (KEY, not)

Find (KEY, end)
Find (KEY, repeat)
Find (KEY, until)
Find (ID, read)
Find (ID, write)

Find (SYM, ,)
Find (SYM, ;)
Find (SYM, :=)
Find (SYM, +)
Find (SYM, -)

Find (SYM, *)
Find (SYM, /)
Find (SYM, ()
Find (SYM, ))
Find (SYM, <)

Find (SYM, =)
Find (SYM, >)
Find (SYM, >=)
Find (SYM, <=)
Find (ID, a2c)
Find (INT, 123)
Find (CHAR, 'E')
Find (STRING, "ABC")

Find 跨行注释 from Line 9 to 11

La finsih
```

### 测试 - 2


```
/* -- test2 -- */
int A = 1, B;
bool C1 = true, C2 = false, C3 == true;
string D;
float E = -1.6;
char F = 'k';
D := "scanner";
while A <= B and C1 and C2 or C3 do
	A := A * 2;
	E := -1 * E;
end
```

```
Input File: 
Input File: 
in/t2.txt
Output File: 
out/t2.txt
Find 注释 at Line 1

Find (KEY, int)
Find (ID, A)
Find (SYM, =)
Find (INT, 1)
Find (SYM, ,)
Find (ID, B)
Find (SYM, ;)

Find (KEY, bool)
Find (ID, C1)
Find (SYM, =)
Find (KEY, true)
Find (SYM, ,)
Find (ID, C2)
Find (SYM, =)
Find (ID, false)
Find (SYM, ,)
Find (ID, C3)
Find (SYM, =)
Find (SYM, =)
Find (KEY, true)
Find (SYM, ;)

Find (KEY, string)
Find (ID, D)
Find (SYM, ;)

Find (KEY, float)
Find (ID, E)
Find (SYM, =)
Find (FLOAT, -1.6)
Find (SYM, ;)

Find (KEY, char)
Find (ID, F)
Find (SYM, =)
Find (CHAR, 'k')
Find (SYM, ;)

Find (ID, D)
Find (SYM, :=)
Find (STRING, "scanner")
Find (SYM, ;)

Find (KEY, while)
Find (ID, A)
Find (SYM, <=)
Find (ID, B)
Find (KEY, and)
Find (ID, C1)
Find (KEY, and)
Find (ID, C2)
Find (KEY, or)
Find (ID, C3)
Find (KEY, do)

Find (ID, A)
Find (SYM, :=)
Find (ID, A)
Find (SYM, *)
Find (INT, 2)
Find (SYM, ;)

Find (ID, E)
Find (SYM, :=)
Find (INT, -1)
Find (SYM, *)
Find (ID, E)
Find (SYM, ;)

Find (KEY, end)

La finsih
```

### 测试 - 3

```
/* -- test3 -- */

& $ . ~
hihi "
hihi */
" hihi
/* hihi
'a
a'
```


```
Input File: 
in/t3.txt
Output File: 
out/t3.txt
Find 注释 at Line 1


Error at Line 3: 非法符号 &
Error at Line 3: 非法符号 $
Error at Line 3: 非法符号 .
Error at Line 3: 非法符号 ~

Find (ID, hihi)
Error at Line 4: 字符串缺少 "

Find (ID, hihi)
Error at Line 5: 注释缺少 /*

Error at Line 6: 字符串缺少 "
Find (ID, hihi)

Error at Line 7: 注释缺少 */
Find (ID, hihi)

Error at Line 8: 字符缺少 '
Find (ID, a)

Find (ID, a)
Error at Line 9: 字符缺少 '

La finsih
```

## Ⅳ. 参考资料

1.  **Lex − A Lexical Analyzer Generator** M. E. Lesk a and E. Schmidt
2. **《编译原理教学-华南理工》实验指导书-编译原理**
