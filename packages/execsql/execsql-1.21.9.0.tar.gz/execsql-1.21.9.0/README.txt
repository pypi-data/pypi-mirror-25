execsql.py
=========================

*Multi-DBMS SQL script processor.*

execsql.py is a Python program that applies a SQL script stored in a text file 
to a PostgreSQL, MS-Access, SQLite, MS-SQL-Server, MySQL, MariaDB, or Firebird 
database, or to an ODBC DSN.  execsql.py also supports a set of special 
commands (metacommands) that can import and export data, copy data between 
databases, and conditionally execute SQL statements and metacommands.  
These metacommands make up a control language that works the same across 
all supported database management systems (DBMSs). The metacommands are 
embedded in SQL comments, so they will be ignored by other script 
processors (e.g., psql for Postgres and sqlcmd for SQL Server).  The 
metacommands make up a toolbox that can be used to create both automated 
and interactive data processing applications.


Capabilities
=========================

You can use execsql to:

* Import data from text files or OpenDocument spreadsheets into a database.

* Copy data between different databases, even databases using different types of database management systems.

* Export tables and views as formatted text, comma-separated values (CSV), tab-separated values (TSV), OpenDocument spreadsheets, HTML tables, JSON, LaTeX tables, or unformatted (e.g., binary) data.

* Export data to non-tabular formats using several different template processors.

* View tables and views on the console or in a GUI dialog window.

* Conditionally execute different SQL commands and metacommands based on the DBMS in use, the database in use, data values, user input, and other conditions. Conditional execution can be used with the INCLUDE metacommand to implement loops.

* Use simple dynamically-created data entry forms to get user input.

* Write messages to the console or to a file during the processing of a SQL script, using metacommands embedded in SQL comments. These messages can be used to display the progress of the script or create a custom log of the operations that have been carried out or results obtained. Status messages and data exported in text format can be combined in a single text file. Data tables can be exported in a text format that is compatible with Markdown pipe tables, so that script output can be converted into a variety of document formats.

* Write more modular and maintainable SQL code by factoring repeated code out into separate scripts, parameterizing the code using substitution variables, and using the INCLUDE metacommand to merge the modules into a single script.

* Merge multiple elements of a workflow—e.g., data loading, summarization, and reporting—into a single script for better coupling of related steps and more secure maintenance.

Standard SQL provides no features for interacting with external files or 
with the user, or for controlling the flow of actions to be carried out
based either on data or on user input.  execsql provides these features
in a way that operates identically across all supported DBMSs on both
Linux and Windows.

execsql is inherently a command-line program that can operate in a completely 
non-interactive mode (except for password prompts). Therefore, it is suitable 
for incorporation into a toolchain controlled by a shell script (on Linux), 
batch file (on Windows), or other system-level scripting application. When 
used in this mode, the only interactive elements will be password prompts; 
passwords are not accepted on the command line or as arguments to the 
CONNECT metacommand. However, several metacommands can be used to generate
interactive prompts and data displays, so execsql scripts can be written to 
provide some user interactivity.

In addition, execsql automatically maintains a log that documents key 
information about each run of the program, including the databases that are 
used, the scripts that are run, and the user's choices in response to 
interactive prompts. Together, the script and the log provide documentation 
of all actions carried out that may have altered data.


Syntax and Options
========================


Commands
------------------------

    execsql.py -ta [other options] sql_script_file Access_db 

    execsql.py -tf [other options] sql_script_file Firebird_host Firebird_db

    execsql.py -tm [other options] sql_script_file MySQL_host MySQL_db 

    execsql.py -tp [other options] sql_script_file Postgres_host Postgres_db

    execsql.py -ts [other options] sql_script_file SQL_Server_host SQL_Server_db

    execsql.py -tl [other options] sql_script_file SQLite_db 


Arguments
--------------------------

     sql_script_file   The name of a text file of SQL commands to be executed. Required argument.

     Access_db         The name of the Access database against which to run the SQL.

     Firebird_db       The name of the Firebird database against which to run the SQL.

     Firebird_host     The name of the Firebird host (server) against which to run the SQL. 

     MySQL_db          The name of the MySQL database against which to run the SQL.

     MySQL_host        The name of the MySQL host (server) against which to run the SQL.

     Postgres_db       The name of the Postgres database against which to run the SQL.

     Postgres_host     The name of the Postgres host (server) against which to run the SQL. 

     SQL_Server_db     The name of the SQL Server database against which to run the SQL.

     SQL_Server_host   The name of the SQL Server host (server) against which to run the SQL. 

     SQLite_db         The name of the SQLite database against which to run the SQL.


