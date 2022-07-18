     #include "b_tree.h"

// -----------------------------------------------------------------------------
//  BTree: b-tree to index hash values produced by qalsh
// -----------------------------------------------------------------------------
BTree::BTree() // default constructor
{
	root_ = -1;
	file_ = NULL;
	root_ptr_ = NULL;
}

// -----------------------------------------------------------------------------
BTree::~BTree() // destructor
{
	char *header = new char[file_->get_blocklength()];
	write_header(header);	   // write <root_> to <header>
	file_->set_header(header); // write back to disk
	delete[] header;
	header = NULL;

	if (root_ptr_ != NULL)
	{
		delete root_ptr_;
		root_ptr_ = NULL;
	}
	if (file_ != NULL)
	{
		delete file_;
		file_ = NULL;
	}
}

// -----------------------------------------------------------------------------
void BTree::init(	   // init a new tree
	int b_length,	   // block length
	const char *fname) // file name
{
	FILE *fp = fopen(fname, "r");
	if (fp)
	{				// check whether the file exist
		fclose(fp); // ask whether replace?
		// printf("The file \"%s\" exists. Replace? (y/n)", fname);

		// char c = getchar();			// input 'Y' or 'y' or others
		// getchar();					// input <ENTER>
		// assert(c == 'y' || c == 'Y');
		remove(fname); // otherwise, remove existing file
	}
	file_ = new BlockFile(b_length, fname); // b-tree stores here

	// -------------------------------------------------------------------------
	//  init the first node: to store <blocklength> (page size of a node),
	//  <number> (number of nodes including both index node and leaf node),
	//  and <root> (address of root node)
	// -------------------------------------------------------------------------
	root_ptr_ = new BIndexNode();
	root_ptr_->init(0, this);
	//返回BIndexNode中的变量block_
	root_ = root_ptr_->get_block();
	//释放root-ptr的内存
	delete_root();
}

