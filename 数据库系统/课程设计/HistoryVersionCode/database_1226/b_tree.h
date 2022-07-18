#ifndef __B_TREE_H
#define __B_TREE_H

#include <iostream>
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstring>

#include "def.h"
#include "util.h"
#include "block_file.h"
#include "b_node.h"
#include <pthread.h>

class BlockFile;
class BNode;
class BLeafNode;
class BIndexNode;
struct Result;

// -----------------------------------------------------------------------------
//  BTree: b-tree to index hash tables produced by qalsh
// -----------------------------------------------------------------------------
class BTree
{
public:
	int root_;		  // address of disk for root
	BNode *root_ptr_; // pointer of root
	BlockFile *file_; // file in disk to store

	// -------------------------------------------------------------------------
	BTree();  // default constructor
	~BTree(); // destructor

	// -------------------------------------------------------------------------
	void init(				// init a new b-tree
		int b_length,		// block length
		const char *fname); // file name

	// -------------------------------------------------------------------------
	void init_restore(		// load an exist b-tree
		const char *fname); // file name

	// -------------------------------------------------------------------------
	int bulkload(			  // bulkload b-tree from hash table in mem
		int n,				  // number of entries
		const Result *table); // hash table

	//--------------------------------------------------------------------------
	int parallelBulkLoad(
		int n,				 // number of entries
		const Result *table, // hash table
		int maxThreadNum,	 // max thread num
		int maxBufferBlock	 // max number of blocks in buffer
	);

	// -------------------------------------------------------------------------
	/*
		start routine of thread, this function will put n entries into serveral
		blocks, every leaf node will be as full as possible
	*/
	static void *batchLoadLeaf(void *args);

	// -------------------------------------------------------------------------
	static void *batchLoadIndex(void *args);

	static void *loadBlockToDisk(void *args);

protected:
	// -------------------------------------------------------------------------
	inline int read_header(const char *buf)
	{ // read <root> from buffer
		memcpy(&root_, buf, SIZEINT);
		return SIZEINT;
	}

	// -------------------------------------------------------------------------
	inline int write_header(char *buf)
	{ // write <root> into buffer
		memcpy(buf, &root_, SIZEINT);
		return SIZEINT;
	}
 
	// -------------------------------------------------------------------------
	void load_root(); // load root of b-tree

	// -------------------------------------------------------------------------
	void delete_root(); // delete root of b-tree

	//--------------------------------------------------------------------------
	int *alloc_blocks( // allocate n empty blocks in the block file
		int n);		   // returns an array of indexs of blocks that were allocated

	//--------------------------------------------------------------------------
	void write_leaf_blocks( // write n blocks to the block file
		BLeafNode * nodes[],
		int firstBlock,
		int n);
		
	//--------------------------------------------------------------------------
	void write_index_blocks( // write n blocks to the block file
		BIndexNode* nodes[],
		int firstBlock,
		int n);
};

// -------------------------------------------------------------------------
/*
	shared memory for threads
*/

typedef struct
{
	const Result *hashTable;   // hash table that store entries
	int entryNum;			   // the number of entries that the function needs to load
	int *blockIndex;		   // the index of block that allocated for these entries
	int blockIndexLen;		   // the length of array blockIndex
	int blockIndexStart;	   // the start index of array blockIndex
	int blockIndexEnd;		   // the end index of array blockIndex
	int maxBlock;			   // the maxium number of block in memory that the function can allocate
	int minBlock;			   // I don't want some thread write out one node for an I/O
	BTree *bTree;			   // the btree that these nodes should belongs to
	pthread_mutex_t *fileLock; // prevent multi-thread access file
} BatchLoadLeafArgs;

typedef struct
{
	int *sonBlockTable;		   // hash table that store entries
	float *sonKeyTable;		   // table that store sons' key index
	int son_num;			   // the number of entries that the function needs to load
	int currentLevel;		   // layers level
	int *blockIndex;		   // the index of block that allocated for these entries
	int blockIndexLen;		   // the length of array blockIndex
	int blockIndexStart;	   // the start index of array blockIndex
	int blockIndexEnd;		   // the end index of array blockIndex
	int maxBlock;			   // the maxium number of block in memory that the function can allocate
	int minBlock;			   // I don't want some thread write out one node for an I/O
	BTree *bTree;			   // the btree that these nodes should belongs to
	pthread_mutex_t *fileLock; // prevent multi-thread access file
} BatchLoadIndexArgs;

#endif // __B_TREE_H