Options
---------------------

    -a value        Define the replacement for a substitution variable $ARG_x. 
    -d value        Automatically make directories used by the 	EXPORT
                    metacommand: 'n'-no (default); 'y'-yes.
    -e value        Character encoding of the database. Only used for some 
                      database types. 
    -f value        Character encoding of the script file. 
    -g value        Character encoding to use for output of the WRITE and EXPORT
                    metacommands. 
    -i value        Character encoding to use for data files imported with the 
                    IMPORT metacommand. 
    -m              Display the allowable metacommands, and exit. 
    -p value        The port number to use for client-server databases. 
    -s value        The number of lines of an IMPORTed file to scan to diagnose 
                    the quote and delimiter characters. 
    -t value        Type of database: 
                          'p'-Postgres, 
                          'f'-Firebird, 
                          'l'-SQLite, 
                          'm'-MySQL or MariaDB, 
                          'a'-Access, 
                          's'-SQL Server, 
                          'd'-DSN connection.
    -u value        The database user name (optional). 
    -v value        Use a GUI for interactive prompts. 
    -w              Do not prompt for the password when the user is specified. 
    -y              List all valid character encodings and exit. 
    -z value        Buffer size, in kb, to use with the IMPORT metacommand 
                    (the default is 32).


Requirements
===========================

The execsql program uses third-party Python libraries to communicate with 
different database and spreadsheet software. These libraries must be 
installed to use those programs with execsql. Only those libraries that 
are needed, based on the command line arguments and metacommands, must 
be installed. The libraries required for each database or spreadsheet 
application are:

* PosgreSQL: psycopg2.

* SQL Server: pydobc.

* MS-Access: pydobc and pywin32.

* MySQL or MariaDB: pymysql.

* Firebird: fdb.

* DSN connections: pyodbc.

* OpenDocument spreadsheets: odfpy.

* Excel spreadsheets (read only): xlrd.

Connections to SQLite databases are made using Python's standard library, 
so no additional software is needed.

If the Jinja or Airspeed template processors will be used, those software
libraries must also be installed.



Distribution History
============================


