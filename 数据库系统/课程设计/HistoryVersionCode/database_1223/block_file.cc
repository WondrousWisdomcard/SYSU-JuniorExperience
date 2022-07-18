#include "block_file.h"

// -----------------------------------------------------------------------------
//  some points to NOTE:
//  1) 2 types of block # are used (i.e. the internal # (e.g. act_block) 
//     and external # (e.g. pos)). internal # is one larger than external #
//     because the first block of the file is used to store header info. 
//     data info is stored starting from the 2nd block (excluding the header
//     block).both types of # start from 0.
//
//  2) "act_block" is internal block #. "number" is the # of data block (i.e. 
//     excluding the header block). maximum actblock equals to number. Maximum 
//     external block # equals to number - 1 
//
//  3) cache_cont records the internal numbers. 
// -----------------------------------------------------------------------------
BlockFile::BlockFile(				// constructor
	int   b_length,						// block length
	const char *name)					// file name
{
	strcpy(fname_, name);
	//page size B
	block_length_ = b_length;

	num_blocks_ = 0;				// num of blocks, init to 0
	// -------------------------------------------------------------------------
	//  init <fp> and open <file_name_>. if <file_name_> exists, then fp != 0,
	//  and we excute if-clause program. otherwise, we excute else-clause 
	//  program.
	//
	//  "rb+": read or write data from or into binary doc. if the file not 
	//  exist, it will return NULL.
	// -------------------------------------------------------------------------
	if ((fp_ = fopen(fname_, "rb+")) != 0) {
		// ---------------------------------------------------------------------
		//  init <new_flag_> (since the file exists, <new_flag_> is false).
		//  reinit <block_length_> (determined by the doc itself).
		//  reinit <num_blocks_> (number of blocks in doc itself).
		// ---------------------------------------------------------------------
		new_flag_ = false;			// reinit <block_length_> by file
		block_length_ = fread_number();
		num_blocks_ = fread_number();
	}
	else {
		// ---------------------------------------------------------------------
		//  init <new_flag_>: as file is just constructed (new), it is true.
		//  write <block_length_> and <num_blocks_> to the header of file.
		//  since the file is empty (new), <num_blocks_> is 0 (no blocks in it)
		//
		//  "wb+": read or write data from or into binary doc. if file not
		//  exist, we will construct a new file.
		// ---------------------------------------------------------------------
		assert(block_length_ >= BFHEAD_LENGTH);

		fp_ = fopen(fname_, "wb+");
		new_flag_ = true;
		fwrite_number(block_length_);
		fwrite_number(0);

		// ---------------------------------------------------------------------
		//  since <block_length_> >= 8 bytes, for the remain bytes, we will 
		//  init 0 to them.
		//
		//  ftell() return number of bytes from current position to the 
		//  beginning position of the file.
		// ---------------------------------------------------------------------
		int  length = block_length_ - (int) ftell(fp_);
		char *buffer = new char[length];

		memset(buffer, 0, sizeof(buffer));
		put_bytes(buffer, length);

		delete[] buffer; buffer = NULL;
	}
	// -------------------------------------------------------------------------
	//  Redirect file pointer to the start position of the file
	// -------------------------------------------------------------------------
	fseek(fp_, 0, SEEK_SET);
	act_block_ = 0;					// init <act_block_> (no blocks)
}

// -----------------------------------------------------------------------------
BlockFile::~BlockFile()				// destructor
{
	if (fp_) fclose(fp_);
}

// -----------------------------------------------------------------------------
//  note that this func does not read the header of blockfile. it fetches the 
//  info in the first block excluding the header of blockfile.
// -----------------------------------------------------------------------------
void BlockFile::read_header(		// read remain bytes excluding header
	char *buffer)						// contain remain bytes (return)
{
	fseek(fp_, BFHEAD_LENGTH, SEEK_SET); // jump out of first 8 bytes
	get_bytes(buffer, block_length_ - BFHEAD_LENGTH); // read remaining bytes

	if (num_blocks_ < 1) {			// no remain bytes
		fseek(fp_, 0, SEEK_SET);	// fp return to beginning pos
		act_block_ = 0;				// no act block
	} 
	else {
		// ---------------------------------------------------------------------
		//  since we have read the first block (header block) of block file,
		//  thus <act_block_> = 1, and the file pointer point to the 2nd block
		//  (first block to store real data).
		// ---------------------------------------------------------------------
		act_block_ = 1;
	}
}

// -----------------------------------------------------------------------------
//  note that this func does not write the header of blockfile. it writes the 
//  info in the first block excluding the header of blockfile.
// -----------------------------------------------------------------------------
void BlockFile::set_header(			// set remain bytes excluding header
	const char *buffer)					// contain remain bytes
{
	fseek(fp_, BFHEAD_LENGTH, SEEK_SET); // jump out of first 8 bytes
	put_bytes(buffer, block_length_ - BFHEAD_LENGTH); // write remain bytes
	
	if (num_blocks_ < 1) {			// no remain bytes
		fseek(fp_, 0, SEEK_SET);	// fp return to beginning pos
		act_block_ = 0;				// no act block
	}
	else {
		// ---------------------------------------------------------------------
		//  since we have write the first block (header block) of block file,
		//  thus <act_block_> = 1, and the file pointer point to the 2nd block 
		//  (first block to store real data).
		// ---------------------------------------------------------------------
		act_block_ = 1;
	}
}

