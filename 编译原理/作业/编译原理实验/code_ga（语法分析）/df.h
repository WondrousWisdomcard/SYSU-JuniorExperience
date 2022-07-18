/**
 * Declarations of the syntax tree
 **/

#ifndef TREE
typedef struct Node
{
    char* content;
    int cnum;
    struct Node* children[10];
} Node;

Node* genNode(char* content);
void addChild(Node* p, Node* child);
void freeNode(Node* p);
void showNode(Node* p, int d, int i);
#endif
