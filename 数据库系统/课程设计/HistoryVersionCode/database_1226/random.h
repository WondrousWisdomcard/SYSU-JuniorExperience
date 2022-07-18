#ifndef __RANDOM_H
#define __RANDOM_H

#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstdlib>

#include "def.h"

// -----------------------------------------------------------------------------
//  functions used for generating random variables (r.v.)
// -----------------------------------------------------------------------------
inline float uniform(				// r.v. from Uniform(min, max)
	float min,							// min value
	float max)							// max value
{
	// assert(min <= max);
	// float x = min + (max - min) * (float)rand() / (float)RAND_MAX;
	// assert(x >= min && x <= max);
	// return x;

	return min + (max - min) * (float)rand() / (float)RAND_MAX;
}

// -----------------------------------------------------------------------------
float gaussian(						// r.v. from Gaussian(mean, sigma)
	float mu,							// mean (location)
	float sigma);						// stanard deviation (scale > 0)

// -----------------------------------------------------------------------------
float cauchy(						// r.v. from Cauchy(gamma, delta)
	float gamma,						// scale factor (gamma > 0)
	float delta);						// location

// -----------------------------------------------------------------------------
float levy(							// r.v. from Levy(gamma, delta)
	float gamma,						// scale factor (gamma > 0)
	float delta);						// location

// -----------------------------------------------------------------------------
float p_stable(						// r.v. from p-satble distr.
	float p,							// p value, where p in (0,2]
	float zeta,							// symmetric factor (zeta in [-1, 1])
	float gamma,						// scale factor (gamma > 0)
	float delta);						// location

// -----------------------------------------------------------------------------
//  functions used for calculating probability distribution function (pdf) and 
//  cumulative distribution function (cdf)
// -----------------------------------------------------------------------------
inline float gaussian_pdf(			// pdf of N(0, 1)
	float x)							// variable
{
	return exp(-x * x / 2.0f) / sqrt(2.0f * PI);
}

// -----------------------------------------------------------------------------
float gaussian_cdf(					// cdf of N(0, 1) in range (-inf, x]
	float x,							// integral border
	float step = 0.001f);				// step increment

// -----------------------------------------------------------------------------
float new_gaussian_cdf(				// cdf of N(0, 1) in range [-x, x]
	float x,							// integral border (x > 0)
	float step = 0.001f);				// step increment

// -----------------------------------------------------------------------------
inline float levy_pdf(				// pdf of Levy(1, 0)
	float x)							// variable
{
	return exp(-1.0f / (2.0f * x)) / (sqrt(2.0f * PI) * pow(x, 1.5f));
}

// -----------------------------------------------------------------------------
float levy_cdf(						// cdf of Levy(0, 1) in range (0, x]
	float x,							// integral border (x > 0)
	float step = 0.001f);				// step increment

// -----------------------------------------------------------------------------
//  query-oblivious and query-aware collision probability under gaussian
//  distribution, cauchy distribution and levy distribution
// -----------------------------------------------------------------------------
float orig_gaussian_prob(			// calc original gaussian probability
	float x);							// x = w / r

// -----------------------------------------------------------------------------
float new_gaussian_prob(			// calc new gaussian probability
	float x);							// x = w / (2 * r)

// -----------------------------------------------------------------------------
inline float orig_cauchy_prob(		// calc original cauchy probability
	float x)							// x = w / r
{
	return 2.0F * atan(x) / PI - log(1.0F + x * x) / (PI * x);
}

// -----------------------------------------------------------------------------
inline float new_cauchy_prob(		// calc new cauchy probability
	float x)							// x = w / (2 * r)
{
	return 2.0F * atan(x) / PI;
}

// -----------------------------------------------------------------------------
float orig_levy_prob(				// calc original levy probability
	float x);							// x = w / r

// -----------------------------------------------------------------------------
float new_levy_prob(				// calc new levy probability
	float x);							// x = w / (2 * r)

// -----------------------------------------------------------------------------
void orig_stable_prob(				// calc orig stable probability
	float p,							// the p value, where p in (0, 2]
	float zeta,							// symmetric factor (zeta in [-1, 1])
	float ratio,						// approximation ratio
	float radius,						// radius
	float w,							// bucket width
	int   num,							// number of repetition
	float &p1,							// p1 = p(w / r), returned
	float &p2);							// p2 = p(w / (c * r)), returned

// -----------------------------------------------------------------------------
void new_stable_prob(				// calc new stable probability
	float p,							// the p value, where p in (0, 2]
	float zeta,							// symmetric factor (zeta in [-1, 1])
	float ratio,						// approximation ratio
	float radius,						// radius
	float w,							// bucket width
	int   num,							// number of repetition
	float &p1,							// p1 = p(w / (2 *r)), returned
	float &p2);							// p2 = p(w / (2 * c * r)), returned

// -----------------------------------------------------------------------------
//  probability vs. w for a fixed ratio c
// -----------------------------------------------------------------------------
void prob_of_gaussian();			// curve of p1, p2 vs. w under gaussian

// -----------------------------------------------------------------------------
void prob_of_cauchy();				// curve of p1, p2 vs. w under cauchy

// -----------------------------------------------------------------------------
void prob_of_levy();				// curve of p1, p2 vs. w under levy

// -----------------------------------------------------------------------------
//  the difference (p1 - p2) vs. w for a fixed ratio
// -----------------------------------------------------------------------------
void diff_prob_of_gaussian();		// curve of p1 - p2 vs. w under gaussian

// -----------------------------------------------------------------------------
void diff_prob_of_cauchy();			// curve of p1 - p2 vs. w under cauchy

// -----------------------------------------------------------------------------
void diff_prob_of_levy();			// curve of p1 - p2 vs. w under levy

// -----------------------------------------------------------------------------
//  rho = log(1/p1) / log(1/p2) vs. w for a fixed ratio c
// -----------------------------------------------------------------------------
void rho_of_gaussian();				// curve of rho vs. w under gaussian

// -----------------------------------------------------------------------------
void rho_of_cauchy();				// curve of rho vs. w under cauchy

// -----------------------------------------------------------------------------
void rho_of_levy();					// curve of rho vs. w under levy

#endif // __RANDOM_H
