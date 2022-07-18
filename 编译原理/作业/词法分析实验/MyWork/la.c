#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SIZE_1 2048
#define SIZE_2 128

// - Data Structure --------- --------- --------- --------- --------- --------- --------- --------- 

enum TOKEN_TYPE {
    // Keyword tokens                   // |-18 Keywords-----------|
    KEY_OR, KEY_AND, KEY_NOT,           // | or    | and   | not   |    
    KEY_INT, KEY_BOOL, KEY_CHAR,        // | int   | bool  | char  |    
    KEY_WHILE, KEY_DO,                  // | while | do    |       |    
    KEY_IF, KEY_THEN, KEY_ELSE,         // | if    | then  | else  |    
    KEY_END, KEY_REPEAT, KEY_UNTIL,     // | end   | repeat| until |    
    KEY_READ, KEY_WRITE,                // | read  | write |       | 
    KEY_TRUE, KEY_FALSE,                // | true  | false |       | 

    // Operator tokens                  // |-17 Operators-|
    OP_G, OP_L, OP_ASSIGN,              // | >  | <  | := |  
    OP_GE, OP_LE, OP_EQ,                // | >= | <= | =  |
    OP_COMMA, OP_QUOTA, OP_SEMI,        // | ,  | '  | ;  |
    OP_LPAREN, OP_RPAREN,               // | (  | )  |    |
    OP_LBRACE, OP_RBRACE,               // | {  | }  |    |
    OP_ADD, OP_SUB,                     // | +  | -  |    |
    OP_MUL, OP_DIV,                     // | *  | /  |    |

    // Other tokens     // |-Each NF--------------------|-Example-|
    ID,                 // | letter(letter|digit)*      | c1      |
    NUM,                // | digit digit*               | 123     |
    STRING,             // | ' any character except' '  | 'hi!'   |
    NONE,               // |                            | 1c      |
    ANNO                // | { any character }          | {hi}    |
};

// We have token_strings[i] corrsponding to TOKEN_TYPE i
char* token_strings[] = { 
    // Keyword tokens
    "KEY_OR", "KEY_AND", "KEY_NOT",  
    "KEY_INT", "KEY_BOOL", "KEY_CHAR", 
    "KEY_WHILE", "KEY_DO",
    "KEY_IF", "KEY_THEN", "KEY_ELSE",  
    "KEY_END", "KEY_REPEAT", "KEY_UNTIL",  
    "KEY_READ", "KEY_WRITE", 
    "KEY_TRUE", "KEY_FALSE", 
    // Operator tokens
    "OP_G", "OP_L", "OP_ASSIGN",
    "OP_GE", "OP_LE", "OP_EQ",
    "OP_COMMA", "OP_QUOTA", "OP_SEMI",
    "OP_LPAREN", "OP_RPAREN", "OP_LBRACE", "OP_RBRACE",               
    "OP_ADD", "OP_SUB", "OP_MUL", "OP_DIV",
    // Other tokens
    "ID", "NUM", "STRING", "NONE", "ANNO"     
    };

int tokens_size = 35;
char* tokens[] = { 
    // 18 Keyword tokens
    "or", "and", "not",  
    "int", "bool", "char", 
    "while", "do",
    "if", "then", "else",  
    "end", "repeat", "until",  
    "read", "write",  
    "true", "false",
    // 17 Operator tokens
    ">", "<", ":=",
    ">=", "<=", "=",
    ",", "\'", ";",
    "(", ")", "{", "}",               
    "+", "-", "*", "/",          
    };

char* getTokenName(enum TOKEN_TYPE i){
    return token_strings[i];
}

enum TOKEN_TYPE getTokenType(char *token){
    for(int i = 0; i < tokens_size; i++){
        if(strcmp(tokens[i], token) == 0){
            return (enum TOKEN_TYPE)i;
        }
        
    }
    return NONE;
} 

// - Took Function --------- --------- --------- --------- --------- --------- --------- --------- 

/**
 * 判断字符 c 是否为数字
 */
int isDigit(char c){
    if(c >= '0' && c <= '9')
        return 1;
    else
        return 0;
}

/**
 * 判断字符 c 是否为字母
 */
