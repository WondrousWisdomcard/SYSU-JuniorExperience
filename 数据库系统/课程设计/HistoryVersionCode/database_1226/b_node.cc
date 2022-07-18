#include "b_node.h"

// -----------------------------------------------------------------------------
//  BNode: basic structure of node in b-tree
// -----------------------------------------------------------------------------
BNode::BNode() // constructor
{
	level_ = -1;
	num_entries_ = -1;
	left_sibling_ = -1;
	right_sibling_ = -1;
	key_ = NULL;
	block_ = -1;
	capacity_ = -1;
	dirty_ = false;
	btree_ = NULL;
}

// -----------------------------------------------------------------------------
BNode::~BNode() // destructor
{
	key_ = NULL;
	btree_ = NULL;
}

// -----------------------------------------------------------------------------
void BNode::init( // init a new node, which not exist
	int level,	  // level (depth) in b-tree
	BTree *btree) // b-tree of this node
{
	btree_ = btree;
	level_ = (char)level;
	dirty_ = true;
	left_sibling_ = -1;
	right_sibling_ = -1;
	key_ = NULL;
	num_entries_ = 0;
	block_ = -1;
	capacity_ = -1;
}

// -----------------------------------------------------------------------------
void BNode::init_restore( // load an exist node from disk to init
	BTree *btree,		  // b-tree of this node
	int block)			  // addr of disk for this node
{
	btree_ = btree;
	block_ = block;
	dirty_ = false;
	left_sibling_ = -1;
	right_sibling_ = -1;
	key_ = NULL;
	num_entries_ = 0;
	level_ = -1;
	capacity_ = -1;
}

//------------------------------------------------------------------------------
void BNode::init_noalloc( // init a new node in menmory without allocating a block
	int level,			  // level in b-tree
	BTree *btree,		  // b-tree of this node
	int block			  // the index of the block that pre-allocated for this node
)
{
	btree_ = btree;
	level_ = (char)level;
	dirty_ = true;
	left_sibling_ = -1;
	right_sibling_ = -1;
	key_ = NULL;
	num_entries_ = 0;
	block_ = block;
	capacity_ = -1;
}

// -----------------------------------------------------------------------------
BNode *BNode::get_left_sibling() // get the left-sibling node
{
	BNode *node = NULL;
	if (left_sibling_ != -1)
	{						// left sibling node exist
		node = new BNode(); // read left-sibling from disk
		node->init_restore(btree_, left_sibling_);
	}
	return node;
}

// -----------------------------------------------------------------------------
BNode *BNode::get_right_sibling() // get the right-sibling node
{
	BNode *node = NULL;
	if (right_sibling_ != -1)
	{						// right sibling node exist
		node = new BNode(); // read right-sibling from disk
		node->init_restore(btree_, right_sibling_);
	}
	return node;
}

// -----------------------------------------------------------------------------
//  BIndexNode: structure of index node for b-tree
// -----------------------------------------------------------------------------
BIndexNode::BIndexNode() // constructor
{
	level_ = -1;
	num_entries_ = -1;
	left_sibling_ = -1;
	right_sibling_ = -1;
	block_ = -1;
	capacity_ = -1;
	dirty_ = false;
	btree_ = NULL;
	key_ = NULL;
	son_ = NULL;
}

// -----------------------------------------------------------------------------
BIndexNode::~BIndexNode() // destructor
{
	if (dirty_)
	{ // if dirty, rewrite to disk
		int block_length = btree_->file_->get_blocklength();
		char *buf = new char[block_length];
		write_to_buffer(buf);
		btree_->file_->write_block(buf, block_);

		delete[] buf;
		buf = NULL;
	}

	if (key_ != NULL)
	{
		delete[] key_;
		key_ = NULL;
	}
	if (son_ != NULL)
	{
		delete[] son_;
		son_ = NULL;
	}
}

