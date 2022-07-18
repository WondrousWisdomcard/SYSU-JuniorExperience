SRCS=random.cc pri_queue.cc util.cc block_file.cc b_node.cc b_tree.cc \
	main.cc
OBJS=${SRCS:.cc=.o}

CXX=g++ -std=c++11 -g
CPPFLAGS=-w

.PHONY: clean

all: ${OBJS}
	${CXX} ${CPPFLAGS} -o run ${OBJS}

random.o: random.h

pri_queue.o: pri_queue.h

util.o: util.h

block_file.o: block_file.h

b_node.o: b_node.h

b_tree.o: b_tree.h

main.o:

clean:
	-rm ${OBJS}
