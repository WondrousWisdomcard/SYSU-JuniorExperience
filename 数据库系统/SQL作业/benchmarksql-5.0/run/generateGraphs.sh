#!/bin/sh
# ----
# Script to generate the detail graphs of a BenchmarkSQL run.
#
# Copyright (C) 2016, Denis Lussier
# Copyright (C) 2016, Jan Wieck
# ----

if [ $# -lt 1 ] ; then
    echo "usage: $(basename $0) RESULT_DIR [...]" >&2
    exit 2
fi

WIDTH=1200
HEIGHT=400

SIMPLE_GRAPHS="tpm_nopm latency cpu_utilization dirty_buffers"

for resdir in $* ; do
    cd "${resdir}" || exit 1

    for graph in $SIMPLE_GRAPHS ; do
	echo -n "Generating ${resdir}/${graph}.png ... "
	out=$(sed -e "s/@WIDTH@/${WIDTH}/g" -e "s/@HEIGHT@/${HEIGHT}/g" \
		  <../misc/${graph}.R | R --no-save)
	if [ $? -ne 0 ] ; then
	    echo "ERROR"
	    echo "$out" >&2
	    exit 3
	fi
	echo "OK"
    done

    for fname in ./data/blk_*.csv ; do
	if [ ! -f "${fname}" ] ; then
	    continue
	fi
	devname=$(basename ${fname} .csv)

	echo -n "Generating ${resdir}/${devname}_iops.png ... "
	out=$(sed -e "s/@WIDTH@/${WIDTH}/g" -e "s/@HEIGHT@/${HEIGHT}/g" \
		  -e "s/@DEVICE@/${devname}/g" <../misc/blk_device_iops.R | R --no-save)
	if [ $? -ne 0 ] ; then
	    echo "ERROR"
	    echo "$out" >&2
	    exit 3
	fi
	echo "OK"

	echo -n "Generating ${resdir}/${devname}_kbps.png ... "
	out=$(sed -e "s/@WIDTH@/${WIDTH}/g" -e "s/@HEIGHT@/${HEIGHT}/g" \
		  -e "s/@DEVICE@/${devname}/g" <../misc/blk_device_kbps.R | R --no-save)
	if [ $? -ne 0 ] ; then
	    echo "ERROR"
	    echo "$out" >&2
	    exit 3
	fi
	echo "OK"
    done

    for fname in ./data/net_*.csv ; do
	if [ ! -f "${fname}" ] ; then
	    continue
	fi
	devname=$(basename ${fname} .csv)

	echo -n "Generating ${resdir}/${devname}_iops.png ... "
	out=$(sed -e "s/@WIDTH@/${WIDTH}/g" -e "s/@HEIGHT@/${HEIGHT}/g" \
		  -e "s/@DEVICE@/${devname}/g" <../misc/net_device_iops.R | R --no-save)
	if [ $? -ne 0 ] ; then
	    echo "ERROR"
	    echo "$out" >&2
	    exit 3
	fi
	echo "OK"

	echo -n "Generating ${resdir}/${devname}_kbps.png ... "
	out=$(sed -e "s/@WIDTH@/${WIDTH}/g" -e "s/@HEIGHT@/${HEIGHT}/g" \
		  -e "s/@DEVICE@/${devname}/g" <../misc/net_device_kbps.R | R --no-save)
	if [ $? -ne 0 ] ; then
	    echo "ERROR"
	    echo "$out" >&2
	    exit 3
	fi
	echo "OK"
    done

    cd ..
done