Version  | Date       | Features
-------- | ---------- | ----------------------------------------------
1.21.9.0 | 2017-09-06 | Modified to handle trailing comments on SQL script lines.
1.21.8.0 | 2017-08-11 | Modified to allow a password to be specified in the CONNECT metacommand for MySQL.
1.21.7.0 | 2017-08-05 | Modified to allow import of CSV files with more columns than the target table.  Added DEBUG metacommands.
1.21.1.0 | 2017-07-04 | Passed column headers to template processors as a separate object.
1.21.0.0 | 2017-07-01 | Extended the EXPORT metacommand to allow several different template processors to be used.
1.20.0.0 | 2017-06-30 | Added the EMAIL, SUB_ENCRYPT, and SUB_DECRYPT metacommands, and configuration properties to support emailing.  Added the METACOMMAND_ERROR_HALT metacommand, the $METACOMMAND_ERROR_HALT_STATE system variable, and the METACOMMAND_ERROR() conditional.
1.18.0.0 | 2017-06-24 | Improved the speed of import of CSV files to Postgres and MySQL/MariaDB.  Modified the EXPORT...APPEND...AS HTML metacommand to append tables *inside* the (first) </body> tag.
1.17.0.0 | 2017-05-28 | Modified the specifications for the PROMPT ENTRY_FORM to allow checkboxes to be used.
1.16.9.0 | 2017-05-27 | Added a DESCRIPTION keyword to the EXPORT metacommands.
1.16.8.0 | 2017-05-20 | Added the VALUES export format.
1.16.7.0 | 2017-05-20 | Added BOOLEAN_INT and BOOLEAN_WORDS metacommands.  Allowed the PAUSE metacommand to take fractional timeout arguments.  Added a 'console_wait_when_done' configuration parameter.  Added the server name to the password prompt.
1.16.3.0 | 2017-04-23 | Added a configuration option allowing the specification of additional configuration  files to read.  Added a MAX_INT configuration parameter and metacommand.
1.16.0.0 | 2017-03-25 | Added the BEGIN SCRIPT, END SCRIPT, and EXECUTE SCRIPT metacommands. 
1.15.0.0 | 2017-03-09 | Added the TEE keyword to the WRITE, EXPORT, and EXPORT QUERY metacommands.
1.13.0.0 | 2017-03-05 | Added the LOG_WRITE_MESSAGES metacommand and configuration parameter.
1.12.0.0 | 2017-03-04 | Added a 'boolean_words' configuration option. Enabled reading of CSV files with newlines within delimited text data.  Added the SKIP keyword to the IMPORT metacommand for CSV, ODS, and Excel data.  Added the COLUMN_EXISTS conditional. 
1.8.15.0 | 2017-01-14 | Added a $LAST_ROWCOUNT system variable.
1.8.14.0 | 2016-11-13 | Added evaluation of numeric types in input.  Added 'empty_strings' configuration parameter and metacommand.  Corrections to IMPORT metacommand for Firebird.
1.8.13.0 | 2016-11-07 | Added the "-b" command-line option and configuration parameter.
1.8.12.0 | 2016-10-22 | Added the RM_SUB metacommand.
1.8.11.0 | 2016-10-19 | Added the SET COUNTER metacommand.
1.8.10.2 | 2016-10-17 | Added $RUN_ID system variable Modified to recognize as text any imported data that contains only numeric values but where the first digit of any value is a zero.
1.8.8.0  | 2016-09-28 | Added $CURRENT_ALIAS, $RANDOM, and $UUID system variables.
1.8.4.0  | 2016-08-13 | Added logging of database close when autocommit is off.  Added import from MS-Excel.  Corrected parsing of numeric time zones. 
1.7.3.0  | 2016-08-05 | Added $OS system variable.
1.7.2.0  | 2016-06-11 | Added DIRECTORY_EXISTS conditional and option to automatically make directories used by the EXPORT metacommand. 
1.7.0.0  | 2016-05-20 | Added NEWER_DATE and NEWER_FILE conditionals.
1.6.0.0  | 2016-05-15 | Added CONSOLE SAVE metacommand.  Added DSN connections.  Added COPY QUERY and EXPORT QUERY metacommands.
1.4.4.0  | 2016-05-02 | Added CONSOLE HIDE|SHOW metacommands and allowed <Enter> in response to the CONSOLE  WAIT metacommand, to continue without closing.
1.4.2.0  | 2016-05-02 | Added a "Save as..." menu to the GUI console and changed the PAUSE and HALT metacommands to use a GUI if the console is on.
1.4.0.0  | 2016-04-30 | Added a GUI console with a status bar and progress bar to which WRITE output and exported text will be written.
1.3.3.0  | 2016-04-09 | Additions to 'Save as...' options in PROMPT DISPLAY metacommand, and date/time values exported to ODS.
1.3.2.0  | 2016-02-28 | Enabled the use of a backslash as a line continuation character for SQL statements.
1.3.1.0  | 2016-02-20 | Added PROMPT ENTRY_FORM and LOG metacommands.
1.2.15.0 | 2016-02-14 | Added $DB_NAME, $DB_NEED_PWD, $DB_SERVER, and $DB_USER system variables.  Added RAW as an export format for binary data.  Added a PASSWORD keyword to the PROMPT ENTER_SUB metacommand.  Allowed a password to be used in the CONNECT metacommand for Access. Other minor improvements and debugging. 
1.2.10.0 | 2016-01-23 | Added ENCODING keyword to IMPORT metacommand. Added TIMER metacommand and $TIMER system variable.
1.2.8.2  | 2016-01-21 | Fixed extra quoting in drop table methodFixed str coercion in TXT export.
1.2.8.0  | 2016-01-11 | Suppressed column headers when EXPORTing to CSV and TSV with APPEND.  Eliminated %H%M pattern to match time values in IMPORTed data.
1.2.7.1  | 2016-01-03 | Modified import of integers to Postgres; added the AUTOCOMMIT metacommand and modified the BATCH metacommand; changed to explicitly roll back any uncommitted changes on exit; miscellaneous debugging.
1.2.4.6  | 2015-12-19 | Modified quoting of column names for the COPY and IMPORT metacommands.
1.2.4.5  | 2015-12-17 | Fixed asterisks in PROMPT ENTER_SUB.
1.2.4.4  | 2015-12-14 | Fixed regexes for quoted filenames.
1.2.4.3  | 2015-12-13 | Fixed -y option display; fixed parsing of WRITE CREATE_TABLE comment option; fixed parsing of backslashes in substitution strings on Windows.
1.2.4.0  | 2015-11-21 | Added connections to PostgreSQL, SQL Server,  MySQL, MariaDB, SQLite, and Firebird.  Added numerous metacommands and conditional tests. Added reading of configuration files.
0.4.4.0  | 2010-06-20 | Added INCLUDE, WRITE, EXPORT, SUB, EXECUTE, HALT, and IF (HASROWS, SQL_ERROR) metacommands.
0.3.1.0  | 2008-12-19 | Executes SQL against Access, captures output of the last statement.



Copyright and License
================================

Copyright (c) 2007, 2008, 2009, 2014, 2015, 2016, 2017 R.Dreas Nielsen

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. The GNU General Public License is available at
http://www.gnu.org/licenses/.