// -----------------------------------------------------------------------------
void BTree::init_restore( // load the tree from a tree file
	const char *fname)	  // file name
{
	FILE *fp = fopen(fname, "r"); // check whether the file exists
	if (!fp)
	{
		printf("tree file %s does not exist\n", fname);
		exit(1);
	}
	fclose(fp);

	// -------------------------------------------------------------------------
	//  it doesn't matter to initialize blocklength to 0.
	//  after reading file, <blocklength> will be reinitialized by file.
	// -------------------------------------------------------------------------
	file_ = new BlockFile(0, fname);
	root_ptr_ = NULL;

	// -------------------------------------------------------------------------
	//  read the content after first 8 bytes of first block into <header>
	// -------------------------------------------------------------------------
	char *header = new char[file_->get_blocklength()];
	file_->read_header(header); // read remain bytes from header
	read_header(header);		// init <root> from <header>

	delete[] header;
	header = NULL;
}
// -----------------------------------------------------------------------------
int BTree::bulkload(	 // bulkload a tree from memory
	int n,				 // number of entries
	const Result *table) // hash table
{
	BIndexNode *index_child = NULL;
	BIndexNode *index_prev_nd = NULL;
	BIndexNode *index_act_nd = NULL;
	BLeafNode *leaf_child = NULL;
	BLeafNode *leaf_prev_nd = NULL;
	BLeafNode *leaf_act_nd = NULL;

	int id = -1;
	int block = -1;
	float key = MINREAL;

	// -------------------------------------------------------------------------
	//  build leaf node from <_hashtable> (level = 0)
	// -------------------------------------------------------------------------
	bool firstNode = true; // determine relationship of sibling
	int startBlock = 0;	   // position of first node
	int endBlock = 0;	   // position of last node

	for (int i = 0; i < n; ++i)
	{
		id = table[i].id_;
		key = table[i].key_;

		if (!leaf_act_nd)
		{
			leaf_act_nd = new BLeafNode();
			leaf_act_nd->init(0, this);

			if (firstNode)
			{
				firstNode = false; // init <startBlock>
				startBlock = leaf_act_nd->get_block();
			}
			else
			{ // label sibling
				leaf_act_nd->set_left_sibling(leaf_prev_nd->get_block());
				leaf_prev_nd->set_right_sibling(leaf_act_nd->get_block());

				delete leaf_prev_nd;
				leaf_prev_nd = NULL;
			}
			endBlock = leaf_act_nd->get_block();
		}
		leaf_act_nd->add_new_child(id, key); // add new entry

		if (leaf_act_nd->isFull())
		{ // change next node to store entries
			leaf_prev_nd = leaf_act_nd;
			leaf_act_nd = NULL;
		}
	}
	if (leaf_prev_nd != NULL)
	{
		delete leaf_prev_nd;
		leaf_prev_nd = NULL;
	}
	if (leaf_act_nd != NULL)
	{
		delete leaf_act_nd;
		leaf_act_nd = NULL;
	}

	// -------------------------------------------------------------------------
	//  stop condition: lastEndBlock == lastStartBlock (only one node, as root)
	// -------------------------------------------------------------------------
	int current_level = 1;			 // current level (leaf level is 0)
	int lastStartBlock = startBlock; // build b-tree level by level
	int lastEndBlock = endBlock;	 // build b-tree level by level

	while (lastEndBlock > lastStartBlock)
	{
		firstNode = true;
		for (int i = lastStartBlock; i <= lastEndBlock; ++i)
		{
			block = i; // get <block>
			if (current_level == 1)
			{
				leaf_child = new BLeafNode();
				leaf_child->init_restore(this, block);
				key = leaf_child->get_key_of_node();

				delete leaf_child;
				leaf_child = NULL;
			}
			else
			{
				index_child = new BIndexNode();
				index_child->init_restore(this, block);
				key = index_child->get_key_of_node();

				delete index_child;
				index_child = NULL;
			}

			if (!index_act_nd)
			{
				index_act_nd = new BIndexNode();
				index_act_nd->init(current_level, this);

				if (firstNode)
				{
					firstNode = false;
					startBlock = index_act_nd->get_block();
				}
				else
				{
					index_act_nd->set_left_sibling(index_prev_nd->get_block());
					index_prev_nd->set_right_sibling(index_act_nd->get_block());

					delete index_prev_nd;
					index_prev_nd = NULL;
				}
				endBlock = index_act_nd->get_block();
			}
			index_act_nd->add_new_child(key, block); // add new entry

			if (index_act_nd->isFull())
			{
				index_prev_nd = index_act_nd;
				index_act_nd = NULL;
			}
		}
		if (index_prev_nd != NULL)
		{ // release the space
			delete index_prev_nd;
			index_prev_nd = NULL;
		}
		if (index_act_nd != NULL)
		{
			delete index_act_nd;
			index_act_nd = NULL;
		}

		lastStartBlock = startBlock; // update info
		lastEndBlock = endBlock;	 // build b-tree of higher level
		++current_level;
	}
	root_ = lastStartBlock; // update the <root>

	if (index_prev_nd != NULL)
		delete index_prev_nd;
	if (index_act_nd != NULL)
		delete index_act_nd;
	if (index_child != NULL)
		delete index_child;
	if (leaf_prev_nd != NULL)
		delete leaf_prev_nd;
	if (leaf_act_nd != NULL)
		delete leaf_act_nd;
	if (leaf_child != NULL)
		delete leaf_child;

	return 0;
}

