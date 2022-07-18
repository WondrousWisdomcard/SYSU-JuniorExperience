#include "util.h"

timeval  g_start_time;
timeval  g_end_time;

float    g_runtime = -1.0f;
float    g_ratio   = -1.0f;
float    g_recall  = -1.0f;
uint64_t g_io      = 0;
uint64_t g_memory  = 0;

// -------------------------------------------------------------------------
void create_dir(					// create directory
	char *path)							// input path
{
	int len = (int) strlen(path);
	for (int i = 0; i < len; ++i) {
		if (path[i] == '/') {
			char ch = path[i + 1];
			path[i + 1] = '\0';

			int ret = access(path, F_OK);
			if (ret != 0) {
				ret = mkdir(path, 0755);
				if (ret != 0) printf("Could not create %s\n", path);
			}
			path[i + 1] = ch;
		}
	}
}

// -----------------------------------------------------------------------------
int read_txt_data(					// read data (text) from disk
	int   n,							// number of data/query objects
	int   d,							// dimensionality
	const char *fname,					// address of data/query set
	float **data)						// data/query objects (return)
{
	gettimeofday(&g_start_time, NULL);
	FILE *fp = fopen(fname, "r");
	if (!fp) {
		printf("Could not open %s\n", fname);
		return 1;
	}

	int i = 0;
	int j = 0;
	while (!feof(fp) && i < n) {
		fscanf(fp, "%d", &j);
		for (j = 0; j < d; ++j) {
			fscanf(fp, " %f", &data[i][j]);
		}
		fscanf(fp, "\n");
		++i;
	}
	assert(feof(fp) && i == n);
	fclose(fp);

	gettimeofday(&g_end_time, NULL);
	float running_time = g_end_time.tv_sec - g_start_time.tv_sec + 
		(g_end_time.tv_usec - g_start_time.tv_usec) / 1000000.0f;
	printf("Read Data: %f Seconds\n\n", running_time);

	return 0;
}

// -----------------------------------------------------------------------------
int read_bin_data(					// read data (binary) from disk
	int   n,							// number of data points
	int   d,							// dimensionality
	const char *fname,					// address of data
	float **data)						// data/query objects (return)
{
	gettimeofday(&g_start_time, NULL);
	FILE *fp = fopen(fname, "rb");
	if (!fp) {
		printf("Could not open %s\n", fname);
		return 1;
	}

	int i = 0;
	while (!feof(fp) && i < n) {
		fread(data[i++], SIZEFLOAT, d, fp);
	}
	fclose(fp);

	gettimeofday(&g_end_time, NULL);
	float running_time = g_end_time.tv_sec - g_start_time.tv_sec + 
		(g_end_time.tv_usec - g_start_time.tv_usec) / 1000000.0f;
	printf("Read Data: %f Seconds\n\n", running_time);

	return 0;
}

// -----------------------------------------------------------------------------
int write_data_new_form(			// write dataset with new format
	int   n,							// cardinality
	int   d,							// dimensionality
	int   B,							// page size
	const float **data,					// data set
	const char *out_path) 				// output path
{
	gettimeofday(&g_start_time, NULL);
	
	// -------------------------------------------------------------------------
	//  check whether the directory exists
	// -------------------------------------------------------------------------
	char data_path[200];
	strcpy(data_path, out_path);
	strcat(data_path, "data/");
	
	printf("***data folder: %s\n",data_path);

	create_dir(data_path);
	
	// -------------------------------------------------------------------------
	//  write new format data for qalsh
	// -------------------------------------------------------------------------
	int num = (int) floor((float) B/(d*SIZEFLOAT)); // num of data in one page
	int total_file = (int) ceil((float) n / num); // total number of data file
	if (total_file == 0) return 1;
	
	char fname[200];
	char *buffer = new char[B];		// one buffer page size
	memset(buffer, 0, B * SIZECHAR);

	int left  = 0;
	int right = 0;

	for (int i = 0; i < total_file; ++i) {
		// ---------------------------------------------------------------------
		//  write data to buffer
		// ---------------------------------------------------------------------
		
		get_data_filename(i, data_path, fname);

		left  = i * num;
		right = left + num;
		if (right > n) right = n;	
		//将数据传到buffer中
		write_data_to_buffer(d, left, right, data, buffer);

		// ---------------------------------------------------------------------
		//  write one page of data to disk
		// ---------------------------------------------------------------------
		write_buffer_to_page(B, fname, (const char *) buffer);
	}
	delete[] buffer; buffer = NULL;

	gettimeofday(&g_end_time, NULL);
	float write_file_time = g_end_time.tv_sec - g_start_time.tv_sec + 
		(g_end_time.tv_usec - g_start_time.tv_usec) / 1000000.0f;
	printf("Write Dataset in New Format: %f Seconds\n\n", write_file_time);
	
	return 0;
}