// -----------------------------------------------------------------------------
void BIndexNode::init( // init a new node, which not exist
	int level,		   // level (depth) in b-tree
	BTree *btree)	   // b-tree of this node
{
	btree_ = btree;
	level_ = (char)level;
	num_entries_ = 0;
	left_sibling_ = -1;
	right_sibling_ = -1;
	dirty_ = true;

	//page size B
	int b_length = btree_->file_->get_blocklength();
	capacity_ = (b_length - get_header_size()) / get_entry_size();
	if (capacity_ < 50)
	{ // ensure at least 50 entries
		printf("capacity = %d, which is too small.\n", capacity_);
		exit(1);
	}

	key_ = new float[capacity_];
	son_ = new int[capacity_];
	//分配内存
	memset(key_, MINREAL, capacity_ * SIZEFLOAT);
	memset(son_, -1, capacity_ * SIZEINT);

	char *blk = new char[b_length]; // init <block_>, get new addr
	block_ = btree_->file_->append_block(blk);
	delete[] blk;
	blk = NULL;
}

// -----------------------------------------------------------------------------
void BIndexNode::init_restore( // load an exist node from disk to init
	BTree *btree,			   // b-tree of this node
	int block)				   // addr of disk for this node
{
	btree_ = btree;
	block_ = block;
	dirty_ = false;

	int b_len = btree_->file_->get_blocklength();
	capacity_ = (b_len - get_header_size()) / get_entry_size();
	if (capacity_ < 50)
	{ // at least 50 entries
		printf("capacity = %d, which is too small.\n", capacity_);
		exit(1);
	}

	key_ = new float[capacity_];
	son_ = new int[capacity_];
	memset(key_, MINREAL, capacity_ * SIZEFLOAT);
	memset(son_, -1, capacity_ * SIZEINT);

	// -------------------------------------------------------------------------
	//  read the buffer <blk> to init <level_>, <num_entries_>, <left_sibling_>,
	//  <right_sibling_>, <key_> and <son_>.
	// -------------------------------------------------------------------------
	char *blk = new char[b_len];
	btree_->file_->read_block(blk, block);
	read_from_buffer(blk);

	delete[] blk;
	blk = NULL;
}

//------------------------------------------------------------------------------
void BIndexNode::init_noalloc( // init a new node in menmory without allocating a block
	int level,				   // level in b-tree
	BTree *btree,			   // b-tree of this node
	int block				   // the index of the block that pre-allocated for this node
)
{
	btree_ = btree;
	level_ = (char)level;
	block_ = block;
	num_entries_ = 0;
	left_sibling_ = -1;
	right_sibling_ = -1;
	dirty_ = true;

	//page size B
	int b_length = btree_->file_->get_blocklength();
	capacity_ = (b_length - get_header_size()) / get_entry_size();
	if (capacity_ < 50)
	{ // ensure at least 50 entries
		printf("capacity = %d, which is too small.\n", capacity_);
		exit(1);
	}

	key_ = new float[capacity_];
	son_ = new int[capacity_];
	//分配内存
	memset(key_, MINREAL, capacity_ * SIZEFLOAT);
	memset(son_, -1, capacity_ * SIZEINT);

	// whithout allocating block in the file
}

// -----------------------------------------------------------------------------
//  Read info from buffer to initialize <level_>, <num_entries_>,
//  <left_sibling_>, <right_sibling_>, <key_> and <son_> of b-index node
// -----------------------------------------------------------------------------
void BIndexNode::read_from_buffer( // read a b-node from buffer
	const char *buf)			   // store info of a b-index node
{
	int i = 0;
	memcpy(&level_, &buf[i], SIZECHAR);
	i += SIZECHAR;
	memcpy(&num_entries_, &buf[i], SIZEINT);
	i += SIZEINT;
	memcpy(&left_sibling_, &buf[i], SIZEINT);
	i += SIZEINT;
	memcpy(&right_sibling_, &buf[i], SIZEINT);
	i += SIZEINT;

	for (int j = 0; j < num_entries_; ++j)
	{
		memcpy(&key_[j], &buf[i], SIZEFLOAT);
		i += SIZEFLOAT;
		memcpy(&son_[j], &buf[i], SIZEINT);
		i += SIZEINT;
	}
}