int BTree::parallelBulkLoad(
	int n,				 // number of entries
	const Result *table, // hash table
	int maxThreadNum,	 // max thread num
	int maxBufferBlock	 // max number of blocks in buffer
)
{
    SharedMemory* unWrittenBlock = new SharedMemory();
	pthread_mutex_t fileLock;
	pthread_mutex_init(&fileLock, NULL);
	
    // single consumer thread
    pthread_t t;
    pthread_create(&t, NULL, &loadBlockToDisk, unWrittenBlock);

	int threadNum = maxThreadNum;

	int id = -1;
	int block = -1;
	float key = MINREAL;
	/*
		get Index node and Leaf node's capacity
	*/
	int BlockLength = this->file_->get_blocklength();
	int BIndexNodeCap = (BlockLength - (SIZECHAR + SIZEINT * 3)) / (SIZEFLOAT + SIZEINT);
	int BLeafNodeCap = (BlockLength - (SIZECHAR + SIZEINT * 3) - (int)ceil((float)BlockLength / LEAF_NODE_SIZE) * SIZEFLOAT - SIZEINT) / SIZEINT;

	// calculate the blocks number that the leaves need
	int LeafBlockNum = (int)ceil((double)n / BLeafNodeCap);
	//std::cout << "Leaf layer needs " << LeafBlockNum << "blocks\n";

	// pre-allocate blocks for the Leaf layer
	int *LeafBlockIndex = alloc_blocks(LeafBlockNum);
	int c = 0;

	// -------------------------------------------------------------------------
	//  build leaf node from <_hashtable> (level = 0)
	// -------------------------------------------------------------------------
	bool firstNode = true; // determine relationship of sibling
	int startBlock = 0;	   // position of first node
	int endBlock = 0;	   // position of last node

	// caluculate batch load variable
	int batchBlockSize = LeafBlockNum / threadNum;								  // blocks number for each batch load
	int lastBatchBlockSize = LeafBlockNum - (threadNum - 1) * batchBlockSize;	  // blocks number for the last batch load(can be 0)
	int batchEntrySize = batchBlockSize * BLeafNodeCap;							  // entries number for each batch load
	int lastBatchEntrySize = n - batchBlockSize * BLeafNodeCap * (threadNum - 1); // entries number for the last batch load(can be 0)
	int MAX_BLOCK = maxBufferBlock;
	int MIN_BLOCK = maxBufferBlock > 30 ? 10 : maxBufferBlock / 2;

	// define thread and arguments for each thread
	pthread_t tid[threadNum + 5];
	BatchLoadLeafArgs BLLA[threadNum + 5];
	BatchLoadIndexArgs BLIA[threadNum + 5];
	// assign thread arguments
	for (int i = 0; i < threadNum; i++)
	{
		BLLA[i].hashTable = table + i * batchEntrySize;						  // hash table that store data entries
		BLLA[i].entryNum = batchEntrySize;									  // the number of entries that the function needs to load
		BLLA[i].blockIndex = LeafBlockIndex;								  // the index of block that allocated for these entries
		BLLA[i].blockIndexLen = LeafBlockNum;								  // the length of array blockIndex
		BLLA[i].blockIndexStart = 0 + i * batchBlockSize;					  // the start index of array blockIndex
		BLLA[i].blockIndexEnd = BLLA[i].blockIndexStart + batchBlockSize - 1; // the end index of array blockIndex
		BLLA[i].maxBlock = MAX_BLOCK;										  // the maxium number of block in memory that the function can allocate
		BLLA[i].minBlock = MIN_BLOCK;
		BLLA[i].bTree = this;
		BLLA[i].fileLock = &fileLock; // prevent multi-thread access file
		BLLA[i].sharedMemory = unWrittenBlock;
	}
	BLLA[threadNum - 1].entryNum = lastBatchEntrySize;												  // the number of entries that the function needs to load
	BLLA[threadNum - 1].blockIndexEnd = BLLA[threadNum - 1].blockIndexStart + lastBatchBlockSize - 1; // the end index of array blockIndex

	float *leafBlockKey = (float *)malloc(SIZEFLOAT * LeafBlockNum);
	int keyCount = 0;
	float *batchKey = NULL;

	for (int i = 0; i < threadNum; ++i)
	{
		if (BLLA[i].entryNum > 0)
		{
			pthread_create(&tid[i], NULL, batchLoadLeaf, &(BLLA[i]));
		}
	}
	for (int i = 0; i < threadNum; i++)
	{
		if (BLLA[i].entryNum > 0)
		{
			pthread_join(tid[i], (void **)&batchKey);
			for (int j = 0; j <= (BLLA[i].blockIndexEnd - BLLA[i].blockIndexStart); j++)
			{
				leafBlockKey[keyCount++] = batchKey[j];
			}
			free(batchKey);
		}
	}
	
	startBlock = LeafBlockIndex[0];
	endBlock = LeafBlockIndex[LeafBlockNum - 1];

	// -------------------------------------------------------------------------
	// build index node from bottom to top
	// stop condition: lastEndBlock == lastStartBlock (only one node, as root)
	// -------------------------------------------------------------------------
	int current_level = 1;			 // current level (leaf level is 0)
	int lastStartBlock = startBlock; // build b-tree level by level
	int lastEndBlock = endBlock;	 // build b-tree level by level
	float *lastLayerKey = leafBlockKey;
	float *currentLayerKey = NULL;
	int *lastLayerBlockIndex = LeafBlockIndex;
	int lastLayerBlockNum = LeafBlockNum;
	int *currentLayerBlockIndex = NULL;
	int currentLayerBlockNum;
	//std::cout << lastEndBlock - lastStartBlock << '\n';
	
	while (lastEndBlock > lastStartBlock)
	{
		
		currentLayerBlockNum = (int)ceil((double)lastLayerBlockNum / BIndexNodeCap);
		currentLayerBlockIndex = alloc_blocks(currentLayerBlockNum);
		batchBlockSize = currentLayerBlockNum / threadNum;										   //blocks number for each batch load
		lastBatchBlockSize = currentLayerBlockNum - (threadNum - 1) * batchBlockSize;			   //blocks number for the last batch load(can be 0)
		batchEntrySize = batchBlockSize * BIndexNodeCap;										   //entries number for each batch load
		lastBatchEntrySize = lastLayerBlockNum - batchBlockSize * BIndexNodeCap * (threadNum - 1); //entries number for the last batch load(can be 0)
		for (int i = 0; i < threadNum; i++)
		{
			BLIA[i].sonBlockTable = lastLayerBlockIndex + i * batchEntrySize;	  // hash table that store entries
			BLIA[i].sonKeyTable = lastLayerKey + i * batchEntrySize;			  // table that store sons' key index
			BLIA[i].son_num = batchEntrySize;									  // the number of entries that the function needs to load
			BLIA[i].currentLevel = current_level;								  //layers level
			BLIA[i].blockIndex = currentLayerBlockIndex;						  // the index of block that allocated for these entries
			BLIA[i].blockIndexLen = currentLayerBlockNum;						  // the length of array blockIndex
			BLIA[i].blockIndexStart = 0 + i * batchBlockSize;					  // the start index of array blockIndex
			BLIA[i].blockIndexEnd = BLIA[i].blockIndexStart + batchBlockSize - 1; // the end index of array blockIndex
			BLIA[i].maxBlock = MAX_BLOCK;										  // the maxium number of block in memory that the function can allocate
			BLIA[i].minBlock = MIN_BLOCK;										  // I don't want some thread write out one node for an I/O
			BLIA[i].bTree = this;												  // the btree that these nodes should belongs to
			BLIA[i].fileLock = &fileLock;	
			BLIA[i].sharedMemory = unWrittenBlock;									  // prevent multi-thread access file
		}
		BLIA[threadNum - 1].son_num = lastBatchEntrySize;												  // the number of entries that the function needs to load
		BLIA[threadNum - 1].blockIndexEnd = BLIA[threadNum - 1].blockIndexStart + lastBatchBlockSize - 1; // the end index of array blockIndex
		
		// std::cout << "Level " << current_level << ": Arguments loaded\n";
		// printf("%d %d\n", lastStartBlock, lastEndBlock);
		
		for (int i = 0; i <= threadNum - 1; i++)
		{
			if (BLIA[i].son_num > 0)
			{
				pthread_create(&tid[i], NULL, batchLoadIndex, &(BLIA[i]));
			}
		}
		currentLayerKey = (float *)malloc(sizeof(float) * (currentLayerBlockNum));
		keyCount = 0;
		for (int i = 0; i <= threadNum - 1; i++)
		{
			if (BLIA[i].son_num > 0)
			{
				pthread_join(tid[i], (void **)&batchKey);
				for (int j = 0; j <= (BLIA[i].blockIndexEnd - BLIA[i].blockIndexStart); j++)
				{
					currentLayerKey[keyCount++] = batchKey[j];
				}
				free(batchKey);
			}
		}
		free(lastLayerBlockIndex);
		free(lastLayerKey);
		lastLayerBlockIndex = currentLayerBlockIndex;
		lastLayerKey = currentLayerKey;
		lastLayerBlockNum = currentLayerBlockNum;
		lastStartBlock = currentLayerBlockIndex[0];						 // update info
		lastEndBlock = currentLayerBlockIndex[currentLayerBlockNum - 1]; // build b-tree of higher level
		++current_level;
		currentLayerBlockIndex = NULL;
		currentLayerKey = NULL;

	}
	assert(lastStartBlock == lastEndBlock);
	root_ = lastStartBlock; // update the <root>
	
	unWrittenBlock->start = false;
    
    pthread_join(t, NULL);
    
   	// delete unWrittenBlock;

	return 0;
}
// -------------------------------------------------------------------------
/*
	customer thread work
*/
void *BTree::loadBlockToDisk(
	void *args){
    SharedMemory* sharedMemory = (SharedMemory *)args;
	while(true){
		sharedMemory->writeBlockToDisk();
		if(sharedMemory->start == false && sharedMemory->isEmpty()){
			break;
		}
	}
	return NULL;
}