// -----------------------------------------------------------------------------
inline void get_data_filename(		// get file name of data
	int   file_id,						// data file id
	const char *data_path,				// path to store data in new format
	char  *fname)						// file name of data (return)
{
	sprintf(fname, "%s%d.data", data_path, file_id);
}

// -----------------------------------------------------------------------------
inline void write_data_to_buffer(	// write data to buffer
	int   d,							// dimensionality
	int   left,							// left data id
	int   right,						// right data id
	const float **data,					// data set
	char  *buffer)						// buffer to store data (return)
{
	int c = 0;
	for (int i = left; i < right; ++i) {
		for (int j = 0; j < d; ++j) {
			memcpy(&buffer[c], &data[i][j], SIZEFLOAT);
			c += SIZEFLOAT;
		}
	}
}

// -----------------------------------------------------------------------------
inline int write_buffer_to_page(	// write buffer to one page
	int   B,							// page size
	const char *fname,					// file name of data
	const char *buffer)					// buffer to store data
{
	assert(fname != NULL && buffer != NULL);

	FILE *fp = fopen(fname, "wb");	// open data file to write
	fwrite(buffer, B, 1, fp);
	fclose(fp);
	return 0;
}

// -----------------------------------------------------------------------------
int read_data_new_format(			// read data with new format from disk
	int   id,							// index of data
	int   d,							// dimensionality
	int   B,							// page size
	const char *out_path,				// output path
	float *data)						// real data (return)
{
	// -------------------------------------------------------------------------
	//  get file name of data
	// -------------------------------------------------------------------------
	char fname[200];
	char data_path[200];
	strcpy(data_path, out_path);
	strcat(data_path, "data/");
									
	int num = (int) floor((float) B/(d*SIZEFLOAT)); // num of data in one page
	int file_id = (int) floor((float) id / num); // data file id
	get_data_filename(file_id, data_path, fname);

	// -------------------------------------------------------------------------
	//  read buffer (one page of data) in new format from disk
	// -------------------------------------------------------------------------
	char *buffer = new char[B];		// allocate one page size
	memset(buffer, 0, B * SIZECHAR);
	read_buffer_from_page(B, fname, buffer);

	// -------------------------------------------------------------------------
	//  read data from buffer
	// -------------------------------------------------------------------------
	int index = id % num;
	read_data_from_buffer(index, d, (const char *) buffer, data);
	delete[] buffer; buffer = NULL;

	return 0;
}

// -----------------------------------------------------------------------------
inline int read_buffer_from_page(	// read buffer from page
	int   B,							// page size
	const char *fname,					// file name of data
	char  *buffer)						// buffer to store data (return)
{
	assert(fname != NULL && buffer != NULL);

	FILE *fp = fopen(fname, "rb");
	fread(buffer, B, 1, fp);
	fclose(fp);

	return 0;
}

// -----------------------------------------------------------------------------
inline void read_data_from_buffer(	// read data from buffer
	int   index,						// index of data in buffer
	int   d,							// dimensionality
	const char *buffer,					// buffer to store data
	float *data)						// data set (return)
{
	int c = index * d * SIZEFLOAT;
	for (int i = 0; i < d; ++i) {
		memcpy(&data[i], &buffer[c], SIZEFLOAT);
		c += SIZEFLOAT;
	}
}

// -----------------------------------------------------------------------------
int read_ground_truth(				// read ground truth results from disk
	int qn,								// number of query objects
	const char *fname,					// address of truth set
	Result **R)							// ground truth results (return)
{
	gettimeofday(&g_start_time, NULL);
	FILE *fp = fopen(fname, "r");
	if (!fp) {
		printf("Could not open %s\n", fname);
		return 1;
	}

	int tmp1 = -1;
	int tmp2 = -1;
	fscanf(fp, "%d %d\n", &tmp1, &tmp2);
	assert(tmp1 == qn && tmp2 == MAXK);

	for (int i = 0; i < qn; ++i) {
		for (int j = 0; j < MAXK; ++j) {
			fscanf(fp, "%d %f ", &R[i][j].id_, &R[i][j].key_);
		}
		fscanf(fp, "\n");
	}
	fclose(fp);

	gettimeofday(&g_end_time, NULL);
	float running_time = g_end_time.tv_sec - g_start_time.tv_sec + 
		(g_end_time.tv_usec - g_start_time.tv_usec) / 1000000.0f;
	printf("Read Ground Truth: %f Seconds\n\n", running_time);

	return 0;
}

