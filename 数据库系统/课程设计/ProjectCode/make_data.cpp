#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <fstream>

using namespace std;

#define Random(x) (rand() % x)

struct Result
{ // basic data structure
	float key_;
	int id_;
};

int ResultComp(		// compare function for qsort (ascending)
	const void *e1, // 1st element
	const void *e2) // 2nd element
{
	int ret = 0;
	Result *item1 = (Result *)e1;
	Result *item2 = (Result *)e2;

	if (item1->key_ < item2->key_)
	{
		ret = -1;
	}
	else if (item1->key_ > item2->key_)
	{
		ret = 1;
	}
	else
	{
		if (item1->id_ < item2->id_)
			ret = -1;
		else if (item1->id_ > item2->id_)
			ret = 1;
	}
	return ret;
}

int main()
{
	srand((int)time(NULL));
	int n = 20000000;	 //表示点的个数，自己定义
	int range = 20000000; //表示值的范围，自己定义
	Result *table = new Result[n];
	printf("Generate Data...\n");
	for (int i = 0; i < n; i++)
	{
		table[i].id_ = i;			   //value值
		table[i].key_ = Random(range); //key值
	}

	printf("Sort Data...\n");
	qsort(table, n, sizeof(Result), ResultComp);

	printf("Write Data...\n");
	ofstream outFile;
	outFile.open("./data/dataset.csv", ios::out);
	for (int i = 0; i < n; i++)
	{
		outFile << table[i].key_ << ',' << table[i].id_ << endl;
		if (i % 1000000 == 0)
		{
			printf("%d\n", i);
		}
	}

	outFile.close();

	return 0;
}