// -------------------------------------------------------------------------
/*
	start routine of thread, this function wil put n entries into serveral
	blocks, every leaf node will be as full as possible
*/
void *BTree::batchLoadLeaf(
	void *args)
{
	// Load arguments
	BatchLoadLeafArgs *funcArgs = (BatchLoadLeafArgs *)args;
	const Result *hashTable = funcArgs->hashTable;
	int entryNum = funcArgs->entryNum;
	int *blockIndex = funcArgs->blockIndex;
	int blockIndexLen = funcArgs->blockIndexLen;
	int blockIndexStart = funcArgs->blockIndexStart;
	int blockIndexEnd = funcArgs->blockIndexEnd;
	int maxBlock = funcArgs->maxBlock;
	int minBlock = funcArgs->minBlock;
	BTree *bTree = funcArgs->bTree;
	pthread_mutex_t *fileLock = funcArgs->fileLock;
	SharedMemory* sharedMemory = funcArgs->sharedMemory;

	float *batchKey = (float *)malloc(sizeof(float) * (blockIndexEnd - blockIndexStart + 1)); //node key on the fly
	int keyCount = 0;

	int id;
	float key;
	BLeafNode *currentLeafNode = NULL;
	int currentBlockIndex = blockIndexStart;
	for (int i = 0; i <= entryNum - 1; i++)
	{
		assert(currentBlockIndex <= blockIndexEnd);
		id = hashTable[i].id_;
		key = hashTable[i].key_;
		if (currentLeafNode == NULL)
		{
			currentLeafNode = new BLeafNode();
			currentLeafNode->init_noalloc(0, bTree, blockIndex[currentBlockIndex]);
			if (currentBlockIndex - 1 >= 0)
			{ // has previous leaf node
				currentLeafNode->set_left_sibling(blockIndex[currentBlockIndex - 1]);
			}
			if (currentBlockIndex + 1 <= blockIndexLen - 1)
			{ // has next leaf node
				currentLeafNode->set_right_sibling(blockIndex[currentBlockIndex + 1]);
			}
		}
		currentLeafNode->add_new_child(id, key);
		if (currentLeafNode->isFull())
		{
			pthread_mutex_lock(fileLock);
			batchKey[keyCount++] = currentLeafNode->get_key_of_node();
			sharedMemory->addBlocksToMemory(currentLeafNode);
			pthread_mutex_unlock(fileLock);
			currentLeafNode = NULL;
			currentBlockIndex++;
		}
	}
	if (currentLeafNode != NULL)
	{
		pthread_mutex_lock(fileLock);
		batchKey[keyCount++] = currentLeafNode->get_key_of_node();
		sharedMemory->addBlocksToMemory(currentLeafNode);
		pthread_mutex_unlock(fileLock);	
	}
	assert(keyCount == blockIndexEnd - blockIndexStart + 1);
	return batchKey;
}

