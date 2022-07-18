%{
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include "df.h"

#define YYSTYPE Node*

FILE* yyin;
int yylex(void);
void yyerror(const char *s);

// 根节点
Node* root = NULL;

// 符号表
Symbol symbolTable[TABLE_SIZE];
int symbolNum = 0;

char* type_string[6] = {"null", "int", "float", "char", "string", "bool"};

// 可视化语法树的代码串
char map[100000] = "digraph demo{\nnode [shape=box, style=\"rounded\", color=\"black\", fontname=\"Microsoft YaHei\"];\nedge [fontname=\"Microsoft YaHei\"];\n";
int id = 0;


// 中间代码生成：临时标号申请
int label_id = 0;
int newLabel();
// 中间代码生成：临时变量申请
int temp_id = 0;
int newTempID();
// 因为我们有节点的全局ID 中间代码中每一个为定义next标号可以先用全局ID给他标记下来
// 这样对于一个中间代码文本中，我们可以找到他，并识别他的原本在语法树中的节点。
// 我们遍历一遍树，将必要的next = $$->next自顶向下更新，同时我们每更新一个节点，就去中间代码串中寻找他的位置，并修改成我们新赋值的next值。
void UpdateNext(Node* root, char code[]);

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
		$$ = genNode("program", 0); 
		addChild($$, $1);
		addChild($$, $2);
		root = $$;

		// 中间代码生成
		strcpy($$->code, $2->code);
		UpdateNext(root, root->code);
	}
	| stmt	
	{ 
		$$ = genNode("program", 0); 
		addChild($$, $1);
		root = $$; 

		// 中间代码生成
		strcpy($$->code, $1->code);
		UpdateNext(root, root->code);
	}

declarations: declaration ';' {
		$$ = genNode("declarations", 0); 
		addChild($$, $1);
	}
	| declaration ';' declarations 
	{ 
		$$ = genNode("declarations", 0); 
		addChild($$, $1);
		addChild($$, $3);
	}
	
declaration: TYPE varlist
    { 
		$$ = genNode("declaration", 0); 
		addChild($$, $1);
		addChild($$, $2);
		
		// 生成符号表
		updateSymbolTable($$); 
	}

varlist: ID { 
		$$ = genNode("varlist", 0);  
		addChild($$, $1);
	}
    | ID ',' varlist {
		$$ = genNode("varlist", 0); 
		addChild($$, $1);
		addChild($$, $3);
	}

stmt: xstmt ';' {
		$$ = genNode("xstmt", 0); 
		addChild($$, $1);

		// 中间代码生成
		$1->next = $$->next;
		strcpy($$->code, $1->code);
	}
    | xstmt ';' stmt {
		$$ = genNode("xstmt", 0); 
		addChild($$, $1);
		addChild($$, $3);

		// 中间代码生成
		$1->next = newLabel(); // L 属性赋初始值的地方

		// $$->code = $1->code || Label $1->next || $3->code
		strcpy($$->code, $1->code);
		char labelcode[25];
		sprintf(labelcode, "Label %03d:\n", $1->next);
		strcat($$->code, labelcode);
		strcat($$->code, $3->code);
	}
    

