# 包烟复习：C

> 学习资料：[菜鸟教程](https://www.runoob.com/cprogramming/c-tutorial.html)

[toc]

## 杂谈

1. **预处理指令**：`#include <stdio.h>` 是预处理器指令，告诉 C 编译器在实际编译之前要包含 `stdio.h` 文件。

2. **sizeof**：表达式 `sizeof(type)` 得到对象或类型的存储字节大小。

3. **未初始化**：带有静态存储持续时间的变量会被隐式初始化为 NULL（所有字节的值都是 0），其他所有变量的初始值是未定义的。

4. **extern**：`extern int i;` 仅声明该变量，而未定义该变量，未为其建立存储空间。

   用于在一个源文件中引用另一个源文件中定义的变量，只需在引用的文件中将变量加上 extern 关键字的声明。

5. **左值和右值**：右值指的是存储在内存中某些地址的数值，不能对其进行赋值。

6. **整数/浮点数常量前后缀**：

   * 前缀：0X表示十六进制，0表示八进制，无前缀十进制
   * 后缀： U 表示无符号整数，L 表示长整数
   * 指数符号：E 

7. **部分字符常量**：终止 `\0`换行 `\n` 回车 `\t`

8. **定义常量**：宏定义 `#define identifier value` 或 前缀声明指定类型  `const type variable = value;`

   * define 定义简单函数：`#define  MAX_2(x, y)  ( x> y ? x : y )`

9. **储存类修饰符**：

   * **auto**：所有局部变量默认的存储类
   * **register**：用于定义存储在寄存器中而不是 RAM 中的局部变量，不能对其取地址
   * **static**：修饰局部变量可以在函数调用之间保持局部变量的值，也是所有全局变量默认的存储类
   * **extern**：提供一个全局变量的引用，全局变量对所有的程序文件都是可见的，可以在其他文件中使用 *extern* 来得到已定义的变量或函数的引用。

10. **运算符**：

    * **自增/自减**：`c = a++` 先赋值后运算，`c = ++a` 先计算后赋值。
    * **位运算符**：诸位执行操作，与 `&` ，或 `|`，异或 `^`，取反 `~`，左移 `<<`，右移 `>>`

    * **取地址**：`&`
    * （由地址）**指向变量**：`*`
    * 优先级：位运算的优先级较低（甚至低于相等/不等）

11. `switch`语句：若等于某一个常量表达式，则从这个表达式后的语句开始执行，并执行后面所有 case 后的语句。

    ```c
    switch(表达式)
    {
        case 常量表达式1: 语句1;
        case 常量表达式2: 语句2;
        ...
        default: 语句N;
    }
    ```

12. **函数传参**：

    * 传值：`void swap(int x, int y);`
    * 传指针：`void swap(int *x, int *y);`
    * 传引用：`void swap(int &x, int &y);`

13. **内部函数 / 外部函数 / 内联函数**：分别使用 `static` 、 `extern` 和 `inline`（加在返回值类型前面）

    * 使用内部函数，可以使函数的作用域只局限于所在文件。即使在不同的文件中有同名的内部函数，也互不干扰。

    * 外部函数，可供其它文件调用，如果在定义函数时省略 extern，则默认为外部函数。

      在需要调用此函数的其他文件中，需要对此函数作声明（不要忘记，即使在本文件中调用一个函数，也要用函数原型来声明）。在对此函数作声明时，要加关键字 extern，表示该函数是在其他文件中定义的外部函数。

    * 内联函数是指用 inline 关键字修饰的函数。内联扩展用来消除函数调用时的时间开销，通常用于频繁执行的函数，对于小内存空间的函数非常受益。

      内联函数从源代码层看，有函数的结构，而在编译后，却不具备函数的性质，故不能定义为内联函数，不适用于复杂函数。

14. **主函数** `int main( int argc, char *argv[] )`：

    * 可执行文件名称和所有参数的个数之和传递给 argc；
    * 可执行文件名称（包括路径名称）作为一个字符串，首地址被赋给 argv[0]，参数1也作为一个字符串，首地址被赋给 argv[1]，... ...依次类推。

15. **占位符**：

    * **%d, %i** 代表整数、**%f** 浮点、**%c** 字符
    *  **%s** 字符串：**遇空格、制表符或换行符结束**
    *  **%p** 指针
    *  **%e** 科学计数
    *  **%i** 读入十进制，八进制，十六进制整数
    *  **%o** 读入八进制整数、**%x,%X** 读入十六进制整数
    * **%u** 读入一个无符号十进制整数。

16. **数组**

    * 初始化赋值：

      ````c
      int a[5] = {1, 2, 3, 4, 5};
      int b[4][2] = {{0,0}, {1,2}, {2,4}, {3,6}};
      ````

    * 数组传参：

      ```c
      void func_1(int *a);
      void func_2(int a[5]);
      void func_3(int a[]);
      void func_4(int b[][2]);
      void func_5(int (*b)[2]);
      void func_6(int *b, int n, int m);
      ```

      ``` c++
      void func_6(int *b, int n, int m){ 
          int i, j; 
          for(i = 0; i < n; i++) { 
              for(j = 0; j < m; j++) 
                  printf("%d ", *(b + i*m + j));
              printf("\n"); 
          } 
      }
      ```

17. **枚举**：

    ```c
    enum DAY
    {
    	MON=1, TUE, WED, THU, FRI, SAT, SUN
    };
    enum DAY day = WED;
    ```

18. **指针**：`int a = 0; int *p = &a;`

    * NULL 指针是一个定义在标准库中的值为零的常量
    * 指针所指向的对象的类型决定递增递减操作的效果
    * 由指针组成的数组：`int * ptr_arr[10];`
    * 指向指针的指针：`int ** pp = &p;`

19. **函数指针**：

    ```c
    #include <stdio.h>
    int max(int x, int y) {
        return x > y ? x : y;
    }
    int main(void) {
        int (* p)(int, int) = & max; // &可以省略
        int a = 1, b = 2;
        d = p(a, b); 
        return 0;
    }
    ```

20. **结构体**：

    ``` c++
    struct NODE
    {
        char string[100];
        struct NODE *next_node;
    };
    ```

    * 成员访问符：`.`
    * 使用 -> 运算符访问指向该结构的指针访问结构的成员

21. **UNION**：一个变量（相同的内存位置）可以存储多个多种类型的数据，可以根据需要在一个共用体内使用任何内置的或者用户自定义的数据类型。

    * 共用体占用的内存应足够存储共用体中最大的成员，还要考虑字节对齐。

    ``` c
    union Data{
        int i;
        float f;
        char str[9]; // 9 个字节
        double d; // 8 个字节
    }data; // 16个字节
    ```

22. **位域**：所谓"位域"是把一个字节中的二进位划分为几个不同的区域，并说明每个区域的位数。每个域有一个域名，允许在程序中按域名进行操作。这样就可以把几个不同的对象用一个字节的二进制位域来表示。

    ```c
    struct bs{
        unsigned a:4;
        unsigned  :4;    /* 空域 */
        unsigned b:4;    /* 从下一单元开始存放 */
        unsigned c:4
    }
    // 在这个两个字节的位域定义中
    // a 占第一字节的 4 位，后 4 位填 0 表示不使用
    // b 从第二字节开始，占用 4 位，c 占用 4 位。
    ```

    * 位域赋值方法与一般结构体相同，赋值时应注意赋值不能超过该位域的允许范围。

23. **typedef**：可以使用它来为类型取一个新的名字

    ```c
    typedef unsigned char BYTE;
    ```


24. **输入输出**：

    * `scanf` 和 `printf`：前者注意加 `scanf("%d", &a);`

      * %d int, %ld long int, %lld long long int
      * %c char, %f float/double, %s char*, %p 指针

    * `getchar` 和 `putchar`：

      * `int getchar(void)` 函数从屏幕读取下一个可用的字符，**并把它返回为一个整数**，这个函数在同一个时间内只会读取一个单一的字符。
      * `int putchar(int c)` 函数把字符输出到屏幕上，并返回相同的字符。

    * `gets` 和 `puts`：（不建议使用）

      * `char *gets(char *s)` 函数从 **stdin** 读取一行到 **s** 所指向的缓冲区，直到一个终止符或 EOF。

        `int puts(const char *s)` 函数把字符串 s 和一个尾随的换行符写入到 **stdout**。

    * `fget` 和 `fputs`：

      ``` c
      char c[100];
      printf("Enter a value:");
      fgets(c, 100, stdin);
      
      printf("\nYou entered:");
      fputs(c, stdout);
      ```

25. **文件读写**：

    * `fopen()`：创建一个新文件或打开一个已有的文件
      * 函数原型：`FILE *fopen( const char * filename, const char * mode );`
      * Mode：
        * **r**：打开一个已有的文本文件，允许读取文件。
        * **w**：打开一个文本文件，允许写入文件。如果文件不存在，则会创建一个新文件。在这里，您的程序会从文件的开头写入内容。如果文件存在，则该会被截断为零长度，重新写入。
        * **a**：打开一个文本文件，以追加模式写入文件。如果文件不存在，则会创建一个新文件。在这里，您的程序会在已有的文件内容中追加内容。
        * **r+**：打开一个文本文件，允许读写文件。
        * **w+**：打开一个文本文件，允许读写文件。如果文件已存在，则文件会被截断为零长度，如果文件不存在，则会创建一个新文件。
        * **a+**：打开一个文本文件，允许读写文件。如果文件不存在，则会创建一个新文件。读取会从文件的开头开始，写入则只能是追加模式。
        * 上述后面补一个 b 表示处理二进制文件
    * `fclose()` 关闭文件
    * `fseek()` 可以移动文件指针到指定位置读,或插入写
      * 函数原型：`int fseek(FILE *stream, long offset, int whence);`
      * `fseek` 设置当前读写点到 offset 处, whence 可以是 `SEEK_SET,SEEK_CUR,SEEK_END` 这些值决定是从文件头、当前点和文件尾计算偏移量 offset。
    * 输入输出
      * `int fputc( int c, FILE *fp );`
      * `int fputs( const char *s, FILE *fp );`
      * `int fgetc( FILE * fp );`
      * `char *fgets( char *buf, int n, FILE *fp );`
    * 二进制输入输出 IO
      * `size_t fread(void *ptr, size_t size_of_elements, size_t number_of_elements, FILE *a_file); `         
      * `size_t fwrite(const void *ptr, size_t size_of_elements, size_t number_of_elements, FILE *a_file);`

26. **预处理命令**：以`#`开头

    * ```c
      #ifndef MESSAGE
         #define MESSAGE "You wish!"
      #endif
      ```

    * `#include`、`#define`

    * 使用预定义宏

      ```c
      #include <stdio.h>
      
      int main()
      {
         printf("File :%s\n", __FILE__ );
         printf("Date :%s\n", __DATE__ );
         printf("Time :%s\n", __TIME__ );
         printf("Line :%d\n", __LINE__ );
         printf("ANSI :%d\n", __STDC__ );
         return 0;
      }
      /* 输出
      File :test.c
      Date :Jun 2 2012
      Time :03:36:24
      Line :8
      ANSI :1
      */
      ```

    * 宏延续运算符`\`：

      ```c
      #define  message_for(a, b)  \
          printf(#a " and " #b ": We love you!\n")
      ```

    * 字符串常量化运算符`#`：

      ```c
      #include <stdio.h>
      
      #define  message_for(a, b)  \
          printf(#a " and " #b ": We love you!\n")
      
      int main(void)
      {
         message_for(Carole, Debra);
         return 0;
      }
      // 输出：Carole and Debra: We love you!
      ```

    * 标记粘贴运算符`##`

      ``` c
      #include <stdio.h>
      
      #define tokenpaster(n) printf ("token" #n " = %d", token##n)
      
      int main(void)
      {
         int token34 = 40;
         tokenpaster(34);
         return 0;
      }
      // 输出：token34 = 40
      ```

27. **头文件**

    * 系统文件：`#include <file>`
    * 用户文件：`#include "file"`

28. **强制类型转换**：如果一个运算符两边的运算数类型不同，先要将其转换为相同的类型，即较低类型转换为较高类型，然后再参加运算

    char, short -> int -> unsigned -> long -> double, float -> double

29. **错误处理**：在发生错误时，大多数的 C 或 UNIX 函数调用返回 1 或 NULL，同时会设置一个错误代码 errno，该错误代码是全局变量，表示在函数调用期间发生了错误。您可以在 errno.h 头文件中找到各种各样的错误代码。

    * C 语言提供了 **perror()** 和 **strerror()** 函数来显示与 **errno** 相关的文本消息。
    * 需要 include `errno.h`

    ``` c
    #include <stdio.h>
    #include <errno.h>
    #include <string.h>
     
    extern int errno ; // notice
     
    int main ()
    {
       FILE * pf;
       int errnum;
       pf = fopen ("unexist.txt", "rb");
       if (pf == NULL)
       {
          errnum = errno;
          fprintf(stderr, "错误号: %d\n", errno);
          perror("通过 perror 输出错误");
          fprintf(stderr, "打开文件错误: %s\n", strerror( errnum ));
       }
       else
       {
          fclose (pf);
       }
       return 0;
    }
    /*
    错误号: 2
    通过 perror 输出错误: No such file or directory
    打开文件错误: No such file or directory
    */
    ```

30. **内存管理**
    * 头文件：`stdlib.h`
    * `calloc`：函数原型`void *calloc(int num, int size);` **在内存中动态地分配 num 个长度为 size 的连续空间**，并将每一个字节都初始化为 0。所以它的结果是分配了 num*size 个字节长度的内存空间，并且每个字节的值都是0。
    * `free`：函数原型`void free(void *address);`该函数释放 address 所指向的内存块，释放的是动态分配的内存空间。
    * `malloc`：函数原型`void *malloc(int num);` 在堆区分配一块指定大小的内存空间，用来存放数据。这块内存空间在函数执行完成后不会被初始化，它们的值是未知的。
    * `realloc`：函数原型`void *realloc(void *address, int newsize);`
      该函数重新分配内存，把内存扩展到 newsize。

## C 标准库

* **<ctype.h>** 提供了一些函数，可用于测试和映射字符，例如`int isdigit(int c)`、`int isalnum(int c)`、`int tolower(int c)`、`int toupper(int c)`

* **<errno.h>** 定义了整数变量 errno，它是通过系统调用设置的，在错误事件中的某些库函数表明了什么发生了错误。

* **<limits.h>** 决定了各种变量类型的各种属性（例如最大值、最小值）。例如常用宏`INT_MIN`、`INT_MAX`、`LONG_MIN`

* **<math.h>** 定义了各种数学函数，参数和返回值类型全是 double

* **<stdarg.h>** 定义了一个变量类型 va_list 和三个宏，这三个宏可用于在参数个数未知（即参数个数可变）时获取函数中的参数。

* **<stddef .h>** 定义了各种变量类型和宏，包括无符号整数类型`size_t`（sizeof 关键字返回的结果），`NULL` 空指针。

* **<stdio .h>** 定义了三个变量类型、一些宏和各种函数来执行输入和输出。包括`size_t`、`FILE`，`NULL`、`stderr`、`stdin`、`stdout`、`fopen`、`scanf`、`printf`等。

* **<stdlib .h>** 定义了各种通用工具函数，包括：`atoi`、`atof`、`malloc`、`free`、`abs`、`rand`等。

* **<string .h>** 

  | 函数 & 描述                                                  |
  | :----------------------------------------------------------- |
  | [void *memchr(const void *str, int c, size_t n)](https://www.runoob.com/cprogramming/c-function-memchr.html) 在参数 *str* 所指向的字符串的前 n 个字节中搜索第一次出现字符 c（一个无符号字符）的位置。 |
  | [int memcmp(const void *str1, const void *str2, size_t n)](https://www.runoob.com/cprogramming/c-function-memcmp.html) 把 *str1* 和 *str2* 的前 n 个字节进行比较。 |
  | [void *memcpy(void *dest, const void *src, size_t n)](https://www.runoob.com/cprogramming/c-function-memcpy.html) 从 src 复制 n 个字符到 *dest*。 |
  | [void *memmove(void *dest, const void *src, size_t n)](https://www.runoob.com/cprogramming/c-function-memmove.html) 另一个用于从 *src* 复制 n 个字符到 *dest* 的函数。 |
  | [void *memset(void *str, int c, size_t n)](https://www.runoob.com/cprogramming/c-function-memset.html) 复制字符 c（一个无符号字符）到参数 *str* 所指向的字符串的前 n 个字符。 |
  | [char *strcat(char *dest, const char *src)](https://www.runoob.com/cprogramming/c-function-strcat.html) 把 *src* 所指向的字符串追加到 *dest* 所指向的字符串的结尾。 |
  | [char *strncat(char *dest, const char *src, size_t n)](https://www.runoob.com/cprogramming/c-function-strncat.html) 把 *src* 所指向的字符串追加到 *dest* 所指向的字符串的结尾，直到 n 字符长度为止。 |
  | [char *strchr(const char *str, int c)](https://www.runoob.com/cprogramming/c-function-strchr.html) 在参数 *str* 所指向的字符串中搜索第一次出现字符 c（一个无符号字符）的位置。 |
  | [int strcmp(const char *str1, const char *str2)](https://www.runoob.com/cprogramming/c-function-strcmp.html) 把 *str1* 所指向的字符串和 *str2* 所指向的字符串进行比较。 |
  | [int strncmp(const char *str1, const char *str2, size_t n)](https://www.runoob.com/cprogramming/c-function-strncmp.html) 把 *str1* 和 *str2* 进行比较，最多比较前 n 个字节。 |
  | [char *strcpy(char *dest, const char *src)](https://www.runoob.com/cprogramming/c-function-strcpy.html) 把 *src* 所指向的字符串复制到 *dest*。 |
  | [char *strncpy(char *dest, const char *src, size_t n)](https://www.runoob.com/cprogramming/c-function-strncpy.html) 把 *src* 所指向的字符串复制到 *dest*，最多复制 n 个字符。 |
  | [size_t strlen(const char *str)](https://www.runoob.com/cprogramming/c-function-strlen.html) 计算字符串 str 的长度，直到空结束字符，但不包括空结束字符。 |
  | [char *strrchr(const char *str, int c)](https://www.runoob.com/cprogramming/c-function-strrchr.html) 在参数 *str* 所指向的字符串中搜索最后一次出现字符 c（一个无符号字符）的位置。 |
  | [char *strstr(const char *haystack, const char *needle)](https://www.runoob.com/cprogramming/c-function-strstr.html) 在字符串 *haystack* 中查找第一次出现字符串 *needle*（不包含空结束字符）的位置。 |
  | [char *strtok(char *str, const char *delim)](https://www.runoob.com/cprogramming/c-function-strtok.html) 分解字符串 *str* 为一组字符串，*delim* 为分隔符。 |

* **<time.h>** 定义了操作日期和时间的结构和函数。

  * **clock_t** 适合存储处理器时间的类型。

  * **time_t is** 适合存储日历时间类型。

  * **struct tm** 用来保存时间和日期的结构。

    ``` c
    struct tm {
       int tm_sec;         /* 秒，范围从 0 到 59        */
       int tm_min;         /* 分，范围从 0 到 59        */
       int tm_hour;        /* 小时，范围从 0 到 23        */
       int tm_mday;        /* 一月中的第几天，范围从 1 到 31    */
       int tm_mon;         /* 月，范围从 0 到 11        */
       int tm_year;        /* 自 1900 年起的年数        */
       int tm_wday;        /* 一周中的第几天，范围从 0 到 6    */
       int tm_yday;        /* 一年中的第几天，范围从 0 到 365    */
       int tm_isdst;       /* 夏令时                */
    };
    ```

  * **CLOCKS_PER_SEC** 宏表示每秒的处理器时钟个数。

  | 函数 & 描述                                                  |
  | :----------------------------------------------------------- |
  | [char *ctime(const time_t *timer)](https://www.runoob.com/cprogramming/c-function-ctime.html) 返回一个表示当地时间的字符串，当地时间是基于参数 timer。 |
  | [double difftime(time_t time1, time_t time2)](https://www.runoob.com/cprogramming/c-function-difftime.html) 返回 time1 和 time2 之间相差的秒数 (time1-time2)。 |
  | [time_t time(time_t *timer)](https://www.runoob.com/cprogramming/c-function-time.html) 计算当前日历时间，并把它编码成 time_t 格式。 |
