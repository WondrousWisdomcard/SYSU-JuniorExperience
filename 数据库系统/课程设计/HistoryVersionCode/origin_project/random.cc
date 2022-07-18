#include "random.h"

// -----------------------------------------------------------------------------
//  functions used for generating random variables (r.v.).
//
//  use Box-Muller transform to generate a r.v. from Gaussian(mean, sigma)
//  standard Gaussian distr. is Gaussian(0, 1), where mean = 0 and sigma = 1
// -----------------------------------------------------------------------------
float gaussian(						// r.v. from N(mean, sigma)
	float mu,							// mean (location)
	float sigma)						// stanard deviation (scale > 0)
{
	// assert(sigma > 0.0f);
	float u1 = -1.0f;
	float u2 = -1.0f;
	do {
		u1 = uniform(0.0f, 1.0f);
	} while (u1 < FLOATZERO);
	u2 = uniform(0.0f, 1.0f);

	return mu + sigma * sqrt(-2.0f * log(u1)) * cos(2.0f * PI * u2);
	// return mu + sigma * sqrt(-2.0f * log(u1)) * sin(2.0f * PI * u2);
}

// -----------------------------------------------------------------------------
//  standard Cauchy distr. is Cauchy(1, 0), where gamma = 1 and delta = 0
// -----------------------------------------------------------------------------
float cauchy(						// r.v. from Cauchy(gamma, delta)
	float gamma,						// scale factor (gamma > 0)
	float delta)						// location
{
	// assert(gamma > 0.0f);
	float u = -1.0f;
	do {
		u = uniform(0.0f, 1.0f);
	} while (u < FLOATZERO || u > 1.0f - FLOATZERO);

	return gamma * tan(PI * (u - 0.5f)) + delta;

	// -------------------------------------------------------------------------
	//  another way to generate a standard Cauchy(1.0, 0.0) r.v.
	// -------------------------------------------------------------------------
	// float g1 = -1.0f, g2 = -1.0f;
	// g1 = gaussian(0.0f, 1.0f);
	// do {
	// 	g2 = gaussian(0.0f, 1.0f);
	// } while (fabs(g2) < FLOATZERO);

	// return (g1 / g2);
}

// -----------------------------------------------------------------------------
//  standard Levy distr. is Levy(1, 0), where gamma = 1 and delta = 0
// -----------------------------------------------------------------------------
float levy(							// r.v. from Levy(gamma, delta)
	float gamma,						// scale factor (gamma > 0)
	float delta)						// location
{
	// assert(gamma > 0.0f);
	float g = -1.0f;
	do {
		g = gaussian(0.0f, 1.0f);
	} while (fabs(g) < FLOATZERO);

	return gamma / (g * g) + delta;
}

// -----------------------------------------------------------------------------
//  generate a random variable from p-satble distribution
//  if beta == 0, the stable distribution is symmetric;
//  if beta != 0, the stable distribution is not symmetric.
//
//  the method come from section 1.7 of the book "stable distribution" by Nolan
// -----------------------------------------------------------------------------
float p_stable(						// r.v. from p-satble distr.
	float p,							// p value, where p in (0, 2]
	float zeta,							// symmetric factor (zeta in [-1, 1])
	float gamma,						// scale factor (gamma > 0)
	float delta)						// location
{
	// assert(p > 0.0f && p <= 2.0f);
	// assert(zeta >= -1.0f && zeta <= 1.0f);
	// assert(gamma > 0.0f);

	float x = -1.0f;				// r.v. from p-stable distr.
	float u1 = uniform(0.0f, 1.0f);	// r.v. from uniform distr.
	float u2 = uniform(0.0f, 1.0f);	// r.v. from uniform distr.

	float theta = PI * (u1 - 0.5f);
	float w = -log(u2);

	if (fabs(zeta) < FLOATZERO) {
		// ---------------------------------------------------------------------
		//  symmetric random variable
		// ---------------------------------------------------------------------
		if (fabs(p - 1.0f) < FLOATZERO) {
			x = tan(theta);
		}
		else {
			float t1 = sin(p * theta) / pow(cos(theta), 1.0f / p);
			float t2 = cos((p - 1.0f) * theta) / w;

			x = t1 * pow(t2, (1.0f - p) / p);
		}
	}
	else {
		// ---------------------------------------------------------------------
		//  non-symmetric random variable
		// ---------------------------------------------------------------------
		if (fabs(p - 1.0f) < FLOATZERO) {
			float t0 = PI / 2.0f;
			float t1 = (t0 + zeta * theta) * tan(theta);
			float t2 = (t0 * w * cos(theta)) / (t0 + zeta * theta);

			x = (t1 - zeta * log(t2)) / t0;
		}
		else {
			float t0 = atan(zeta * tan(PI * p / 2.0f)) / p;
			float t1 = sin(p * (t0 + theta));
			float t2 = pow(cos(p * t0) * cos(theta), 1.0f / p);
			float t3 = cos(p * t0 + (p - 1.0f) * theta) / w;

			x = t1 * pow(t3, (1.0f - p) / p) / t2;
		}
	}
	return gamma * x + delta;
}