// -----------------------------------------------------------------------------
void BIndexNode::write_to_buffer( // write info of node into buffer
	char *buf)					  // store info of this node (return)
{
	int i = 0;
	memcpy(&buf[i], &level_, SIZECHAR);
	i += SIZECHAR;
	memcpy(&buf[i], &num_entries_, SIZEINT);
	i += SIZEINT;
	memcpy(&buf[i], &left_sibling_, SIZEINT);
	i += SIZEINT;
	memcpy(&buf[i], &right_sibling_, SIZEINT);
	i += SIZEINT;

	for (int j = 0; j < num_entries_; ++j)
	{
		memcpy(&buf[i], &key_[j], SIZEFLOAT);
		i += SIZEFLOAT;
		memcpy(&buf[i], &son_[j], SIZEINT);
		i += SIZEINT;
	}
}

// -----------------------------------------------------------------------------
//  find position of entry that is just less than or equal to input entry.
//  if input entry is smaller than all entry in this node, we'll return -1.
//  the scan order is from right to left.
// -----------------------------------------------------------------------------
int BIndexNode::find_position_by_key(
	float key) // input key
{
	int pos = -1;
	for (int i = num_entries_ - 1; i >= 0; --i)
	{
		if (key_[i] <= key)
		{
			pos = i;
			break;
		}
	}
	return pos;
}

// -----------------------------------------------------------------------------
//  get the left-sibling node
// -----------------------------------------------------------------------------
BIndexNode *BIndexNode::get_left_sibling()
{
	BIndexNode *node = NULL;
	if (left_sibling_ != -1)
	{							 // left sibling node exist
		node = new BIndexNode(); // read left-sibling from disk
		node->init_restore(btree_, left_sibling_);
	}
	return node;
}

// -----------------------------------------------------------------------------
//  get the right-sibling node
// -----------------------------------------------------------------------------
BIndexNode *BIndexNode::get_right_sibling()
{
	BIndexNode *node = NULL;
	if (right_sibling_ != -1)
	{							 // right sibling node exist
		node = new BIndexNode(); // read right-sibling from disk
		node->init_restore(btree_, right_sibling_);
	}
	return node;
}

// -----------------------------------------------------------------------------
void BIndexNode::add_new_child( // add a new entry from its child node
	float key,					// input key
	int son)					// input son
{
	// assert(num_entries_ >= 0 && num_entries_ < capacity_);
	key_[num_entries_] = key; // add new entry into its pos
	son_[num_entries_] = son;

	++num_entries_; // update <num_entries_>
	dirty_ = true;	// node modified, <dirty_> is true
}

// -----------------------------------------------------------------------------
//  BLeafNode: structure of leaf node in b-tree
// -----------------------------------------------------------------------------
BLeafNode::BLeafNode() // constructor
{
	level_ = -1;
	num_entries_ = -1;
	left_sibling_ = -1;
	right_sibling_ = -1;
	block_ = -1;
	capacity_ = -1;
	dirty_ = false;
	btree_ = NULL;
	num_keys_ = -1;
	capacity_keys_ = -1;
	key_ = NULL;
	id_ = NULL;
}

// -----------------------------------------------------------------------------
BLeafNode::~BLeafNode() // destructor
{
	if (dirty_)
	{ // if dirty, rewrite to disk
		int block_length = btree_->file_->get_blocklength();
		char *buf = new char[block_length];
		write_to_buffer(buf);
		btree_->file_->write_block(buf, block_);

		delete[] buf;
		buf = NULL;
	}

	if (key_ != NULL)
	{
		delete[] key_;
		key_ = NULL;
	}
	if (id_ != NULL)
	{
		delete[] id_;
		id_ = NULL;
	}
}