// -----------------------------------------------------------------------------
inline void get_lp_filename(		// get file name of L_p norm
	float p,							// the p value of L_p norm
	char  *fname)						// file name (return)
{
	sprintf(fname, "%sL%0.1f", fname, p);
}

// -----------------------------------------------------------------------------
float calc_lp_dist(					// calc L_{p} norm
	int   dim,							// dimension
	float p,							// the p value of Lp norm, p in (0,2]
	float threshold,					// threshold
	const float *vec1,					// 1st point
	const float *vec2)					// 2nd point
{
	if (fabs(p - 2.0f) < FLOATZERO) {
		return sqrt(calc_l2_sqr(dim, SQR(threshold), vec1, vec2));
	}
	else if (fabs(p - 1.0f) < FLOATZERO) {
		return calc_l1_dist(dim, threshold, vec1, vec2);
	}
	else if (fabs(p - 0.5f) < FLOATZERO) {
		float ret = calc_l0_sqrt(dim, sqrt(threshold), vec1, vec2);
		return SQR(ret);
	}
	else {
		float ret = calc_lp_pow(dim, p, pow(threshold, p), vec1, vec2);
		return pow(ret, 1.0f / p);
	}
}

// -----------------------------------------------------------------------------
float calc_l2_sqr(					// calc l2 square distance
	int   dim,							// dimension
	float threshold,					// threshold
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	unsigned d = dim & ~unsigned(7);
	const float *aa = p1, *end_a = aa + d;
	const float *bb = p2, *end_b = bb + d;

	float r = 0.0f;
	float r0, r1, r2, r3, r4, r5, r6, r7;

	const float *a = end_a, *b = end_b;

	r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = 0.0f;
	switch (dim & 7) {
		case 7: r6 = SQR(a[6] - b[6]);
		case 6: r5 = SQR(a[5] - b[5]);
		case 5: r4 = SQR(a[4] - b[4]);
		case 4: r3 = SQR(a[3] - b[3]);
		case 3: r2 = SQR(a[2] - b[2]);
		case 2: r1 = SQR(a[1] - b[1]);
		case 1: r0 = SQR(a[0] - b[0]);
	}

	a = aa; b = bb;
	for (; a < end_a; a += 8, b += 8) {
		r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
		if (r > threshold) return r;

		r0 = SQR(a[0] - b[0]);
		r1 = SQR(a[1] - b[1]);
		r2 = SQR(a[2] - b[2]);
		r3 = SQR(a[3] - b[3]);
		r4 = SQR(a[4] - b[4]);
		r5 = SQR(a[5] - b[5]);
		r6 = SQR(a[6] - b[6]);
		r7 = SQR(a[7] - b[7]);
	}
	r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
	
	return r;
}

// -----------------------------------------------------------------------------
float calc_l1_dist(					// calc Manhattan distance
	int   dim,							// dimension
	float threshold,					// threshold
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	unsigned d = dim & ~unsigned(7);
	const float *aa = p1, *end_a = aa + d;
	const float *bb = p2, *end_b = bb + d;

	float r = 0.0f;
	float r0, r1, r2, r3, r4, r5, r6, r7;

	const float *a = end_a, *b = end_b;

	r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = 0.0f;
	switch (dim & 7) {
		case 7: r6 = fabs(a[6] - b[6]);
		case 6: r5 = fabs(a[5] - b[5]);
		case 5: r4 = fabs(a[4] - b[4]);
		case 4: r3 = fabs(a[3] - b[3]);
		case 3: r2 = fabs(a[2] - b[2]);
		case 2: r1 = fabs(a[1] - b[1]);
		case 1: r0 = fabs(a[0] - b[0]);
	}

	a = aa; b = bb;
	for (; a < end_a; a += 8, b += 8) {
		r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
		if (r > threshold) return r;

		r0 = fabs(a[0] - b[0]);
		r1 = fabs(a[1] - b[1]);
		r2 = fabs(a[2] - b[2]);
		r3 = fabs(a[3] - b[3]);
		r4 = fabs(a[4] - b[4]);
		r5 = fabs(a[5] - b[5]);
		r6 = fabs(a[6] - b[6]);
		r7 = fabs(a[7] - b[7]);
	}
	r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
	
	return r;
}