// -----------------------------------------------------------------------------
//  functions used for calculating probability distribution function (pdf) and
//  cumulative distribution function (cdf).
// -----------------------------------------------------------------------------
float gaussian_cdf(					// cdf of N(0, 1) in range (-inf, x]
	float x,							// integral border
	float step)							// step increment
{
	float ret = 0.0f;
	for (float i = -10.0f; i < x; i += step) {
		ret += step * gaussian_pdf(i);
	}
	return ret;
}

// -----------------------------------------------------------------------------
float new_gaussian_cdf(				// cdf of N(0, 1) in range [-x, x]
	float x,							// integral border (x > 0)
	float step)							// step increment
{
	// assert(x > 0.0f);
	float ret = 0.0f;
	for (float i = -x; i <= x; i += step) {
		ret += step * gaussian_pdf(i);
	}
	return ret;
}

// -----------------------------------------------------------------------------
float levy_cdf(						// cdf of Levy(0, 1) in range (0, x]
	float x,							// integral border (x > 0)
	float step)							// step increment
{
	// assert(x > 0.0f);
	float ret = 0.0f;
	for (float i = step; i < x; i += step) {
		ret += (step * levy_pdf(i));
	}
	return ret;
}

// -----------------------------------------------------------------------------
//  query-oblivious and query-aware collision probability under gaussian
//  distribution and cauchy distribution
// -----------------------------------------------------------------------------
float orig_gaussian_prob(			// calc original gaussian probability
	float x)							// x = w / r
{
	float norm = gaussian_cdf(-x, 0.001F);
	float tmp  = 2.0F * (1.0F - exp(-x * x / 2.0F)) / (sqrt(2.0F * PI) * x);

	return 1.0F - 2.0F * norm - tmp;
}

// -----------------------------------------------------------------------------
float new_gaussian_prob(			// calc new gaussian probability
	float x)							// x = w / (2 * r)
{
	return new_gaussian_cdf(x, 0.001F);
}

// -----------------------------------------------------------------------------
float orig_levy_prob(				// calc original levy probability
	float x)							// x = w / r
{
	float p    = 0.0F;
	float step = 0.001F;
	for (float i = step; i < x; i += step) {
		p += (step * levy_pdf(i) * (1.0F - i / x));
	}
	return p;
}

// -----------------------------------------------------------------------------
float new_levy_prob(				// calc new levy probability
	float x)							// x = w / (2 * r)
{
	return levy_cdf(x, 0.001F);
}