// -----------------------------------------------------------------------------
void BLeafNode::init( // init a new node, which not exist
	int level,		  // level (depth) in b-tree
	BTree *btree)	  // b-tree of this node
{
	btree_ = btree;
	level_ = (char)level;

	num_entries_ = 0;
	num_keys_ = 0;
	left_sibling_ = -1;
	right_sibling_ = -1;
	dirty_ = true;

	// -------------------------------------------------------------------------
	//  init <capacity_keys_> and calc key size
	// -------------------------------------------------------------------------
	//page size B
	int b_length = btree_->file_->get_blocklength();
	int key_size = get_key_size(b_length);

	key_ = new float[capacity_keys_];
	memset(key_, MINREAL, capacity_keys_ * SIZEFLOAT);

	int header_size = get_header_size();
	int entry_size = get_entry_size();

	capacity_ = (b_length - header_size - key_size) / entry_size;
	if (capacity_ < 100)
	{ // at least 100 entries
		printf("capacity = %d, which is too small.\n", capacity_);
		exit(1);
	}
	id_ = new int[capacity_];
	memset(id_, -1, capacity_ * SIZEINT);

	char *blk = new char[b_length];
	block_ = btree_->file_->append_block(blk);
	delete[] blk;
	blk = NULL;
}

// -----------------------------------------------------------------------------
void BLeafNode::init_restore( // load an exist node from disk to init
	BTree *btree,			  // b-tree of this node
	int block)				  // addr of disk for this node
{
	btree_ = btree;
	block_ = block;
	dirty_ = false;

	// -------------------------------------------------------------------------
	//  init <capacity_keys> and calc key size
	// -------------------------------------------------------------------------
	int b_length = btree_->file_->get_blocklength();
	int key_size = get_key_size(b_length);

	key_ = new float[capacity_keys_];
	memset(key_, MINREAL, capacity_keys_ * SIZEFLOAT);

	int header_size = get_header_size();
	int entry_size = get_entry_size();

	capacity_ = (b_length - header_size - key_size) / entry_size;
	if (capacity_ < 100)
	{ // at least 100 entries
		printf("capacity = %d, which is too small.\n", capacity_);
		exit(1);
	}
	id_ = new int[capacity_];
	memset(id_, -1, capacity_ * SIZEINT);

	// -------------------------------------------------------------------------
	//  read the buffer <blk> to init <level_>, <num_entries_>, <left_sibling_>,
	//  <right_sibling_>, <num_keys_> <key_> and <id_>
	// -------------------------------------------------------------------------
	char *blk = new char[b_length];
	btree_->file_->read_block(blk, block);
	read_from_buffer(blk);

	delete[] blk;
	blk = NULL;
}

//------------------------------------------------------------------------------
void BLeafNode::init_noalloc( //init a new node in menmory without allocating a block
	int level,				  // level in b-tree
	BTree *btree,			  // b-tree of this node
	int block				  // the index of the block that pre-allocated for this node
)
{
	btree_ = btree;
	level_ = (char)level;
	block_ = block;
	num_entries_ = 0;
	num_keys_ = 0;
	left_sibling_ = -1;
	right_sibling_ = -1;
	dirty_ = true;

	// -------------------------------------------------------------------------
	//  init <capacity_keys_> and calc key size
	// -------------------------------------------------------------------------
	//page size B
	int b_length = btree_->file_->get_blocklength();
	int key_size = get_key_size(b_length);

	key_ = new float[capacity_keys_];
	memset(key_, MINREAL, capacity_keys_ * SIZEFLOAT);

	int header_size = get_header_size();
	int entry_size = get_entry_size();

	capacity_ = (b_length - header_size - key_size) / entry_size;
	if (capacity_ < 100)
	{ // at least 100 entries
		printf("capacity = %d, which is too small.\n", capacity_);
		exit(1);
	}
	id_ = new int[capacity_];
	memset(id_, -1, capacity_ * SIZEINT);
	// whithout allocating block in the file
}
// -----------------------------------------------------------------------------
void BLeafNode::read_from_buffer( // read a b-node from buffer
	const char *buf)			  // store info of a b-node
{
	int i = 0;
	// -------------------------------------------------------------------------
	//  read header: <level_> <num_entries_> <left_sibling_> <right_sibling_>
	// -------------------------------------------------------------------------
	memcpy(&level_, &buf[i], SIZECHAR);
	i += SIZECHAR;
	memcpy(&num_entries_, &buf[i], SIZEINT);
	i += SIZEINT;
	memcpy(&left_sibling_, &buf[i], SIZEINT);
	i += SIZEINT;
	memcpy(&right_sibling_, &buf[i], SIZEINT);
	i += SIZEINT;

	// -------------------------------------------------------------------------
	//  read keys: <num_keys_> and <key_> and entries: <id_>
	// -------------------------------------------------------------------------
	memcpy(&num_keys_, &buf[i], SIZEINT);
	i += SIZEINT;
	for (int j = 0; j < capacity_keys_; ++j)
	{
		memcpy(&key_[j], &buf[i], SIZEFLOAT);
		i += SIZEFLOAT;
	}
	for (int j = 0; j < num_entries_; ++j)
	{
		memcpy(&id_[j], &buf[i], SIZEINT);
		i += SIZEINT;
	}
}

