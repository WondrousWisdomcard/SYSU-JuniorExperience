#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <string>
#include <set>
#include <fstream>
#include <sstream>

#include "def.h"
#include "util.h"
#include "random.h"
#include "pri_queue.h"
#include "b_node.h"
#include "b_tree.h"

using namespace std;


// -----------------------------------------------------------------------------
int main(int nargs, char **args)
{    

	char data_file[200];
	char tree_file[200];
	int  B_ = 512; // node size
	int n_pts_ = 1000000;

	strncpy(data_file, "./data/dataset.csv", sizeof(data_file));
	strncpy(tree_file, "./result/B_tree", sizeof(tree_file));
	printf("data_file   = %s\n", data_file);
	printf("tree_file   = %s\n", tree_file);

	Result *table = new Result[n_pts_]; 

	ifstream fp(data_file); 
	string line;
	int i=0;
	while (getline(fp,line)){ 
        string number;
        istringstream readstr(line); 
        
		getline(readstr,number,','); 
		table[i].key_ = atof(number.c_str()); 

		getline(readstr,number,','); 
		table[i].id_ = atoi(number.c_str());    
        i++;
    }
	
	fp.close();

	timeval start_t;  
    timeval end_t;

	gettimeofday(&start_t,NULL);
		
	BTree* trees_ = new BTree();
	trees_->init(B_, tree_file);
	//对这个函数进行并行
	if (trees_->bulkload(n_pts_, table)) return 1;

	delete[] table; table = NULL;

	gettimeofday(&end_t, NULL);

	float run_t1 = end_t.tv_sec - start_t.tv_sec + 
						(end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
	printf("运行时间: %f  s\n", run_t1);
	

	return 0;
}
