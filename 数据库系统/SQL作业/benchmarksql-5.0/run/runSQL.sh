#!/usr/bin/env bash

# ----
# Check command line usage
# ----
if [ $# -ne 2 ] ; then
    echo "usage: $(basename $0) PROPS_FILE SQL_FILE" >&2
    exit 2
fi

# ----
# Load common functions
# ----
source funcs.sh $1

# ----
# Determine which SQL file to use.
#
# 1) If $2 specifies a file that ends in .sql, we use that.
# 2) If a file ./sql.<dbtype>/$2.sql exists, we use that.
# 3) If none of the above, use ./sql.common/$2.sql.
# ----
if echo "$2" | grep -q -e '\.sql$' ; then
    ENDS_WITH_SQL=1
else
    ENDS_WITH_SQL=0
fi

if [ -f "${2}" -a $ENDS_WITH_SQL -eq 1 ] ; then
    SQL_FILE="$2"
else
    if [ -f "./sql.$(getProp db)/${2}.sql" ] ; then
        SQL_FILE="./sql.$(getProp db)/${2}.sql"
    else
    	SQL_FILE="./sql.common/${2}.sql"
	if [ ! -f "${SQL_FILE}" ] ; then
	   echo "ERROR: Cannot locate SQL file for ${2}" >&2
	   exit 1
	fi
    fi
fi

# ----
# Set myCP according to the database type.
# ----
setCP || exit 1

echo "# ------------------------------------------------------------"
echo "# Loading SQL file ${SQL_FILE}"
echo "# ------------------------------------------------------------"
myOPTS="-Dprop=$1"
myOPTS="$myOPTS -DcommandFile=${SQL_FILE}"
java -cp "$myCP" $myOPTS ExecJDBC
