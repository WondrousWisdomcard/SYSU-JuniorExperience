#include <iostream>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include <cstdlib>
#include <cstring>

#include "def.h"
#include "util.h"
#include "random.h"
#include "pri_queue.h"
#include "b_node.h"
#include "b_tree.h"

using namespace std;

#define Random(x) (rand() % x)
#define DEFAULT_THREAD_NUM 2
#define DEFAULT_BUFFER_SIZE 500
#define DEFAULT_ENTRY_NUM 10000000


void make_data(int n)
{
	srand((int)time(NULL));
	int range = 20; //表示值的范围，自己定义
	Result *table = new Result[n];
	printf("Generate Data...\n");
	for (int i = 0; i < n; i++)
	{
		table[i].id_ = i;			   //value值
		table[i].key_ = Random(range); //key值
	}

	//printf("Sort Data...\n");
	qsort(table, n, sizeof(Result), ResultComp);

	//printf("Write Data...\n");
	ofstream outFile;
	outFile.open("./data/dataset.csv", ios::out);
	for (int i = 0; i < n; i++)
	{
		outFile << table[i].key_ << ',' << table[i].id_ << endl;
	}

	outFile.close();
}


void evaluate(){
    char data_file[200];
    char tree_file_ser[200];
	char tree_file_par[200];
    int  B_ = 512; // node size
    ofstream outFile;
	
    int threadNum[] = {1,2,3,4,5,6,7,8,9,10,15,20,30,40,50};//15
    int bufferSize[] = {10,50,100,200,300,500,1000,2000};//8
    int entryNum[] = {100,1000,10000,100000,1000000,10000000};//6

    make_data(DEFAULT_ENTRY_NUM);
    outFile.open("./result/result_threadNum.csv", ios::out);
    outFile<<"threadNum  sertime  partime"<<endl;

    strncpy(data_file, "./data/dataset.csv", sizeof(data_file));
    

    //1. threadNum
    printf("结果存放于./result/result_threadNum.csv\n");
    for(int i = 0;i < 15;++i){
        Result *table = new Result[DEFAULT_ENTRY_NUM]; 
        ifstream fp(data_file); 
        string line;
        int k = 0;
        while (getline(fp,line) && k <= DEFAULT_ENTRY_NUM - 1){ 
            string number;
            istringstream readstr(line); 
            
            getline(readstr,number,','); 
            table[k].key_ = atof(number.c_str()); 

            getline(readstr,number,','); 
            table[k].id_ = atoi(number.c_str());    
            k++;
        }
    
        fp.close();

        timeval start_t;  
        timeval end_t;

        BTree* trees_ = new BTree();
        trees_->init(B_, tree_file_ser);
        gettimeofday(&start_t,NULL);
        
        if (trees_->bulkload(DEFAULT_ENTRY_NUM, table)) return ;

        gettimeofday(&end_t, NULL);
        float run_t1 = end_t.tv_sec - start_t.tv_sec + 
                            (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
        //printf("串行运行时间: %f  s\n", run_t1);
        delete trees_;
        //-------------------------------------------------------------------------------
        trees_ = new BTree();
        
        trees_->init(B_, tree_file_par);
        gettimeofday(&start_t,NULL);
        
        if (trees_->parallelBulkLoad(DEFAULT_ENTRY_NUM, table, threadNum[i], DEFAULT_BUFFER_SIZE)) return ;
        gettimeofday(&end_t, NULL);

        float run_t2 = end_t.tv_sec - start_t.tv_sec + 
                            (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
        //printf("并行运行时间: %f  s\n", run_t1);
        
        
        if(table != NULL){
            delete[] table; 
            table = NULL;
        }
        outFile<<threadNum[i]<<"  "<<run_t1<<"  "<<run_t2<<endl;
    }
    outFile.close();


    //2. bufferSize
    outFile.open("./result/result_bufferSize.csv", ios::out);
    outFile<<"bufferSize  sertime  partime"<<endl;
    printf("结果存放于./result/result_bufferSize.csv\n");
    for(int i = 0;i < 8;++i){
        Result *table = new Result[DEFAULT_ENTRY_NUM]; 
        ifstream fp(data_file); 
        string line;
        int k = 0;
        while (getline(fp,line) && k <= DEFAULT_ENTRY_NUM - 1){ 
            string number;
            istringstream readstr(line); 
            
            getline(readstr,number,','); 
            table[k].key_ = atof(number.c_str()); 

            getline(readstr,number,','); 
            table[k].id_ = atoi(number.c_str());    
            k++;
        }
    
        fp.close();
        timeval start_t;  
        timeval end_t;

        BTree* trees_ = new BTree();
        trees_->init(B_, tree_file_ser);
        gettimeofday(&start_t,NULL);
        
        if (trees_->bulkload(DEFAULT_ENTRY_NUM, table)) return ;

        gettimeofday(&end_t, NULL);
        float run_t1 = end_t.tv_sec - start_t.tv_sec + 
                            (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
        //printf("串行运行时间: %f  s\n", run_t1);
        delete trees_;
        //-------------------------------------------------------------------------------
        trees_ = new BTree();
        
        trees_->init(B_, tree_file_par);
        gettimeofday(&start_t,NULL);
        
        if (trees_->parallelBulkLoad(DEFAULT_ENTRY_NUM, table,DEFAULT_THREAD_NUM, bufferSize[i])) return ;
        gettimeofday(&end_t, NULL);

        float run_t2 = end_t.tv_sec - start_t.tv_sec + 
                            (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
        //printf("并行运行时间: %f  s\n", run_t1);
        
        
        if(table != NULL){
            delete[] table; 
            table = NULL;
        }
        outFile<<bufferSize[i]<<"  "<<run_t1<<"  "<<run_t2<<endl;
    }
    outFile.close();


    outFile.open("./result/result_entryNum.csv", ios::out);
    outFile<<"entryNum  sertime  partime"<<endl;
    printf("结果存放于./result/result_entryNum.csv\n");
    for(int i = 0;i < 6;++i){
        make_data(entryNum[i]);

        strncpy(data_file, "./data/dataset.csv", sizeof(data_file));
        strncpy(tree_file_ser, "./result/B_tree_ser", sizeof(tree_file_ser));
        strncpy(tree_file_par, "./result/B_tree_par", sizeof(tree_file_par));

        Result *table = new Result[entryNum[i]]; 

        ifstream fp(data_file); 
        string line;
        int k = 0;
        while (getline(fp,line) && k <= entryNum[i] - 1){ 
            string number;
            istringstream readstr(line); 
            
            getline(readstr,number,','); 
            table[k].key_ = atof(number.c_str()); 

            getline(readstr,number,','); 
            table[k].id_ = atoi(number.c_str());    
            k++;
        }
        
        fp.close();

        timeval start_t;  
        timeval end_t;

        BTree* trees_ = new BTree();
        trees_->init(B_, tree_file_ser);
        gettimeofday(&start_t,NULL);
        
        if (trees_->bulkload(entryNum[i], table)) return ;

        gettimeofday(&end_t, NULL);
        float run_t1 = end_t.tv_sec - start_t.tv_sec + 
                            (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
        //printf("串行运行时间: %f  s\n", run_t1);
        delete trees_;
        //-------------------------------------------------------------------------------
        trees_ = new BTree();
        
        trees_->init(B_, tree_file_par);
        gettimeofday(&start_t,NULL);
        
        if (trees_->parallelBulkLoad(entryNum[i], table, DEFAULT_THREAD_NUM, DEFAULT_BUFFER_SIZE)) return ;
        gettimeofday(&end_t, NULL);

        float run_t2 = end_t.tv_sec - start_t.tv_sec + 
                            (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
        //printf("并行运行时间: %f  s\n", run_t1);
        
        
        if(table != NULL){
            delete[] table; 
            table = NULL;
        }
        outFile<<entryNum[i]<<"  "<<run_t1<<"  "<<run_t2<<endl;
    }
    outFile.close();
}