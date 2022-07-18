BENCHMARKSQL README
===================

CHANGE LOG:
-----------

Version 5.0 lussman & jannicash:
--------------------------------------
  +  Upgrade to PostgreSQL 9.3 JDBC 4.1 version 1102 driver
  +  Improve support for Oracle
  +  Re-implement the non-uniform random generator in TPC-C style.
  +  Conform to clause 4.3.3.1 and enable lookup by last name
  +  Add a switch to disable terminal-warehouse association, spreading
     the data access over all configured warehouses.
  +  Re-worked the run shell scripts and the location of SQL files to
     make support of more database types easier.
  +  Add support for Firebird (http://www.firebirdsql.org).
  +  Add FOREIGN KEYS as defined by TPC-C 1.3.
  +  Major code overhaul. The per transaction type terminal data
     generation, execution and terminal trace code is moved into a
     module jTPCCTData. The database connection with all prepared
     statements has moved into a module jTPCCConnection.
  +  Add collecting per transaction result data and OS Level
     resource usage collection. The R statistics package is used
     to graph detailed information and a complete report in HTML
     can be generated from the data.

Version 4.1.2 TBD jannicash:
-----------------------------------
  + Fixed one more preparedStatement() leak. Hopefully with the help
    of Oracle's V$OPEN_CURSOR view we got them all now.
  + Fixed a possible deadlock problem in the NEW_ORDER transaction.
    Multiple parallel transaction could attempt to lock the same
    STOCK rows in reverse order. Sorting the order lines by item ID
    avoids this problem.

Version 4.1.1 2016-01-31 jannicash:
-----------------------------------
  + Changed the status line to update only once per second. The previous
    implementation was getting rather noisy at high throughput.
  + Fixed two preparedStatement() leaks that could cause ORA-01000 errors
    on longer runs with high throughput.
  + Fixed  a problem in the calculation of sleep time between
    transactions when using limitTxnsPerMin that could cause the test
    to hang at the end.
  + Added support for escaping ; as \; in SQL files to be able to load
    functions and execute anonymous PL blocks (needed for next item).
  + Changed the definition of history.hist_id into a plain integer with
    no special functionality. Two new database vendor specific SQL
    scripts allow to enable the column after data load as an auto
    incrementing primary key. See HOW-TO-RUN.txt for details.

Version 4.1.0 2014-03-13 lussman:
---------------------------------
  + Upgrade to using JDK 7
  + Upgrade to PostgreSQL JDBC 4.1 version 1101 driver
  + Stop claiming to support DB2 (only Postgres & Oracle are well tested)

Version 4.0.9 2013-11-04 cadym:
-------------------------------
  + Incorporate new PostgreSQL JDBC 4 version 1100 driver
  + Changed default user from postgres to benchmarksql
  + Added id column as primary key to history table
  + Renamed schema to benchmarksql
  + Changed log4j format to be more readable
  + Created the "benchmark" schema to contain all tables
  + Incorporate new PostgreSQL JDBC4 version 1003 driver
  + Transaction rate pacing mechanism
  + Correct error with loading customer table from csv file
  + Status line report dynamically shown on terminal
  + Fix lookup by name in PaymentStatus and Delivery Transactions
    (in order to be more compatible with the TPC-C spec)
  + Rationalized the variable naming in the input parameter files
    (now that the GUI is gone, variable names still make sense)
  + Default log4j settings only writes to file (not terminal)

Version 4.0.2  2013-06-06   lussman & cadym:
--------------------------------------------
  + Removed Swing & AWT GUI so that this program is runnable from
    the command line
  + Remove log4j usage from runSQL & runLoader (only used now for
    the actual running of the Benchmark)
  + Fix truncation problem with customer.csv file
  + Comment out "BadCredit" business logic that was not working
    and throwing stack traces
  + Fix log4j messages to always show the terminal name
  + Remove bogus log4j messages

Version 3.0.9 2013-03-21  lussman:
----------------------------------
  + Config log4j for rotating log files once per minute
  + Default flat file location to '/tmp/csv/' in
    table copies script
  + Drop incomplete & untested Windoze '.bat' scripts
  + Standardize logging with log4j
  + Improve Logging with meaningful DEBUG and INFO levels
  + Simplify "build.xml" to eliminate nbproject dependency
  + Defaults read in from propeerties
  + Groudwork laid to eliminate the GUI
  + Default GUI console to PostgreSQL and 10 Warehouses

Version 2.3.5  2013-01-29  lussman:
-----------------------------------
  + Default build is now with JDK 1.6 and JDBC 4 Postgres 9.2 driver
  + Remove outdated JDBC 3 drivers (for JDK 1.5).  You can run as
    before by a JDBC4 driver from any supported vendor.
  + Remove ExecJDBC warning about trying to rollback when in
    autocommit mode
  + Remove the extraneous COMMIT statements from the DDL scripts
    since ExecJDBC runs in autocommit mode
  + Fix the version number displayed in the console

Versions 1.0 thru 2.2  2004 - 2012 lussman:
-------------------------------------------
  + Dare to Compare
  + Forked from the jTPCC project