// -----------------------------------------------------------------------------
//  use Monte Carlo method to simulate the original collision probability
// -----------------------------------------------------------------------------
void orig_stable_prob(				// calc orig stable probability
	float p,							// the p value, where p in (0, 2]
	float zeta,							// symmetric factor (zeta in [-1, 1])
	float ratio,						// approximation ratio
	float radius,						// radius
	float w,							// bucket width
	int   num,							// number of repetition
	float &p1,							// p1 = p(w / r) (return)
	float &p2)							// p2 = p(w / (c * r)) (return)
{
	// assert(p > 0.0f && p <= 2.0f);
	// assert(zeta >= -1.0f && zeta <= 1.0f);

	int   d = 30;					// d can be any value larger than 1
	float *object = new float[d];	// init the object and queries
	float *query1 = new float[d];	// query 1: distance is radius
	float *query2 = new float[d];	// query 2: distance is ratio * radius

	object[0] = uniform(0.0f, 1.0f);
	query1[0] = object[0] + radius;
	query2[0] = object[0] + ratio * radius;

	for (int i = 1; i < d; ++i) {
		object[i] = uniform(0.0f, 1.0f);
		query1[i] = object[i];
		query2[i] = object[i];
	}

	int bucket_count_1 = 0;
	int bucket_count_2 = 0;

	float *a = new float[d];
	float b  = -1.0f;

	float delta = 0.0f;
	float gamma = 1.0f;				// for gaussian distr. gamma != 1.0f
	if (fabs(p - 2.0f) < FLOATZERO) gamma = 1.0f / sqrt(2.0f);

	for (int i = 0; i < num; ++i) {
		// ---------------------------------------------------------------------
		//  generate a new hash func for each repetition
		// ---------------------------------------------------------------------
		for (int j = 0; j < d; ++j) {
			a[j] = p_stable(p, zeta, gamma, delta);
		}
		b = uniform(0.0f, w);

		// ---------------------------------------------------------------------
		//  hash the object and queries into buckets
		// ---------------------------------------------------------------------
		float obj_proj_dist = 0.0f;
		float q1_proj_dist = 0.0f;
		float q2_proj_dist = 0.0f;

		for (int j = 0; j < d; ++j) {
			obj_proj_dist += object[j] * a[j];
			q1_proj_dist += query1[j] * a[j];
			q2_proj_dist += query2[j] * a[j];
		}
		obj_proj_dist += b;
		q1_proj_dist += b;
		q2_proj_dist += b;

		long obj_bucket = (long) floor(obj_proj_dist / w);
		long q1_bucket  = (long) floor(q1_proj_dist / w);
		long q2_bucket  = (long) floor(q2_proj_dist / w);

		// ---------------------------------------------------------------------
		//  perform original collision counting
		// ---------------------------------------------------------------------
		if (obj_bucket == q1_bucket) bucket_count_1++;
		if (obj_bucket == q2_bucket) bucket_count_2++;
	}
	// -------------------------------------------------------------------------
	//  calculate original collision probabilities
	// -------------------------------------------------------------------------
	p1 = (float) bucket_count_1 / (float) num;
	p2 = (float) bucket_count_2 / (float) num;

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete[] a; a = NULL;
	delete[] object; object = NULL;
	delete[] query1; query1 = NULL;
	delete[] query2; query2 = NULL;
}

// -----------------------------------------------------------------------------
//  Using Monte Carlo method to simulate the new collision probability
// -----------------------------------------------------------------------------
void new_stable_prob(				// calc new stable probability
	float p,							// the p value, where p in (0, 2]
	float zeta,							// symmetric factor (zeta in [-1, 1])
	float ratio,						// approximation ratio
	float radius,						// radius
	float w,							// bucket width
	int   num,							// number of repetition
	float &p1,							// p1 = p(w / r) (return)
	float &p2)							// p2 = p(w / (c * r)) (return)
{
	// assert(p > 0.0f && p <= 2.0f);
	// assert(zeta >= -1.0f && zeta <= 1.0f);

	int d = 30;						// d can be any value larger than 1
	float *object = new float[d];	// init the object and queries
	float *query1 = new float[d];	// query 1: distance is radius
	float *query2 = new float[d];	// query 2: distance is ratio * radius

	object[0] = uniform(0.0f, 1.0f);
	query1[0] = object[0] + radius;
	query2[0] = object[0] + ratio * radius;

	for (int i = 1; i < d; ++i) {
		object[i] = uniform(0.0f, 1.0f);
		query1[i] = object[i];
		query2[i] = object[i];
	}

	int dist_count_1 = 0;
	int dist_count_2 = 0;

	float *a = new float[d];
	float delta = 0.0f;
	float gamma = 1.0f;				// for gaussian distr. gamma != 1.0f
	if (fabs(p - 2.0f) < FLOATZERO) gamma = 1.0f / sqrt(2.0f);

	for (int i = 0; i < num; ++i) {
		// ---------------------------------------------------------------------
		//  generate a new hash func for each repetition
		// ---------------------------------------------------------------------
		for (int j = 0; j < d; ++j) {
			a[j] = p_stable(p, zeta, gamma, delta);
		}

		// ---------------------------------------------------------------------
		//  hash the object and queries (random projection)
		// ---------------------------------------------------------------------
		float obj_proj_dist = 0.0f;
		float q1_proj_dist  = 0.0f;
		float q2_proj_dist  = 0.0f;

		for (int j = 0; j < d; ++j) {
			obj_proj_dist += object[j] * a[j];
			q1_proj_dist  += query1[j] * a[j];
			q2_proj_dist  += query2[j] * a[j];
		}

		// ---------------------------------------------------------------------
		//  perform new collision counting
		// ---------------------------------------------------------------------
		if (fabs(obj_proj_dist - q1_proj_dist) < w / 2.0f) dist_count_1++;
		if (fabs(obj_proj_dist - q2_proj_dist) < w / 2.0f) dist_count_2++;
	}
	// -------------------------------------------------------------------------
	//  calculate new collision probabilities
	// -------------------------------------------------------------------------
	p1 = (float) dist_count_1 / (float) num;
	p2 = (float) dist_count_2 / (float) num;

	// -------------------------------------------------------------------------
	//  release space
	// -------------------------------------------------------------------------
	delete[] a; a = NULL;
	delete[] object; object = NULL;
	delete[] query1; query1 = NULL;
	delete[] query2; query2 = NULL;
}

