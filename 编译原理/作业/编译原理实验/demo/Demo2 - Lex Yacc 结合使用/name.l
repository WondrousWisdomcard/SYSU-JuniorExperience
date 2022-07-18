%{

/* 
A demo from: http://www.ibm.com/developerworks/cn/Linux/sdk/lex/
YYSTYPE 使不被覆盖的方法 http://newbt.net/ms/vdisk/show_bbs.php?id=vdisk_mysql_4438&pid=9
编译运行：其中 yacc -d 中的 -d 用于生成 .h 文件

lex.name.y
yacc -d name.y 
gcc lex.yy.c y.tab.c
*/
 
#define YYSTYPE char*
#include "y.tab.h"
#include <stdio.h>
#include <string.h>

%}

char [A-Za-z]
num [0-9]
eq [=]
name {char}+
age {num}+

%%

{name} { yylval = strdup(yytext); return NAME; }
{eq} { return EQ; }
{age} { yylval = strdup(yytext); return AGE; }

%%
int yywrap()
{
	return 1;
}