// -----------------------------------------------------------------------------
//  read a <block> from <index>
//
//  we point out the difference of counting among the <number>, <act_block> 
//  and <pos>.
//  (1) <num_blocks_>: record the number of blocks, excluding the block
//      of header. start from 1. (internal block)
//  (2) <act_block_>: record the number of blocks currently read or written,
//      including the block of header, thus when we read or write file,
//      current <act_block> equal to 1. <act_block> is corresponding to
//      file pointer.
//  (3) <index> : record position of block we want to read or write, excluding
//      the block of header. start from 0. (external block), i.e., when 
//      <index> = 0, the file pointer is pointed to next block after the 
//      block of header, at this time, <act_block_> equals to 1.
//
//  i.e. if number = 3, there are 4 blocks in the file, 1 header block +
//  3 data block.
//
//  when file is opened, <act_block_> = 1. if <index> = 1, it means that we 
//  want to read or write the 3rd block (2nd data block), thus firstly index++,
//  then <index> = 2, then fseek move to 2nd data block.
//
//  after reading or writing the 2nd data block, file pointer is pointed to 
//  the 3rd data block. As we know it has read or written 3 blocks, thus 
//  currently <act_block> = <index> + 1 = 2 + 1 = 3.
// -----------------------------------------------------------------------------
bool BlockFile::read_block(			// read a <block> from <index>
	Block block,						// a <block> (return)
	int index)							// pos of the block
{
	++index;						// extrnl block to intrnl block
	// assert(index > 0 && index <= num_blocks_);
	seek_block(index);

	get_bytes(block, block_length_);
	if (index + 1 > num_blocks_) {	// <fp_> reaches the end of file
		fseek(fp_, 0, SEEK_SET);
		act_block_ = 0;				// <act_block_> rewind to start pos
	}
	else {
		act_block_ = index + 1;		// <act_block_> to next pos
	}
	return true;
}

// -----------------------------------------------------------------------------
//  note that this function can ONLY write to an already "allocated" block (in 
//  the range of <num_blocks>).
//  if you allocate a new block, please use "append_block" instead.
// -----------------------------------------------------------------------------
bool BlockFile::write_block(		// write a <block> into <index>
	Block block,						// a <block>
	int index)							// position of the blocks
{
	++index;						// extrnl block to intrnl block
	// assert(index > 0 && index <= num_blocks_);
	seek_block(index);

	put_bytes(block, block_length_);// write this block
	if (index + 1 > num_blocks_) {	// update <act_block_>
		fseek(fp_, 0, SEEK_SET);
		act_block_ = 0;
	}
	else {
		act_block_ = index + 1;
	}
	return true;
}

// -----------------------------------------------------------------------------
//  append a new block at the end of file (out of the range of <num_blocks_>).
//  the file pointer is pointed to the new appended block and return its pos.
// -----------------------------------------------------------------------------
int BlockFile::append_block(		// append new block at the end of file
	Block block)						// the new block
{
	fseek(fp_, 0, SEEK_END);		// <fp_> point to the end of file
	put_bytes(block, block_length_);// write a <block>
	//fwrite(block, 1, block_length_, fp_);
	++num_blocks_;					// add 1 to <num_blocks_>
	
	fseek(fp_, SIZEINT, SEEK_SET);	// <fp_> point to pos of header
	fwrite_number(num_blocks_);		// update <num_blocks_>

	// -------------------------------------------------------------------------
	//  <fp_> point to the pos of new added block. 
	//  the equation <act_block_> = <num_blocks_> indicates the file pointer 
	//  point to new added block.
	//  return index of new added block
	// -------------------------------------------------------------------------
	fseek(fp_, -block_length_, SEEK_END);
	return (act_block_ = num_blocks_) - 1;
}

/*
	append a series of blocks(cont), I don't want to call fwrite too often
*/
// unfinished
int* BlockFile::append_blocks(		// append new block at the end of file
	Block block,					// the new blocks
	int n)							// the number of blocks
{
	fseek(fp_, 0, SEEK_END);		// <fp_> point to the end of file
	//put_bytes(block, block_length_);// write a <block>
	fwrite(block, n, block_length_, fp_);
	int start_block = num_blocks_ + 1 - 1;
	num_blocks_ += n;					// add 1 to <num_blocks_>
	int end_block = num_blocks_ - 1;
	
	fseek(fp_, SIZEINT, SEEK_SET);	// <fp_> point to pos of header
	fwrite_number(num_blocks_);		// update <num_blocks_>

	// -------------------------------------------------------------------------
	//  <fp_> point to the pos of new added block. 
	//  the equation <act_block_> = <num_blocks_> indicates the file pointer 
	//  point to new added block.
	//  return index of new added block
	// -------------------------------------------------------------------------
	fseek(fp_, -block_length_, SEEK_END);
	act_block_ = num_blocks_;
	int* blockIndex = (int*)malloc(sizeof(int) * n);
	for(int i = 0; i <= n - 1; i++) {
		blockIndex[i] = start_block + i;
	}
	return blockIndex;
}

// -----------------------------------------------------------------------------
//  delete last <num> block in the file.
//
//  NOTE: we just logically delete the data (only modifying the total number
//  of blcoks), the real data is still stored in file and the size of file is 
//  not changed.
// -----------------------------------------------------------------------------
bool BlockFile::delete_last_blocks(	// delete last <num> blocks
	int num)							// number of blocks to be deleted
{
	if (num > num_blocks_) return false;

	num_blocks_ -= num;				// update <num_blocks_>
	fseek(fp_, SIZEINT, SEEK_SET);
	fwrite_number(num_blocks_);

	fseek(fp_, 0, SEEK_SET);		// <fp> point to beginning of file
	act_block_ = 0;					// <act_block> = 0
	return true;
}