// -----------------------------------------------------------------------------
//  probability vs. w for a fixed ratio c
// -----------------------------------------------------------------------------
void prob_of_gaussian()				// curve of p1, p2 vs. w under gaussian
{
	printf("probability vs. w for c = {2.0, 3.0} under gaussian\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_gaussian_prob(w);
			orig_p2 = orig_gaussian_prob(w / c[i]);

			new_p1 = new_gaussian_prob(w / 2.0f);
			new_p2 = new_gaussian_prob(w / (2.0f * c[i]));

			printf("%.1f\t%.4f\t%.4f\t%.4f\t%.4f\n",
				w, orig_p1, orig_p2, new_p1, new_p2);
		}
		printf("\n");
	}
}

// -----------------------------------------------------------------------------
void prob_of_cauchy()				// curve of p1, p2 vs. w under cauchy
{
	printf("probability vs. w for c = {2.0, 3.0} under cauchy\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_cauchy_prob(w);
			orig_p2 = orig_cauchy_prob(w / c[i]);

			new_p1 = new_cauchy_prob(w / 2.0f);
			new_p2 = new_cauchy_prob(w / (2.0f * c[i]));

			printf("%.1f\t%.4f\t%.4f\t%.4f\t%.4f\n",
				w, orig_p1, orig_p2, new_p1, new_p2);
		}
		printf("\n");
	}
}

// -----------------------------------------------------------------------------
void prob_of_levy()					// curve of p1, p2 vs. w under levy
{
	printf("probability vs. w for c = {2.0, 3.0} under levy\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_levy_prob(w);
			orig_p2 = orig_levy_prob(w / c[i]);

			new_p1 = new_levy_prob(w / 2.0f);
			new_p2 = new_levy_prob(w / (2.0f * c[i]));

			printf("%.1f\t%.4f\t%.4f\t%.4f\t%.4f\n",
				w, orig_p1, orig_p2, new_p1, new_p2);
		}
		printf("\n");
	}
}

// -----------------------------------------------------------------------------
//  the difference (p1 - p2) vs. w for a fixed ratio
// -----------------------------------------------------------------------------
void diff_prob_of_gaussian()		// curve of p1 - p2 vs. w under gaussian
{
	printf("prob of diff vs. w for c = {2.0, 3.0} under gaussian\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2, orig_diff, new_diff;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_gaussian_prob(w);
			orig_p2 = orig_gaussian_prob(w / c[i]);
			orig_diff = orig_p1 - orig_p2;

			new_p1 = new_gaussian_prob(w / 2.0f);
			new_p2 = new_gaussian_prob(w / (2.0f * c[i]));
			new_diff = new_p1 - new_p2;

			printf("%.1f\t%.4f\t%.4f\n", w, orig_diff, new_diff);
		}
		printf("\n");
	}
}

