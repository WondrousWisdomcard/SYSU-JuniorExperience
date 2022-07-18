%{
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include "df.h"

#define YYSTYPE Node*

FILE* yyin;
int yylex(void);
void yyerror(char *s);

%}

%error-verbose

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

%% 

program: declarations stmt	
	{ 
		$$ = genNode("program"); 
		addChild($$, $1);
		addChild($$, $2);
		
		printf("\nSyntax Tree:\n");
		showNode($$, 0, 1); 
		freeNode($$);  
		exit(0); 
	}
	| stmt	
	{ 
		$$ = genNode("program"); 
		addChild($$, $1);
		
		printf("\n语法树的前序遍历:\n0: ");
		showNode($$, 0, 1); 
		freeNode($$);  
		exit(0); 
	}

declarations: declaration ';' {
		$$ = genNode("declarations"); 
		addChild($$, $1);
		addChild($$, $2);
	}
	| declaration ';' declarations 
	{ 
		$$ = genNode("declarations"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
	
declaration: TYPE varlist
    { 
		$$ = genNode("declaration"); 
		addChild($$, $1);
		addChild($$, $2);
	}

varlist: ID { 
		$$ = genNode("varlist");  
		addChild($$, $1);
	}
    | ID ',' varlist {
		$$ = genNode("varlist"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}

stmt: xstmt ';' {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
	}
    | xstmt ';' stmt {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    

xstmt: IF boolexp THEN stmt ELSE stmt END {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		addChild($$, $4);
		addChild($$, $5);
		addChild($$, $6);
		addChild($$, $7);
	}
    | IF boolexp THEN stmt END {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		addChild($$, $4);
		addChild($$, $5);
	}
    | WHILE boolexp DO stmt END {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		addChild($$, $4);
		addChild($$, $5);
	}
    | REPEAT stmt UNTIL boolexp {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		addChild($$, $4);
	}
    | ID ASSIGN exp {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | READ ID {
		$$ = genNode("xstmt"); 
		addChild($$, $1);
		addChild($$, $2);
	}
    | WRITE exp {
		$$ = genNode("writexstmt"); 
		addChild($$, $1);
		addChild($$, $2);
	}

exp: arithmeticexp 
    | boolexp
    | strexp {
		$$ = $1;
	}

arithmeticexp: INT {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
	}
    | FLOAT {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
	}
	| ID {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
	}
    | '(' arithmeticexp ')' {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp '+' arithmeticexp {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp '-' arithmeticexp {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp '*' arithmeticexp {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp '/' arithmeticexp {
		$$ = genNode("arithexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}

boolexp: BOOL {
		$$ = genNode("boolexp"); 
		addChild($$, $1);
	}
    | comparison {
		$$ = genNode("boolexp"); 
		addChild($$, $1);
	}
    | '(' boolexp ')' {
		$$ = genNode("boolexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | NOT boolexp {
		$$ = genNode("boolexp"); 
		addChild($$, $1);
		addChild($$, $2);
	}
    | boolexp AND boolexp {
		$$ = genNode("boolexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | boolexp OR boolexp {
		$$ = genNode("boolexp"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}

strexp: CHAR {
		$$ = genNode("strexp"); 
		addChild($$, $1);
	} 
    | STRING {
		$$ = genNode("strexp"); 
		addChild($$, $1);
	}
    
comparison:
      arithmeticexp '>' arithmeticexp {
		$$ = genNode("comparison"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp '<' arithmeticexp {
		$$ = genNode("comparison"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp '=' arithmeticexp {
		$$ = genNode("comparison"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp GE arithmeticexp {
		$$ = genNode("comparison"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}
    | arithmeticexp LE arithmeticexp {
		$$ = genNode("comparison"); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
	}

%%

Node* genNode(char* content){

	printf("[%s] ", content);
	
	Node* p = NULL;
	if ((p = malloc(sizeof(Node))) == NULL){
		yyerror("out of memory");
	}
	p->content = strdup(content);
	p->cnum = 0;
	for(int i = 0; i < 10; i++){
		p->children[i] = NULL;
	}
	return p;
}

void addChild(Node* p, Node* child){
	p->children[p->cnum] = child;
	p->cnum++;
}

void freeNode(Node* p){
	if(p == NULL){
		return;
	}
	for(int i = 0; i < p->cnum; i++){
		freeNode(p->children[i]);
	}
	free(p->content);
	free(p);
}

void showNode(Node* p, int d, int i){
	if(p == NULL){
		return;
	}
	for(int i = 0; i < d; i++){
		printf("   ");
	}
	
	printf("(%d,%d) %s \n", d, i, p->content);
	for(int i = 0; i < p->cnum; i++){
		showNode(p->children[i], d+1, i+1);	
	}
}


int main(void) {
	char infile[100];
	printf("Input File: \n");
	scanf("%s", infile);
	yyin = fopen(infile, "r");
	
	printf("Line 01: ");
	yyparse();
	return 0;
}
