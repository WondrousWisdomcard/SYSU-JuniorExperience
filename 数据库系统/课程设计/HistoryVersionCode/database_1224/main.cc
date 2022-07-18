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

// print B_Tree
void print_B_Tree(BTree *trees_, char *filename)
{

    FILE *fp;
    fp = fopen(filename, "w");
    if (fp == NULL)
    {
        printf("File can not open!");
        exit(0);
    }

    int start_block = trees_->root_;
    int end_block = trees_->root_;
    int newly_startblock;
    int newly_endblock;

    BIndexNode *index_child = NULL;

    // read root node
    char indexnode_level;
    int indexnode_num_entries;
    BIndexNode *indexnode_left_sibling;
    BIndexNode *indexnode_right_sibling;

    fprintf(fp, "root: block %d\n", start_block);
    index_child = new BIndexNode();
    index_child->init_restore(trees_, start_block);
    indexnode_level = index_child->get_level();
    indexnode_num_entries = index_child->get_num_entries();
    indexnode_left_sibling = index_child->get_left_sibling();
    indexnode_right_sibling = index_child->get_right_sibling();
    fprintf(fp, "\tlevel: %d \tnum_entries: %d\n", indexnode_level, indexnode_num_entries);
    for (int j = 0; j < indexnode_num_entries; ++j)
    {
        fprintf(fp, "\t\tkey: %f\tson: %d\n", index_child->get_key(j), index_child->get_son(j));
    }

    start_block = index_child->get_son(0);
    end_block = index_child->get_son(indexnode_num_entries - 1);
    delete index_child;
    index_child = NULL;

    // index node
    // from root to the leaf layer to layer
    while (start_block > 1)
    {
        for (int k = start_block; k <= end_block; k++)
        {
            fprintf(fp, "index: block %d\n", k);
            index_child = new BIndexNode();
            index_child->init_restore(trees_, k);
            indexnode_level = index_child->get_level();
            indexnode_num_entries = index_child->get_num_entries();
            indexnode_left_sibling = index_child->get_left_sibling();
            indexnode_right_sibling = index_child->get_right_sibling();
            fprintf(fp, "\tlevel: %d \tnum_entries: %d\n", indexnode_level, indexnode_num_entries);
            for (int j = 0; j < indexnode_num_entries; ++j)
            {
                fprintf(fp, "\t\tkey: %f\tson: %d\n", index_child->get_key(j), index_child->get_son(j));
            }
            if (k == start_block)
            {
                newly_startblock = index_child->get_son(0);
            }
            if (k == end_block)
            {
                newly_endblock = index_child->get_son(indexnode_num_entries - 1);
            }
            delete index_child;
            index_child = NULL;
        } // end for loop
        start_block = newly_startblock;
        end_block = newly_endblock;
    } // end while

    // leaf node variable
    BLeafNode *leaf_child = NULL;

    // read root node
    char leafnode_level;
    int leafnode_num_entries;
    int leafnode_num_keys;
    BLeafNode *leafnode_left_sibling;
    BLeafNode *leafnode_right_sibling;

    // print leaf node
    for (int k = start_block; k <= end_block; k++)
    {
        fprintf(fp, "leaf: block %d\n", k);
        leaf_child = new BLeafNode();
        leaf_child->init_restore(trees_, k);
        leafnode_level = leaf_child->get_level();
        leafnode_num_entries = leaf_child->get_num_entries();
        leafnode_left_sibling = leaf_child->get_left_sibling();
        leafnode_right_sibling = leaf_child->get_right_sibling();
        leafnode_num_keys = leaf_child->get_num_keys();
        fprintf(fp, "\tlevel: %d \tnum_entries: %d\tnum_keys: %d\n", leafnode_level, leafnode_num_entries, leafnode_num_keys);
        for (int j = 0; j < leafnode_num_keys; ++j)
        {
            int count_entries = 0;
            fprintf(fp, "\t\tkey: %f\n", leaf_child->get_key(j));
            for (int w = count_entries; w < std::min(count_entries + 16, leafnode_num_entries); w++)
            {
                fprintf(fp, "\t\t\tid: %d\n", leaf_child->get_entry_id(w));
            }
            count_entries += 16;
        }
        delete leaf_child;
        leaf_child = NULL;
    }

    fclose(fp);
}

// -----------------------------------------------------------------------------
int main(int nargs, char **args)
{

    char data_file[200];
    char tree_file_ser[200];
    char tree_file_par[200];
    int B_ = 512; // node size
    int n_pts_ = 20000000;

    strncpy(data_file, "./data/dataset.csv", sizeof(data_file));
    strncpy(tree_file_ser, "./result/B_tree_ser", sizeof(tree_file_ser));
    strncpy(tree_file_par, "./result/B_tree_par", sizeof(tree_file_par));

    printf("data_file   = %s\n", data_file);
    printf("tree_file_ser   = %s\n", tree_file_ser);
    printf("tree_file_par   = %s\n", tree_file_par);

    Result *table = new Result[n_pts_];

    ifstream fp(data_file);
    string line;
    int i = 0;
    while (getline(fp, line) && i <= n_pts_ - 1)
    {
        string number;
        istringstream readstr(line);

        getline(readstr, number, ',');
        table[i].key_ = atof(number.c_str());

        getline(readstr, number, ',');
        table[i].id_ = atoi(number.c_str());
        i++;
    }

    fp.close();

    timeval start_t;
    timeval end_t;

    BTree *trees_ = new BTree();
    trees_->init(B_, tree_file_ser);
    gettimeofday(&start_t, NULL);

    if (trees_->bulkload(n_pts_, table))
        return 1;
    gettimeofday(&end_t, NULL);

    float run_t1 = end_t.tv_sec - start_t.tv_sec +
                   (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
    printf("串行运行时间: %f  s\n", run_t1);
    print_B_Tree(trees_, "./result/ser_res");
    delete trees_;

    trees_ = new BTree();

    trees_->init(B_, tree_file_par);
    gettimeofday(&start_t, NULL);

    if (trees_->parallelBulkLoad(n_pts_, table, 8, 500))
        return 1;
    gettimeofday(&end_t, NULL);

    run_t1 = end_t.tv_sec - start_t.tv_sec +
             (end_t.tv_usec - start_t.tv_usec) / 1000000.0f;
    printf("并行运行时间: %f  s\n", run_t1);
    print_B_Tree(trees_, "./result/par_res");

    if (table != NULL)
    {
        delete[] table;
        table = NULL;
    }

    char systemCmd[1024];
    strncpy(systemCmd, "diff ", 1024);
    strcat(systemCmd, "./result/par_res ");
    strcat(systemCmd, "./result/ser_res");
    printf("%s\n", systemCmd);
    system(systemCmd);
    return 0;
}
