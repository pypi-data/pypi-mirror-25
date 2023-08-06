Release History
===============

**1.3.0 2017-10-03**

*   some more xlsx luxury
*   added more queries
*   added the ability to dump the built-in queries to stdout
*   re-worked the cmd-line parameters (-d is now where it belongs to...)

**1.2.2 2017-09-26**

*   documentation fixes

**1.2.1 2017-09-25**

*   removed percentile() from the most queries, due to too long runtime on
    huge datasets
*   added the possibility to select a group of queries on *analyze*

**1.2.0 2017-09-24**

*   now analyze runs up to cpu_count subprocesses, which will run the queries
    in parallel
*   added cmdline parameter ``--procs`` to allow to set the no. of
    subprocesses to use, bypassing the cpu_count

**1.1.1 2017-09-23**

*   added per-day queries
*   all numerical fields in the XLSX file now formated as #.##0

**1.1.0 2017-09-23**

*   re-built the mechanism to add individual queries
*   \*.spec file prepared to build with pyinstaller w/o change on macOS and
    Linux

**1.0.4 2017-09-22**

*   a little more featured XLXS files

**1.0.3 2017-09-21**

*   now creating a single XLSX file on *analyze*, added option -c to create
    CSV files instead

**1.0.2 2017-09-16**

*   fixed the timestamp column (now hold the seconds since Epoch)

**1.0.1 2017-09-15**

*   now we do understand log records of access to the Default Namespace properly
*   speed-up of unpacking by just unpacking the required archives

**1.0.0 2017-09-10**

*   initial release
