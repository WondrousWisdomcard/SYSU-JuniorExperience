%{
/*
 * 词法分析实验 
 * 19335286 郑有为
 */
 
int Line = 1; 
 
%}

DIGIT [0-9]
LETTER [A-Za-z]
DIGITS [0-9][0-9]*
ASCII [\x00-\x7f]

%%

\n		{ 
			Line += 1; 
			printf("\n"); 
			fprintf(yyout, "\n"); 
		}

[\t ]+		; /* 忽略所有空格和Tab */

or		|
and 	|
int		|
float	|
not		|
bool	|
char	|
string	|
while	|
do		|
if		|
then	|
else	|
end		|
repeat	|
until	|
read	|
write	|
true	|
flase	{ 
			printf("Find (KEY, %s)\n", yytext);
			fprintf(yyout, "Find (KEY, %s)\n", yytext);
		}

">"		|
"<="	|
">="	|
","		|
"{"		|
"}"		|
";"		|
":="	|
"+"		|
"-"		|
"*"		|
"/"		|
"("		|
")"		|
"<"		|
"="		{ 	
			printf("Find (SYM, %s)\n", yytext); 
			fprintf(yyout, "Find (SYM, %s)\n", yytext);
		}

{LETTER}({LETTER}|{DIGIT})*	{ 	
								printf("Find (ID, %s)\n", yytext);
								fprintf(yyout, "Find (ID, %s)\n", yytext);
							}
	
[+-]?({DIGIT})+				{ 
								printf("Find (INT, %s)\n", yytext); 
								fprintf(yyout, "Find (INT, %s)\n", yytext); 
							}

[+-]?{DIGITS}"."{DIGITS}	{ 
								printf("Find (FLOAT, %s)\n", yytext);
								fprintf(yyout, "Find (FLOAT, %s)\n", yytext);
							}


'[^']'						{ 
								printf("Find (CHAR, %s)\n", yytext);
								fprintf(yyout, "Find (CHAR, %s)\n", yytext);
							}
							
\"[^\n\"]*\"				{ 
								printf("Find (STRING, %s)\n", yytext);
								fprintf(yyout, "Find (STRING, %s)\n", yytext);
							}

"/*".*"*/"					{ printf("Find 注释 at Line %d\n", Line); } 

"/*"([^\n"*/"]*\n)*"*/"		{ 
								printf("Find 跨行注释 from Line %d to ", Line);
								for(int i = 0; i < yyleng; i++){
									if(yytext[i] == '\n'){
										Line += 1;
									}
								}
								printf("%d\n", Line);
							} 


[^0-9a-zA-Z\n \t">""<""="",""'""{""}""/"";"":""+""-""*""("")"] { printf("Error at Line %d: 非法符号 %s\n", Line,  yytext); }

'			{ printf("Error at Line %d: 字符缺少 %s\n", Line, yytext); }
\"			{ printf("Error at Line %d: 字符串缺少 %s\n", Line, yytext); }
"/*"		{ printf("Error at Line %d: 注释缺少 */\n", Line); }
"*/"		{ printf("Error at Line %d: 注释缺少 /*\n", Line); }

%%

int main()
{
	char infile[100];
	char outfile[100];
	printf("Input File: \n");
	scanf("%s", infile);
	printf("Output File: \n");
	scanf("%s", outfile);
	
	yyin = fopen(infile, "r");
	yyout = fopen(outfile, "w");
	yylex();
	
	printf("La finsih\n");
	return 0;
}


