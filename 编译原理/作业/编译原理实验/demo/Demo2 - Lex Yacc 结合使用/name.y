%{

/* 
A demo from: http://www.ibm.com/developerworks/cn/Linux/sdk/lex/
YYSTYPE 使不被覆盖的方法 http://newbt.net/ms/vdisk/show_bbs.php?id=vdisk_mysql_4438&pid=9
编译运行：其中 yacc -d 中的 -d 用于生成 .h 文件

lex name.l
yacc -d name.y 
gcc lex.yy.c y.tab.c
*/

#include <stdio.h>
#include <string.h>
#define YYSTYPE char*
%}

%token NAME EQ AGE

%%
file : record file | record		;
record : NAME EQ AGE { printf("%s is %s years old!!!\n", (char*)$1, (char*)$3); }

%%
int main(){
	yyparse();
	return 0;
}

int yyerror(char *msg){
	printf("Error encountered: %s \n", msg);
}
