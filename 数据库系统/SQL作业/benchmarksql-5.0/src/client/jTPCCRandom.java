/*
 * jTPCCUtil - utility functions for the Open Source Java implementation of
 *    the TPC-C benchmark
 *
 * Copyright (C) 2003, Raul Barbosa
 * Copyright (C) 2004-2016, Denis Lussier
 * Copyright (C) 2016, Jan Wieck
 *
 */


import java.io.*;
import java.sql.*;
import java.util.*;
import java.text.*;

public class jTPCCRandom
{
    private static final char[] aStringChars = {
	    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
	    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
	    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
	    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
	    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
    private static final String[] cLastTokens = {
	    "BAR", "OUGHT", "ABLE", "PRI", "PRES",
	    "ESE", "ANTI", "CALLY", "ATION", "EING"};

    private static long         nURandCLast;
    private static long         nURandCC_ID;
    private static long         nURandCI_ID;
    private static boolean      initialized = false;

    private     Random  random;

    /*
     * jTPCCRandom()
     *
     *     Used to create the master jTPCCRandom() instance for loading
     *     the database. See below.
     */
    jTPCCRandom()
    {
	if (initialized)
	    throw new IllegalStateException("Global instance exists");

	this.random = new Random(System.nanoTime());
	jTPCCRandom.nURandCLast = nextLong(0, 255);
	jTPCCRandom.nURandCC_ID = nextLong(0, 1023);
	jTPCCRandom.nURandCI_ID = nextLong(0, 8191);

	initialized = true;
    }

    /*
     * jTPCCRandom(CLoad)
     *
     *     Used to create the master jTPCCRandom instance for running
     *     a benchmark load.
     *
     *     TPC-C 2.1.6 defines the rules for picking the C values of
     *     the non-uniform random number generator. In particular
     *     2.1.6.1 defines what numbers for the C value for generating
     *     C_LAST must be excluded from the possible range during run
     *     time, based on the number used during the load.
     */
    jTPCCRandom(long CLoad)
    {
	long delta;

	if (initialized)
	    throw new IllegalStateException("Global instance exists");

	this.random = new Random(System.nanoTime());
	jTPCCRandom.nURandCC_ID = nextLong(0, 1023);
	jTPCCRandom.nURandCI_ID = nextLong(0, 8191);

	do
	{
	    jTPCCRandom.nURandCLast = nextLong(0, 255);

	    delta = Math.abs(jTPCCRandom.nURandCLast - CLoad);
	    if (delta == 96 || delta == 112)
		continue;
	    if (delta < 65 || delta > 119)
		continue;
	    break;
	} while(true);

	initialized = true;
    }

    private jTPCCRandom(jTPCCRandom parent)
    {
	this.random = new Random(System.nanoTime());
    }

    /*
     * newRandom()
     *
     *     Creates a derived random data generator to be used in another
     *     thread of the current benchmark load or run process. As per
     *     TPC-C 2.1.6 all terminals during a run must use the same C
     *     values per field. The jTPCCRandom Class therefore cannot
     *     generate them per instance, but each thread's instance must
     *     inherit those numbers from a global instance.
     */
    jTPCCRandom newRandom()
    {
	return new jTPCCRandom(this);
    }


    /*
     * nextLong(x, y)
     *
     *     Produce a random number uniformly distributed in [x .. y]
     */
    public long nextLong(long x, long y)
    {
	return (long)(random.nextDouble() * (y - x + 1) + x);
    }

    /*
     * nextInt(x, y)
     *
     *     Produce a random number uniformly distributed in [x .. y]
     */
    public int nextInt(int x, int y)
    {
	return (int)(random.nextDouble() * (y - x + 1) + x);
    }

    /*
     * getAString(x, y)
     *
     *     Procude a random alphanumeric string of length [x .. y].
     *
     *     Note: TPC-C 4.3.2.2 asks for an "alhpanumeric" string.
     *     Comment 1 about the character set does NOT mean that this
     *     function must eventually produce 128 different characters,
     *     only that the "character set" used to store this data must
     *     be able to represent 128 different characters. '#@!%%ÄÖß'
     *     is not an alphanumeric string. We can save ourselves a lot
     *     of UTF8 related trouble by producing alphanumeric only
     *     instead of cartoon style curse-bubbles.
     */
    public String getAString(long x, long y)
    {
	String result = new String();
	long len = nextLong(x, y);
	long have = 1;

	if (y <= 0)
	    return result;

	result += aStringChars[(int)nextLong(0, 51)];
	while (have < len)
	{
	    result += aStringChars[(int)nextLong(0, 61)];
	    have++;
	}

	return result;
    }

    /*
     * getNString(x, y)
     *
     *     Produce a random numeric string of length [x .. y].
     */
    public String getNString(long x, long y)
    {
	String result = new String();
	long len = nextLong(x, y);
	long have = 0;

	while (have < len)
	{
	    result += (char)(nextLong((long)'0', (long)'9'));
	    have++;
	}

	return result;
    }

    /*
     * getItemID()
     *
     *     Produce a non uniform random Item ID.
     */
    public int getItemID()
    {
	return (int)((((nextLong(0, 8191) | nextLong(1, 100000)) + nURandCI_ID)
	       % 100000) + 1);
    }

    /*
     * getCustomerID()
     *
     *     Produce a non uniform random Customer ID.
     */
    public int getCustomerID()
    {
	return (int)((((nextLong(0, 1023) | nextLong(1, 3000)) + nURandCC_ID)
	       % 3000) + 1);
    }

    /*
     * getCLast(num)
     *
     *     Produce the syllable representation for C_LAST of [0 .. 999]
     */
    public String getCLast(int num)
    {
	String result = new String();

	for (int i = 0; i < 3; i++)
	{
	    result = cLastTokens[num % 10] + result;
	    num /= 10;
	}

	return result;
    }

    /*
     * getCLast()
     *
     *     Procude a non uniform random Customer Last Name.
     */
    public String getCLast()
    {
	long num;
	num = (((nextLong(0, 255) | nextLong(0, 999)) + nURandCLast) % 1000);
	return getCLast((int)num);
    }

    public String getState()
    {
	String result = new String();

	result += (char)nextInt((int)'A', (int)'Z');
	result += (char)nextInt((int)'A', (int)'Z');

	return result;
    }

    /*
     * Methods to retrieve the C values used.
     */
    public long getNURandCLast()
    {
	return nURandCLast;
    }

    public long getNURandCC_ID()
    {
	return nURandCC_ID;
    }

    public long getNURandCI_ID()
    {
	return nURandCI_ID;
    }
} // end jTPCCRandom