int isLetter(char c){
    if(c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z')
        return 1;
    else
        return 0;
}

/**
 * 判断字符 c 是否为分隔符
 */
int isSeparator(char c){
    if(c == ' ' || c == '\t' || c == '\n')
        return 1;
    else
        return 0;
}

/**
 * 判断字符 c 是否为操作符里的出现的字符
 */
int isOperatorChar(char c){
    int char_list_size = 12;
    char char_list[] = {
        '>', '<', '=',
        ':', ';', ',',
        '(',')',
        '+', '-', '*', '/'
        };

    for(int i = 0; i < char_list_size; i++){
        if(c == char_list[i]){
            return 1;
        }
    }
    return 0;
}

// - Lexical Analysis --------- --------- --------- --------- --------- --------- --------- --------- 

/**
 * 结构体 TOKEN：由一个 Lexieme 和 Information 组成：例如整型变量 99 的对应 TOKEN 就是 [ID, 99]
 */
typedef struct TOKEN{
    enum TOKEN_TYPE type;
    char info[SIZE_2];
}TOKEN;

FILE* file;
TOKEN file_tokens[SIZE_1];
int file_tokens_num;

int current_row;
int current_col;
char current_word[SIZE_2];
int current_word_ptr;
enum TOKEN_TYPE current_type;
int operator_flag = 0;

int error;

/**
 * 初始化：为所有用到的变量（@line 136- 147）赋初始值，若文件无啊打开，提示报错。
 * @param file_path
 * @return 1 if the file is opened successfully, otherwise 0. 
 */
int la_initial(char file_path[]){

    if(file != NULL){
        fclose(file);
    }
    file = fopen(file_path, "r");  
    if(file == NULL){
        printf("[ERROR] Failed to open test file: %s\n", file_path);
        return 0;
    }  

    current_row = 0;
    current_col = 0;
    current_word[0] = '\0';
    current_word_ptr = 0;
    current_type = NONE;
    error = 0;
    file_tokens_num = 0;

    for(int i = 0; i < SIZE_1; i++){
        file_tokens[i].type = NONE;
        for(int j = 0; j < SIZE_2; j++){
            file_tokens[i].info[j] = '\0';
        }
    }

    return 1;
}

/**
 * 输出词法编译结果：每行为一个 Tokens，由一个 Lexieme 和 Info 组成。
 */
void la_show_result(){
    for(int i = 0; i < file_tokens_num; i++){
        printf("%-10s [%s] \n", getTokenName(file_tokens[i].type), file_tokens[i].info);
    }
}

/**
 * 输出词法编译结果：显示出错原因和出错位置（几行几列）
 */
void la_show_error(const char* message, int row, int col){
    printf("[ERROR] In %d:%d: %s\n", row, col, message);
}

/**
 * 根据当前的 current_word 和 current_type 生成 Tokens 并保存在 file_tokens 中。
 */
void la_make_token(){
    
    if(current_type != ANNO && current_word_ptr != 0){
        current_word[current_word_ptr] = '\0';
        if(current_type == NONE || current_type == ID && getTokenType(current_word) != NONE){
            file_tokens[file_tokens_num].type = getTokenType(current_word);
        }
        else{
            file_tokens[file_tokens_num].type = current_type;
        }
        
        // // Error Detecting on NUM And ID like "1c"
        // if(file_tokens[file_tokens_num].type == NONE){
        //     la_show_error("Illegal Number/ID", current_row, current_col);
        //     error++;
        // }

        for(int i = 0; i < current_word_ptr; i++){
            file_tokens[file_tokens_num].info[i] = current_word[i];
        }
        file_tokens_num++;
    }

    current_word[0] = '\0';
    current_word_ptr = 0;
    current_type = NONE;
    operator_flag = 0;
}

/**
 * 在扫描新的一行时进行预处理
 */
void la_update_line(){
    current_row++; 
    current_col = 0;
    if(current_type != ANNO){
        current_type = NONE;
    }
    operator_flag = 0;
}

/**
 * 根据下一个字符 c 来更新 current_word 和 current_type。
 * @param c lookahead symbol
 */
void la_update_word(char c){

    if(current_word_ptr != 0){
        if(c == '}' && current_type == ANNO || c == '\'' && current_type == STRING){
            current_word[current_word_ptr] = c;
            current_word_ptr++;
            la_make_token();
            return;
        }

        if(c == '{' && current_type != STRING){
            la_make_token();
            current_type = ANNO;
            return;
        }
        else if(c == '\'' && current_type != STRING && current_type != ANNO){
            la_make_token();
            current_type = STRING;
            return;
        }
    }
    else {
        if(c == '{'){
            current_type = ANNO;
        }
        else if(c == '\''){
            current_type = STRING;
        }
        else if(c == '}'){
            return;
        }
        else{
            if(isDigit(c)){
                current_type = NUM;
            }
            else if(isLetter(c)){
                current_type = ID;
            }
            else if(isOperatorChar(c)){
                operator_flag = 1;
            }
            else if(isSeparator(c)){
                if(c == '\n'){
                    // We allow annoation that cross over lines
                    // But string that cross over line is illegal
                    if(current_type == ANNO){
                        current_word[current_word_ptr] = c;
                        current_word_ptr++;
                    }
                    else if(current_type == STRING){
                        la_show_error("Unclosed String", current_row, current_col);
                        la_make_token();
                    }
                    else{
                        if(current_word_ptr != 0){
                            la_make_token();
                        }
                    }
                }
                la_update_line();
                return;
            }
            else{
                char errMsg[SIZE_2];
                sprintf(errMsg, "Illegal Symbol: %c", c);
                la_show_error(errMsg, current_row, current_col);
                error++;
            }
        }
    }

    if(isSeparator(c)){         
        // Make token when meeting a separator 
        if(current_type != STRING && current_type != ANNO){
            if(current_word_ptr != 0){
                la_make_token();
            }
            return;
        }        
    }

    if(current_type == NUM && isLetter(c)){
        la_show_error("Illegal Number/ID", current_row, current_col);
        error++;
    }

    current_word[current_word_ptr] = c;
    current_word_ptr++;
}

/**
 * 执行文件字符扫描和词法分析，在出现错误时或读完程序时终止
 */
void la_start(){
    current_row++;
    while(error == 0){
        int res = fgetc(file);
        char c;

        // Case 1: Consider to make a token when finshing reading source code
        if(res == -1){
            if(current_type == ANNO){
                la_show_error("Unclosed Annoation, lack of '}'", current_row, current_col);
                error++;
            }
            else if(current_type == STRING){
                la_show_error("Unclosed Statement, lack of '", current_row, current_col);
                error++;
            }
            if(current_word_ptr != 0){
                la_make_token();
            }
            break;
        }
        else{
            c = (char)res;        
            current_col++;
        }

        // Case 2: Considet to make a token of operator like + or :=
        if(operator_flag == 1 && current_word_ptr != 0){
            char lookahead_word[SIZE_2];
            memcpy(lookahead_word, current_word, SIZE_2);
            lookahead_word[current_word_ptr] = c;

            if(isOperatorChar(c) == 0 || getTokenType(current_word) != NONE \
                && getTokenType(lookahead_word) == NONE){
                la_make_token();
            }
        }

        // Case 3: Froce to make a token when next char is an operator char
        if(isOperatorChar(c) && current_word_ptr != 0 && operator_flag == 0 \
            && current_type != ANNO && current_type != STRING){
            // Beacuse opeartor char in string("...") and annoation({...}) 
            // is premited, so there has 2 limits on current_type
            la_make_token();
        }

        // Case 4: Ivalid Right Brace
        if(c == '}' && current_type != ANNO && current_type != STRING){
            la_show_error("Unclosed Annoation, lack of '{'", current_row, current_col);
            error++;
        }

        // Step after making token cases: Add c to current_word
        la_update_word(c); 
    }
    if(current_word_ptr != 0){
        la_make_token();
    }
}

// - Main Function --------- --------- --------- --------- --------- --------- --------- ---------

/**
 * 每次输入一个文件路径，程序读取文件内容并作语法分析，将词法分析结果直接输出
 */
int main(int argc, char* argv[]){

    printf("\n+ TINY+ Lexical Analysis Program\n\n");
    
    int test_case = 0;
    int success_case = 0;

    while(1){
        char file_path[256];
        printf("Please enter the path of test file:(\"q\" to quit)\n");
        scanf("%s", file_path);
        if(strcmp(file_path, "q") == 0){
            break;
        }

        if(la_initial(file_path)){
            la_start();
            if(error == 0)
                la_show_result();
        }
    }
    
    return 0;
}