// -----------------------------------------------------------------------------
float calc_l0_sqrt(					// calc L_{0.5} sqrt distance
	int   dim,							// dimension
	float threshold,					// threshold
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	unsigned d = dim & ~unsigned(7);
	const float *aa = p1, *end_a = aa + d;
	const float *bb = p2, *end_b = bb + d;

	float r = 0.0f;
	float r0, r1, r2, r3, r4, r5, r6, r7;

	const float *a = end_a, *b = end_b;

	r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = 0.0f;
	switch (dim & 7) {
		case 7: r6 = sqrt(fabs(a[6] - b[6]));
		case 6: r5 = sqrt(fabs(a[5] - b[5]));
		case 5: r4 = sqrt(fabs(a[4] - b[4]));
		case 4: r3 = sqrt(fabs(a[3] - b[3]));
		case 3: r2 = sqrt(fabs(a[2] - b[2]));
		case 2: r1 = sqrt(fabs(a[1] - b[1]));
		case 1: r0 = sqrt(fabs(a[0] - b[0]));
	}

	a = aa; b = bb;
	for (; a < end_a; a += 8, b += 8) {
		r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
		if (r > threshold) return r;

		r0 = sqrt(fabs(a[0] - b[0]));
		r1 = sqrt(fabs(a[1] - b[1]));
		r2 = sqrt(fabs(a[2] - b[2]));
		r3 = sqrt(fabs(a[3] - b[3]));
		r4 = sqrt(fabs(a[4] - b[4]));
		r5 = sqrt(fabs(a[5] - b[5]));
		r6 = sqrt(fabs(a[6] - b[6]));
		r7 = sqrt(fabs(a[7] - b[7]));
	}
	r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
	
	return r;
}

// -----------------------------------------------------------------------------
float calc_lp_pow(					// calc L_p pow_p distance
	int   dim,							// dimension
	float p,							// the p value of L_p norm, p in (0,2]
	float threshold,					// threshold
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	unsigned d = dim & ~unsigned(7);
	const float *aa = p1, *end_a = aa + d;
	const float *bb = p2, *end_b = bb + d;

	float r = 0.0f;
	float r0, r1, r2, r3, r4, r5, r6, r7;

	const float *a = end_a, *b = end_b;

	r0 = r1 = r2 = r3 = r4 = r5 = r6 = r7 = 0.0f;
	switch (dim & 7) {
		case 7: r6 = pow(fabs(a[6] - b[6]), p);
		case 6: r5 = pow(fabs(a[5] - b[5]), p);
		case 5: r4 = pow(fabs(a[4] - b[4]), p);
		case 4: r3 = pow(fabs(a[3] - b[3]), p);
		case 3: r2 = pow(fabs(a[2] - b[2]), p);
		case 2: r1 = pow(fabs(a[1] - b[1]), p);
		case 1: r0 = pow(fabs(a[0] - b[0]), p);
	}

	a = aa; b = bb;
	for (; a < end_a; a += 8, b += 8) {
		r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
		if (r > threshold) return r;

		r0 = pow(fabs(a[0] - b[0]), p);
		r1 = pow(fabs(a[1] - b[1]), p);
		r2 = pow(fabs(a[2] - b[2]), p);
		r3 = pow(fabs(a[3] - b[3]), p);
		r4 = pow(fabs(a[4] - b[4]), p);
		r5 = pow(fabs(a[5] - b[5]), p);
		r6 = pow(fabs(a[6] - b[6]), p);
		r7 = pow(fabs(a[7] - b[7]), p);
	}
	r += r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7;
	
	return r;
}

// -----------------------------------------------------------------------------
float calc_inner_product(			// calc inner product
	int   dim,							// dimension
	const float *p1,					// 1st point
	const float *p2)					// 2nd point
{
	float r = 0.0f;
	for (int i = 0; i < dim; ++i) {
		r += p1[i] * p2[i];
	}
	return r;
}

