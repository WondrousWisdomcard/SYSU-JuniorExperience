%{
#include "df.h"

/* 定义 YYSTYPE 为 语法树结构体
lex la.l
yacc -d ga.y 
gcc lex.yy.c y.tab.c df.h
 */
#define YYSTYPE Node*

#include "y.tab.h"
#include <stdio.h>
#include <string.h>

void yyerror(char *);

/* 代码行数标记 */
int Line = 1;

%}

DIGIT [0-9]
LETTER [A-Za-z]
DIGITS [0-9][0-9]*

%%

\n		{ /* 更新行数，用于报错 */
			Line += 1; 
			// printf("\nLine %02d: ", Line);
		}
[\t ]+		; /* 忽略所有空格和Tab */

or		{ yylval = genNode(yytext, Line);   return OR; }
and 	{ yylval = genNode(yytext, Line);   return AND; }
not		{ yylval = genNode(yytext, Line);   return NOT; }

while	{ yylval = genNode(yytext, Line);   return WHILE; }
do		{ yylval = genNode(yytext, Line);   return DO; }
if		{ yylval = genNode(yytext, Line);   return IF; }
then	{ yylval = genNode(yytext, Line);   return THEN; }
else	{ yylval = genNode(yytext, Line);   return ELSE; }
end		{ yylval = genNode(yytext, Line);   return END; }
repeat	{ yylval = genNode(yytext, Line);   return REPEAT; }
until	{ yylval = genNode(yytext, Line);   return UNTIL; }

read	{ yylval = genNode(yytext, Line);   return READ; }
write	{ yylval = genNode(yytext, Line);   return WRITE; }

true	|
false	{ yylval = genNode(yytext, Line); setNodeType(yylval, st_bool); return BOOL; }

int		|
float	|
bool	|
char	|
string	{ yylval = genNode(yytext, Line);   return TYPE; }

"<="	{ yylval = genNode(yytext, Line);   return LE; }
">="	{ yylval = genNode(yytext, Line);   return GE; }
":="	{ yylval = genNode(yytext, Line);   return ASSIGN; }

[-()<>=+*/;{},] { yylval = genNode(yytext, Line);   return *yytext; }


{LETTER}({LETTER}|{DIGIT})*	{ yylval = genNode(yytext, Line); return ID; }
	
[+-]?({DIGIT})+				{ yylval = genNode(yytext, Line); setNodeType(yylval, st_int);  return INT; }

[+-]?{DIGITS}"."{DIGITS}	{ yylval = genNode(yytext, Line); setNodeType(yylval, st_float);  return FLOAT; }


'[^']'						{ yylval = genNode(yytext, Line); setNodeType(yylval, st_char);  return CHAR; }
							
\"[^\n\"]*\"				{ 
	yytext[0] = '\'';
	yytext[yyleng-1] = '\'';
	yylval = genNode(yytext, Line); 
	setNodeType(yylval, st_string);  return STRING; } /*常量*/


"/*".*"*/"	                |
"/*"([^\n"*/"]*\n)*"*/"		{ 
								for(int i = 0; i < yyleng; i++){
									if(yytext[i] == '\n'){
										Line += 1;
									}
								}
							} /* 注释*/


[^0-9a-zA-Z\n \t">""<""="",""'""{""}""/"";"":""+""-""*""("")"] { yyerror("出现非法符号"); }
'			{ yyerror("单引号未配对"); }
\"			{ yyerror("双引号未配对"); }
"/*"		{ yyerror("注释缺少 */"); }
"*/"		{ yyerror("注释缺少 /*"); } /* 错误检测 */

%%

void yyerror(char *s) {
	fprintf(stderr, "Error at Line %02d: %s\n", Line, s);
	exit(1);
}

int yywrap(void) { 
    return 1;
}


