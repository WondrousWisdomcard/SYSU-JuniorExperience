lex la.l
yacc -d ga.y 
gcc df.h lex.yy.c y.tab.c -o sa.out