xstmt: IF boolexp THEN stmt ELSE stmt END {
		$$ = genNode("xstmt", 0); 
		addChild($$, $1);  addChild($$, $2); addChild($$, $3);  addChild($$, $4);
		addChild($$, $5);  addChild($$, $6); addChild($$, $7);

		// 中间代码生成
		int fabegin = newLabel();
		// $$->code = $2->code || "If-not _t($2->t_id) Goto Label fabegin" || $4->code 
		// 			  || Goto $$->next || Label fabegin || $6->code

		strcpy($$->code, $2->code);
		char ifnotcode[100];

		if($$->next != -1){
			sprintf(ifnotcode, "If-not _t%d Goto Label %03d\n", $2->t_id, $$->next);
		}
		else{
			sprintf(ifnotcode, "If-not _t%d Goto __Label %03d__\n", $2->t_id, $$->children[0]->id);
		}
		
		strcat($$->code, ifnotcode);
		strcat($$->code, $4->code);
		char labelcode[25];
		if($$->next != -1){
			sprintf(labelcode, "Goto Label %03d\n", $$->next);
		}
		else{
			sprintf(labelcode, "Goto __Label %03d__\n", $$->children[0]->id);
		}

		strcat($$->code, labelcode);
		sprintf(labelcode, "Label %03d:\n", fabegin);
		strcat($$->code, $6->code);
	}
    | IF boolexp THEN stmt END {
		$$ = genNode("xstmt", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		addChild($$, $4); addChild($$, $5);

		// 中间代码生成
		// $$->code = $2->code || "If-not _t($2->t_id) Goto Label $$->next" || $4->code
		strcpy($$->code, $2->code);
		char ifnotcode[100];
		
		if($$->next != -1){
			sprintf(ifnotcode, "If-not _t%d Goto Label %03d\n", $2->t_id, $$->next);
		}
		else{
			sprintf(ifnotcode, "If-not _t%d Goto __Label %03d__\n", $2->t_id, $$->children[0]->id);
		}
		
		strcat($$->code, ifnotcode);
		strcat($$->code, $4->code);
	}
    | WHILE boolexp DO stmt END {
		$$ = genNode("xstmt", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		addChild($$, $4); addChild($$, $5);

		// 中间代码生成
		int begin = newLabel();
		// $$->code = Label begin || $2->code || "If-not _t($2->t_id) Goto Label $$->next"
		//            || $4->code || Goto begin
		char labelcode[25];
		sprintf(labelcode, "Label %03d:\n", begin);
		strcpy($$->code, labelcode);
		strcat($$->code, $2->code);

		char ifnotcode[100];

		if($$->next != -1){
			sprintf(ifnotcode, "If-not _t%d Goto Label %03d\n", $2->t_id, $$->next);
		}
		else{
			sprintf(ifnotcode, "If-not _t%d Goto __Label %03d__\n", $2->t_id, $$->children[0]->id);
		}

		strcat($$->code, ifnotcode);

		strcat($$->code, $4->code);
		sprintf(labelcode, "Goto Label %03d\n", begin);
		strcat($$->code, labelcode);
		
	}
    | REPEAT stmt UNTIL boolexp {
		$$ = genNode("xstmt", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		addChild($$, $4);

		// 中间代码生成
		int begin = newLabel();
		// $$->code = Label begin || $2->code || $4->code || "If-not _t($4->t_id) Goto $$->next || Goto Label begin"
		char labelcode[25];
		sprintf(labelcode, "Label %03d:\n", begin);
		strcpy($$->code, labelcode);

		strcat($$->code, $2->code);
		strcat($$->code, $4->code);

		char ifcode[100];
		if($$->next != -1){
			sprintf(ifcode, "If _t%d Goto Label %03d\n", $4->t_id, $$->next);
		}
		else{
			sprintf(ifcode, "If _t%d Goto __Label %03d__\n", $4->t_id, $$->children[0]->id);
		}

		strcat($$->code, ifcode);

		sprintf(labelcode, "Goto Label %03d\n", begin);
		strcat($$->code, labelcode);

	}
    | ID ASSIGN exp {
		checkID($1); // 检查 ID 是否在符号表中
		checkType($1, $3, 2); // 检查类型是否匹配
		$$ = genNode("xstmt", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);

		// 中间代码生成
		// $$->code = $3->code || "$1->name = $3->name"
		strcpy($$->code, $3->code);
		char newcode[25];
		if($3->t_id == -1){ // 若 exp 为 ID
			sprintf(newcode, "%s = %s\n", $1->content, $3->content);
		} else{
			sprintf(newcode, "%s = _t%d\n", $1->content, $3->t_id);
		}
		strcat($$->code, newcode);
		
	}
    | READ ID {
		checkID($2); // 检查 ID 是否在符号表中
		$$ = genNode("xstmt", 0); 
		addChild($$, $1); addChild($$, $2);

		// 中间代码生成
		// $$->code = "Read $2->name"
		sprintf($$->code, "Read %s\n", $2->content);
	}
    | WRITE exp {
		$$ = genNode("writexstmt", 0); 
		addChild($$, $1); addChild($$, $2);

		// 中间代码生成
		// $$->code = $2->code || "Write $2->name"
		strcat($$->code, $2->code);
		char newcode[25];
		if($2->t_id == -1){ // 若 exp 为 ID
			sprintf(newcode, "Write %s\n", $2->content);
		} else{
			sprintf(newcode, "Write _t%d\n", $2->t_id);
		}
		strcat($$->code, newcode);
	}

exp: arithmeticexp {
		$$ = $1;
	}
    | boolexp {
		$$ = $1;
	}
    | strexp {
		$$ = $1;
	}

arithmeticexp: INT {
		$$ = genNode($1->content, 0); 
		addChild($$, $1);
		setNodeType($$, st_int);

		// 中间代码生成
		// $$->code = "t1 = 123"
		$$->t_id = newTempID();
		sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
	}
    | FLOAT {
		$$ = genNode($1->content, 0); 
		addChild($$, $1);
		setNodeType($$, st_float);

		// 中间代码生成
		// $$->code = "t1 = 1.23"
		$$->t_id = newTempID();
		sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
	}
	| ID {
		checkID($1); // 检查 ID 是否在符号表中
		$$ = genNode($1->content, 0); 
		addChild($$, $1);
		setNodeType($$, $1->type);

		// 中间代码生成
		// Do nothing
		
	}
    | '(' arithmeticexp ')' {
		$$ = genNode("arithexp", 0); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		setNodeType($$, $2->type);

		// 中间代码生成
		// $$->code = $2->code || "$$->name = $2->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $2->code);
		char newcode[25];
		if($2->t_id == -1){ // 若 $2 为 ID
			sprintf(newcode, "_t%d = %s\n", $$->t_id , $2->content);
		} else{
			sprintf(newcode, "_t%d = _t%d\n", $$->t_id , $2->t_id);
		}
		strcat($$->code, newcode);
	}
    | arithmeticexp '+' arithmeticexp {
		checkType($1, $3, 1); // 检查类型是否匹配
		$$ = genNode("arithexp", 0); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		setNodeType($$, $1->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name + $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $3->code);
		strcat($$->code, $1->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " + ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");

		strcat($$->code, newcode);
	}
    | arithmeticexp '-' arithmeticexp {
		checkType($1, $3, 1); // 检查类型是否匹配
		$$ = genNode("arithexp", 0); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		setNodeType($$, $1->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name - $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $3->code);
		strcat($$->code, $1->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " - ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
	}
    | arithmeticexp '*' arithmeticexp {
		checkType($1, $3, 1); // 检查类型是否匹配
		$$ = genNode("arithexp", 0); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		setNodeType($$, $1->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name * $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $3->code);
		strcat($$->code, $1->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " * ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
	}
    | arithmeticexp '/' arithmeticexp {
		checkType($1, $3, 1); // 检查类型是否匹配
		$$ = genNode("arithexp", 0); 
		addChild($$, $1);
		addChild($$, $2);
		addChild($$, $3);
		setNodeType($$, $1->type);

		// 中间代码生成
		// $$->code = $3->code || $1->code || "$1->name / $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $3->code);
		strcat($$->code, $1->code);

		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " / ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
	}

boolexp: BOOL {
		$$ = genNode($1->content, 0); 
		addChild($$, $1);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = "t1 = 1.23"
		$$->t_id = newTempID();
		sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
	}
    | comparison {
		$$ = genNode("boolexp", 0); 
		addChild($$, $1);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || "$$->name = $1->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d\n", $$->t_id , $1->t_id);
		strcat($$->code, newcode);
	}
    | '(' boolexp ')' {
		$$ = genNode("boolexp", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $2->code || "$$->name = $2->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $2->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d\n", $$->t_id , $2->t_id);
		strcat($$->code, newcode);
	}
    | NOT boolexp {
		$$ = genNode("boolexp", 0); 
		addChild($$, $1); addChild($$, $2);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $2->code || "$$->name = not $2->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $2->code);
		char newcode[25];
		sprintf(newcode, "_t%d = not _t%d\n", $$->t_id , $2->t_id);
		strcat($$->code, newcode);

	}
    | boolexp AND boolexp {
		$$ = genNode("boolexp", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name AND $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		strcat($$->code, $3->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d AND _t%d", $$->t_id, $1->t_id, $3->t_id);
		strcat($$->code, newcode);
	}
    | boolexp OR boolexp {
		$$ = genNode("boolexp", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name OR $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		strcat($$->code, $3->code);
		char newcode[25];
		sprintf(newcode, "_t%d = _t%d OR _t%d", $$->t_id, $1->t_id, $3->t_id);
		strcat($$->code, newcode);
	}

strexp: CHAR {
		$$ = genNode($1->content, 0); 
		addChild($$, $1);
		setNodeType($$, st_char);

		// 中间代码生成
		// $$->code = "t1 = 'a'"
		$$->t_id = newTempID();
		sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
	} 
    | STRING {
		$$ = genNode($1->content, 0); 
		addChild($$, $1);
		setNodeType($$, st_string);

		// 中间代码生成
		// $$->code = "t1 = "aa""
		$$->t_id = newTempID();
		sprintf($$->code, "_t%d = %s\n", $$->t_id, $$->content);
	}
    
comparison:
      arithmeticexp '>' arithmeticexp {
		$$ = genNode("comparison", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name > $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		strcat($$->code, $3->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " > ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
	}
    | arithmeticexp '<' arithmeticexp {
		$$ = genNode("comparison", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name < $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		strcat($$->code, $3->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " < ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
		
	}
    | arithmeticexp '=' arithmeticexp {
		$$ = genNode("comparison", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name == $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		strcat($$->code, $3->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " == ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
		
	}
    | arithmeticexp GE arithmeticexp {
		$$ = genNode("comparison", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name >= $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		strcat($$->code, $3->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " >= ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
		
	}
    | arithmeticexp LE arithmeticexp {
		$$ = genNode("comparison", 0); 
		addChild($$, $1); addChild($$, $2); addChild($$, $3);
		setNodeType($$, st_bool);

		// 中间代码生成
		// $$->code = $1->code || $3->code || "$$->name = $1->name <= $3->name" 
		$$->t_id = newTempID();
		strcpy($$->code, $1->code);
		strcat($$->code, $3->code);
		char newcode[25];
		sprintf(newcode, "_t%d = ", $$->t_id);
		if($1->t_id == -1){ // 若 $1 为 ID
			strcat(newcode, $1->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $1->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, " <= ");
		if($3->t_id == -1){ // 若 $3 为 ID
			strcat(newcode, $3->content);
		} else{
			char id_name[5];
			sprintf(id_name, "_t%d", $3->t_id);
			strcat(newcode, id_name);
		}
		strcat(newcode, "\n");
		
		strcat($$->code, newcode);
		
	}

%%

// 生成一个内容为 content 行数为 line 的空节点
Node* genNode(char* content, int line){
	Node* p = NULL;
	if ((p = malloc(sizeof(Node))) == NULL){
		yyerror("out of memory");
	}
	p->content = strdup(content);
	p->cnum = 0;
	p->line = line;
	p->id = id++;
	p->t_id = -1;
	p->next = -1;
	for(int i = 0; i < 10; i++){
		p->children[i] = NULL;
	}
	return p;
}

// 为一个节点 p 添加一个子节点 child
void addChild(Node* p, Node* child){
	p->children[p->cnum] = child;
	p->cnum++;
}

// 递归释放以该节点为根的子树的空间
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

// 可视化生成树
void showNode(Node* p, int d, int i){
	if(p == NULL){
		return;
	}
	for(int i = 0; i < d; i++){
		printf("   ");
	}
	
	printf("(%d,%d) %s [next: %d] \n", d, i, p->content, p->next);
	// printf("(%d,%d) %s [type: %s] \n", d, i, p->content, type_string[(int)p->type]);
	for(int i = 0; i < p->cnum; i++){
		showNode(p->children[i], d+1, i+1);	
	}
}

// 设置节点类型
void setNodeType(Node*p, SymbolType type){
	p->type = type;
}


// 根据 变量声明部分 declaration 生成符号表
// Node *declaration 是以一行变量声明生成的子树
// 其左节点为变量类型，右节点为ID构成的子树
int updateSymbolTable(Node* declaration){
    if(declaration == NULL || declaration->children[0] == NULL || declaration->cnum == 0) {
        return 0;
    }
    enum SymbolType type;
    char typeSpecifier = declaration->children[0]->content[0]; // 类型的首字母
    switch (typeSpecifier) {
        case 'i':
            type = st_int;
            break;
        case 'f':
            type = st_float;
            break;
        case 'b':
            type = st_bool;
            break;
        case 'c':
            type = st_char;
            break;
        case 's':
            type = st_string;
            break;
    }
    appendSymbol(type, declaration->children[1]);
    return 1;
} 

// 更新符号表的同时更新节点的类型
void appendSymbol(enum SymbolType type, Node* node){
    if(node->line == 0) { // 处理非终结符号 varlist
        for(int i = 0; i < node->cnum; i++){
            appendSymbol(type, node->children[i]);
        }
    }
    else { // 处理终结符号 ID
        int len1 = strlen(node->content);
        for(int j = 0; j < symbolNum; j++){
            int len2 = strlen(symbolTable[j].id);
            if(len1 == len2 && memcmp(symbolTable[j].id, node->content, len1) == 0) {
                // 检测到符号表已经出现同名 ID
                fprintf(stderr, "Error at Line %02d: 重复定义变量 %s\n", node->line, node->content);
                exit(1);
            }    
        }
        symbolTable[symbolNum].type = type;
		node->type = type;
		node->t_id = -1;
        memcpy(symbolTable[symbolNum].id, node->content, len1);
        symbolNum++;
    }
}

// 符号表可视化
void showSymbolTable(){
    printf("\nSymbol Table \n");
    printf("      TYPE       ID        VAL\n");
    
    for(int i = 0; i < symbolNum; i++){
        printf("%3d %6s ", i, type_string[(int)symbolTable[i].type]);
        printf("%8s %10s\n", symbolTable[i].id, symbolTable[i].value);
    }
}

// 检查 ID 是否出现在符号表中，若不出现则报错
void checkID(Node* node) {
	int len1 = strlen(node->content);
	for(int j = 0; j < symbolNum; j++){
		int len2 = strlen(symbolTable[j].id);
		if(len1 == len2 && memcmp(symbolTable[j].id, node->content, len1) == 0) {
			// 在符号表中检测到了该 ID 名
			node->type = symbolTable[j].type;
			return;
		}    
	}
	// ID 不存在，出错
	fprintf(stderr, "Error at Line %02d: 使用未定义变量 %s\n", node->line, node->content);
    exit(1);
}


// 检查两个节点的类型是否相同，不同则出错
void checkType(Node *node1, Node* node2, int level) {
	if(level == 2){ // 针对赋值语句
		if(node1->type == st_float && node2->type == st_int){
			return;
		}
	}
	
	if(level == 1){ // 针对算术运算
		if((node1->type == st_float && node2->type == st_int) || (node1->type == st_int && node2->type == st_float))
		return;
	}
	
	if(node1->type != node2->type){
		fprintf(stderr, "Error at Line %02d: 类型不匹配 %s, %s\n", node1->line, node1->content, node2->content);
		exit(1);
	}
}

void getTreeCode(Node* p, int end){
	if(p == NULL){
		return;
	}

	char node_info[120];
	char node_name[100];
	if(p->type == st_null){
		sprintf(node_name, "%s",p->content);
	}
	else{
		sprintf(node_name, "%s(%s)",p->content, type_string[(int)p->type]);
	}
	
	sprintf(node_info, "id%d[label=\"%s\"]\n", p->id, node_name);
	strcat(map, node_info);
	
	
	for(int i = 0; i < p->cnum; i++){
		getTreeCode(p->children[i], 0);	
		char line_info[120];
		sprintf(line_info, "id%d->id%d\n", p->id, p->children[i]->id);
		strcat(map, line_info);
	}

	if(end == 1){
		char end_sign[5] = "}\n";
		strcat(map, end_sign);
		
		FILE* fp = fopen("./treemap.txt", "w");
		fputs(map, fp);
		fclose(fp);
		char header[150] = "digraph demo{\nnode [shape=box, style=\"rounded\", color=\"black\", fontname=\"Microsoft YaHei\"];\nedge [fontname=\"Microsoft YaHei\"];\n";
		strcpy(map, header);
	}
}

int newLabel(){
	return label_id++;
}

int newTempID(){
	return temp_id++;
}

// 因为我们有节点的全局ID 中间代码中每一个为定义next标号可以先用全局ID给他标记下来
// 这样对于一个中间代码文本中，我们可以找到他，并识别他的原本在语法树中的节点。
// 我们遍历一遍树，将必要的next = $$->next自顶向下更新。
// 同时我们每更新一个节点，就去中间代码串中寻找他的位置，并修改成我们新赋值的next值。

void UpdateNext(Node* root, char code[]){
	for(int i = 0; i < root->cnum; i++){
		Node* child = root->children[i];
		if(child->next == -1){
			child->next = root->next;
			char nullnext[25];
			char realnext[25];
			sprintf(nullnext, "__Label %03d__", child->id);
			sprintf(realnext, "Label %03d    ", root->next);
			// printf("%s,%s\n",nullnext, realnext);
			while(1){
				char* h = strstr(code, nullnext);
				if(h == NULL){
					break;
				}
				for(int i = 0; i < strlen(realnext); i++){
					h[i] = realnext[i];
				}
			}
		}
		UpdateNext(child, code);
	}
}




int main(void) {
	char infile[100];
	printf("Input File: \n");
	scanf("%s", infile);
	yyin = fopen(infile, "r");
	if(yyin == NULL){
		printf("Error: 文件无法打开\n");
		exit(1);
	}
	
	// printf("Line 01: ");

	yyparse();
	
	
	// 输出语法分析树
	// showNode(root, 0, 1); 

	// 输出符号表
	showSymbolTable();

	// 生成可视化语法树
	// 成在`treemap.txt`，然后用python运行`tree.py`即可生成可视化语法树`tree.png`。
	getTreeCode(root, 1);

	// 中间代码生成器：输出中间代码
	printf("\nCode:\n%s", root->code);

	// 释放内存
	freeNode(root);

	return 0;
}