// -----------------------------------------------------------------------------
float calc_recall(					// calc recall (percentage)
	int  k,								// top-k value
	const Result *R,					// ground truth results 
	MinK_List *list)					// results returned by algorithms
{
	int i = k - 1;
	int last = k - 1;
	while (i >= 0 && list->ith_key(i) > R[last].key_) {
		i--;
	}
	return (i + 1) * 100.0f / k;
}

// -----------------------------------------------------------------------------
float calc_recall(					// calc recall (percentage)
	int k,								// top-k value
	const Result *R,					// ground truth results 
	const Result *result)				// results returned by algorithms
{
	int i = k - 1;
	int last = k - 1;
	while (i >= 0 && result[i].key_ > R[last].key_) {
		i--;
	}
	return (i + 1) * 100.0f / k;
}

// -----------------------------------------------------------------------------
uint64_t linear(					// linear scan search
	int   n,							// number of data objects
	int   d,							// dimensionality
	int   B,							// page size
	int   p,							// the p value of L_{p} distance
	int   top_k,						// top-k value
	const float *query,					// query object
	const char *data_folder,			// data folder
	MinK_List *list)					// k-NN results (return)
{
	// -------------------------------------------------------------------------
	//  calc <num> and <total_file>, where <num> is the number of data in one 
	//  data file and <total_file> is the total number of data file
	// -------------------------------------------------------------------------
	int num = (int) floor((float) B / (d * SIZEFLOAT));
	int total_file = (int) ceil((float) n / num);
	if (total_file == 0) return 0;

	// -------------------------------------------------------------------------
	//  linear scan method (data in disk)
	//  For each query, we limit that we can ONLY read one page of data
	// -------------------------------------------------------------------------
	char data_path[200];
	strcpy(data_path, data_folder);
	strcat(data_path, "data/");

	int   id      = 0;
	int   size    = 0;
	float dist    = -1.0f;
	float kdist   = MAXREAL;
	char  *buffer = new char[B];	// one page buffer
	float *data   = new float[d];	// one data object

	for (int i = 0; i < total_file; ++i) {
		// ---------------------------------------------------------------------
		//  read one page of data into buffer
		// ---------------------------------------------------------------------
		char fname[200];
		get_data_filename(i, data_path, fname);	
		read_buffer_from_page(B, fname, buffer);

		// ---------------------------------------------------------------------
		//  linear scan data objects in this page buffer
		// ---------------------------------------------------------------------
		if (i < total_file - 1) size = num;
		else size = n - num * (total_file - 1);

		for (int j = 0; j < size; ++j) {
			read_data_from_buffer(j, d, (const char *) buffer, data);
			dist = calc_lp_dist(d, p, kdist, (const float *) data, query);
			kdist = list->insert(dist, id++);
		}
	}
	delete[] buffer; buffer = NULL;
	delete[] data; data = NULL;
	
	return (uint64_t) total_file;
}

// -----------------------------------------------------------------------------
int ground_truth(					// find ground truth
	int   n,							// number of data  objects
	int   qn,							// number of query objects
	int   d,							// dimensionality
	float p,							// the p value of Lp norm, p in (0,2]
	const float **data,					// data set
	const float **query,				// query set
	const char  *truth_set)				// address of truth set
{
	gettimeofday(&g_start_time, NULL);
	FILE *fp = fopen(truth_set, "w");
	if (!fp) {
		printf("Could not create %s\n", truth_set);
		return 1;
	}

	// -------------------------------------------------------------------------
	//  find ground truth results (using linear scan method)
	// -------------------------------------------------------------------------
	fprintf(fp, "%d %d\n", qn, MAXK);

	MinK_List *list = new MinK_List(MAXK);
	for (int i = 0; i < qn; ++i) {
		list->reset();
		float kdist = MAXREAL;
		for (int j = 0; j < n; ++j) {
			float dist = calc_lp_dist(d, p, kdist, data[j], query[i]);
			kdist = list->insert(dist, j);
		}

		for (int j = 0; j < MAXK; ++j) {
			fprintf(fp, "%d %f ", list->ith_id(j), list->ith_key(j));
		}
		fprintf(fp, "\n");
	}
	fclose(fp);
	delete list; list = NULL;

	gettimeofday(&g_end_time, NULL);
	float truth_time = g_end_time.tv_sec - g_start_time.tv_sec + 
		(g_end_time.tv_usec - g_start_time.tv_usec) / 1000000.0f;
	printf("Ground Truth: %f Seconds\n\n", truth_time);

	return 0;
}
