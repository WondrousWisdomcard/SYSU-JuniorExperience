#ifndef DF
#define DF

#define CHILD_ULIMIT 10
#define TABLE_SIZE 100
#define ID_SIZE 10
#define VALUE_SIZE 200
#define BUF_SIZE 1000

// 符号表和节点的类型 type 的取值
typedef enum SymbolType{
    st_null, st_int, st_float, st_char, st_string, st_bool
} SymbolType;

// 语法分析树的节点
typedef struct Node
{
    int id;
    char* content;  // 节点信息
    int line;       // 终结符号所在行编号（令非终结符号的line为0，以区分终结非终结符号）
    int cnum;       // 儿子节点的数量
    enum SymbolType type;   // 节点类型 
    struct Node* children[CHILD_ULIMIT]; // 儿子节点数组

    // 中间代码生成
    int t_id; // 临时变量编号 （ID的临时编号为-1）
    char code[BUF_SIZE];
    int next; // L 属性

} Node;

// 生成一个内容为 content 行数为 line 的空节点
Node* genNode(char* content, int line);

// 为一个节点 p 添加一个子节点 child
void addChild(Node* p, Node* child);
// 递归释放以该节点为根的子树的空间
void freeNode(Node* p);

// 可视化生成树
void showNode(Node* p, int d, int i);

// 生成 pydotplus 文本，用它可以生成可视化的语法分析树
// end = 1
void getTreeCode(Node* p, int end);

// 设置节点类型
void setNodeType(Node*p, SymbolType type);


// 符号表的基本单元
typedef struct Symbol
{
    enum SymbolType type;   // 符号表的类型
    char id[ID_SIZE];       // ID
    char value[VALUE_SIZE]; // 值
} Symbol;

// 为符号表添加一个新的符号
void appendSymbol(enum SymbolType type, Node *node);

// 符号表可视化
void showSymbolTable();

// 根据 变量声明部分 declaration 生成符号表
int updateSymbolTable(Node *declaration);

// 检查 ID 是否出现在符号表中，若不出现则报错
void checkID(Node *node);

// 检查两个节点的类型是否相同，不同则出错
void checkType(Node *node1, Node* node2, int level);

#endif