// -----------------------------------------------------------------------------
void diff_prob_of_cauchy()			// curve of p1 - p2 vs. w under cauchy
{
	printf("prob of diff vs. w for c = {2.0, 3.0} under cauchy\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2, orig_diff, new_diff;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_cauchy_prob(w);
			orig_p2 = orig_cauchy_prob(w / c[i]);
			orig_diff = orig_p1 - orig_p2;

			new_p1 = new_cauchy_prob(w / 2.0f);
			new_p2 = new_cauchy_prob(w / (2.0f * c[i]));
			new_diff = new_p1 - new_p2;

			printf("%.1f\t%.4f\t%.4f\n", w, orig_diff, new_diff);
		}
		printf("\n");
	}
}

// -----------------------------------------------------------------------------
void diff_prob_of_levy()			// curve of p1 - p2 vs. w under levy
{
	printf("prob of diff vs. w for c = {2.0, 3.0} under levy\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2, orig_diff, new_diff;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_levy_prob(w);
			orig_p2 = orig_levy_prob(w / c[i]);
			orig_diff = orig_p1 - orig_p2;

			new_p1 = new_levy_prob(w / 2.0f);
			new_p2 = new_levy_prob(w / (2.0f * c[i]));
			new_diff = new_p1 - new_p2;

			printf("%.1f\t%.4f\t%.4f\n", w, orig_diff, new_diff);
		}
		printf("\n");
	}
}

// -----------------------------------------------------------------------------
//  rho = log(1/p1) / log(1/p2) vs. w for a fixed ratio c
// -----------------------------------------------------------------------------
void rho_of_gaussian()				// curve of rho vs. w under gaussian
{
	printf("rho vs. w for c = {2.0, 3.0} under gaussian\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2, orig_rho, new_rho;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_gaussian_prob(w);
			orig_p2 = orig_gaussian_prob(w / c[i]);
			orig_rho = log(1.0f / orig_p1) / log(1.0f / orig_p2);

			new_p1 = new_gaussian_prob(w / 2.0f);
			new_p2 = new_gaussian_prob(w / (2.0f * c[i]));
			new_rho = log(1.0f / new_p1) / log(1.0f / new_p2);

			printf("%.1f\t%.4f\t%.4f\t%.4f\n", w, orig_rho, new_rho, 1.0f / c[i]);
		}
		printf("\n");
	}
}


// -----------------------------------------------------------------------------
void rho_of_cauchy()				// curve of rho vs. w under cauchy
{
	printf("rho vs. w for c = {2.0, 3.0} under cauchy\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2, orig_rho, new_rho;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_cauchy_prob(w);
			orig_p2 = orig_cauchy_prob(w / c[i]);
			orig_rho = log(1.0f / orig_p1) / log(1.0f / orig_p2);

			new_p1 = new_cauchy_prob(w / 2.0f);
			new_p2 = new_cauchy_prob(w / (2.0f * c[i]));
			new_rho = log(1.0f / new_p1) / log(1.0f / new_p2);

			printf("%.1f\t%.4f\t%.4f\t%.4f\n", w, orig_rho, new_rho, 1.0f / c[i]);
		}
		printf("\n");
	}
}

// -----------------------------------------------------------------------------
void rho_of_levy()					// curve of rho vs. w under levy
{
	printf("rho vs. w for c = {2.0, 3.0} under levy\n");
	float c[2] = { 2.0f, 3.0f };
	float orig_p1, orig_p2, new_p1, new_p2, orig_rho, new_rho;

	for (int i = 0; i < 2; ++i) {
		printf("c = %.1f\n", c[i]);

		for (float w = 0.5f; w < 10.1f; w += 0.5f) {
			orig_p1 = orig_levy_prob(w);
			orig_p2 = orig_levy_prob(w / c[i]);
			orig_rho = log(1.0f / orig_p1) / log(1.0f / orig_p2);

			new_p1 = new_levy_prob(w / 2.0f);
			new_p2 = new_levy_prob(w / (2.0f * c[i]));
			new_rho = log(1.0f / new_p1) / log(1.0f / new_p2);

			printf("%.1f\t%.4f\t%.4f\t%.4f\n", w, orig_rho, new_rho, 1.0f / c[i]);
		}
		printf("\n");
	}
}