// -----------------------------------------------------------------------------
void BLeafNode::write_to_buffer( // write a b-node into buffer
	char *buf)					 // store info of a b-node (return)
{
	int i = 0;
	// -------------------------------------------------------------------------
	//  write header: <level_> <num_entries_> <left_sibling_> <right_sibling_>
	// -------------------------------------------------------------------------
	memcpy(&buf[i], &level_, SIZECHAR);
	i += SIZECHAR;
	memcpy(&buf[i], &num_entries_, SIZEINT);
	i += SIZEINT;
	memcpy(&buf[i], &left_sibling_, SIZEINT);
	i += SIZEINT;
	memcpy(&buf[i], &right_sibling_, SIZEINT);
	i += SIZEINT;

	// -------------------------------------------------------------------------
	//  write keys: <num_keys_> and <key_> and entries: <id_>
	// -------------------------------------------------------------------------
	memcpy(&buf[i], &num_keys_, SIZEINT);
	i += SIZEINT;
	for (int j = 0; j < capacity_keys_; ++j)
	{
		memcpy(&buf[i], &key_[j], SIZEFLOAT);
		i += SIZEFLOAT;
	}
	for (int j = 0; j < num_entries_; ++j)
	{
		memcpy(&buf[i], &id_[j], SIZEINT);
		i += SIZEINT;
	}
}

// -----------------------------------------------------------------------------
int BLeafNode::find_position_by_key( // find pos just less than input key
	float key)						 // input key
{
	int pos = -1;
	for (int i = num_keys_ - 1; i >= 0; --i)
	{
		if (key_[i] <= key)
		{
			pos = i; // position of corresponding id
			break;
		}
	}
	return pos;
}

// -----------------------------------------------------------------------------
BLeafNode *BLeafNode::get_left_sibling() // get left-sibling node
{
	BLeafNode *node = NULL;
	if (left_sibling_ != -1)
	{							// left sibling node exist
		node = new BLeafNode(); // read left-sibling from disk
		node->init_restore(btree_, left_sibling_);
	}
	return node;
}

// -----------------------------------------------------------------------------
BLeafNode *BLeafNode::get_right_sibling() // get right sibling node
{
	BLeafNode *node = NULL;
	if (right_sibling_ != -1)
	{							// right sibling node exist
		node = new BLeafNode(); // read right-sibling from disk
		node->init_restore(btree_, right_sibling_);
	}
	return node;
}

// -----------------------------------------------------------------------------
void BLeafNode::add_new_child( // add new child by input id and key
	int id,					   // input object id
	float key)				   // input key
{
	// assert(num_entries_ < capacity_);

	id_[num_entries_] = id; // add new id into its pos
	if ((num_entries_ * SIZEINT) % LEAF_NODE_SIZE == 0)
	{
		assert(num_keys_ < capacity_keys_);
		key_[num_keys_] = key; // add new key into its pos
		++num_keys_;		   // update <num_keys>
	}
	++num_entries_; // update <num_entries>
	dirty_ = true;	// node modified, <dirty> is true
}