// -----------------------------------------------------------------------------
void *BTree::batchLoadIndex(void *args)
{
	BatchLoadIndexArgs *funcArgs = (BatchLoadIndexArgs *)args;
	int *sonBlockTable = funcArgs->sonBlockTable;	 // table that store sons' block index
	float *sonKeyTable = funcArgs->sonKeyTable;		 // table that store sons' key index
	int son_num = funcArgs->son_num;				 // the number of entries that the function needs to load
	int *blockIndex = funcArgs->blockIndex;			 // the index of block that allocated for these entries
	int currentLevel = funcArgs->currentLevel;		 // layers level
	int blockIndexLen = funcArgs->blockIndexLen;	 // the length of array blockIndex
	int blockIndexStart = funcArgs->blockIndexStart; // the start index of array blockIndex
	int blockIndexEnd = funcArgs->blockIndexEnd;	 // the end index of array blockIndex
	int maxBlock = funcArgs->maxBlock;				 // the maxium number of block in memory that the function can allocate
	int minBlock = funcArgs->minBlock;				 // I don't want some thread write out one node for an I/O
	BTree *bTree = funcArgs->bTree;					 // the btree that these nodes should belongs to
	pthread_mutex_t *fileLock = funcArgs->fileLock;	 // prevent multi-thread access file
	SharedMemory* sharedMemory = funcArgs->sharedMemory;

	int block;
	float key;
	BIndexNode *currentIndexNode = NULL;
	int currentBlockIndex = blockIndexStart;

	float *batchKey = (float *)malloc(sizeof(float) * (blockIndexEnd - blockIndexStart + 1)); //node key on the fly
	int keyCount = 0;

	for (int i = 0; i <= son_num - 1; i++)
	{
		block = sonBlockTable[i]; // get <block>
		key = sonKeyTable[i];
		//std::cout << "load block : " << block << '\n';

		if (currentIndexNode == NULL)
		{
			currentIndexNode = new BIndexNode();
			currentIndexNode->init_noalloc(currentLevel, bTree, blockIndex[currentBlockIndex]);
			if (currentBlockIndex - 1 >= 0)
			{
				currentIndexNode->set_left_sibling(blockIndex[currentBlockIndex - 1]);
			}
			if (currentBlockIndex + 1 <= blockIndexLen - 1)
			{
				currentIndexNode->set_right_sibling(blockIndex[currentBlockIndex + 1]);
			}
		}
		currentIndexNode->add_new_child(key, block);
		
		if (currentIndexNode->isFull())
		{
			pthread_mutex_lock(fileLock);
			batchKey[keyCount++] = currentIndexNode->get_key_of_node();
			sharedMemory->addBlocksToMemory(currentIndexNode);
			pthread_mutex_unlock(fileLock);	

			currentIndexNode = NULL;
			currentBlockIndex++;
		}
	}
	if (currentIndexNode != NULL)
	{
		pthread_mutex_lock(fileLock);
		batchKey[keyCount++] = currentIndexNode->get_key_of_node();
		sharedMemory->addBlocksToMemory(currentIndexNode);
		pthread_mutex_unlock(fileLock);	
	}

	assert(keyCount == blockIndexEnd - blockIndexStart + 1);
	
	// std::cout<<keyCount<<std::endl;
	return batchKey;
}

// -----------------------------------------------------------------------------
void BTree::load_root() // load root of b-tree
{
	if (root_ptr_ == NULL)
	{
		root_ptr_ = new BIndexNode();
		root_ptr_->init_restore(this, root_);
	}
}

// -----------------------------------------------------------------------------
void BTree::delete_root() // delete root of b-tree
{
	if (root_ptr_ != NULL)
	{
		delete root_ptr_;
		root_ptr_ = NULL;
	}
}

//------------------------------------------------------------------------------
int *BTree::alloc_blocks( // allocate n empty blocks in the block file
	int n)
{
	char *randomBlk = (char *)malloc(sizeof(char) * (this->file_->get_blocklength()) * n); // a useless block, just to fill the file
	int *blockIndexs = this->file_->append_blocks(randomBlk, n);
	return blockIndexs;
} // returns an array of indexs of blocks that were allocated
 
