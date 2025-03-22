# SQL Current

SQL Current is a database migrations scripting engine.  It works with any database that has a Python driver.

# Brief Tutorial

Here is a simple SQL Current script:

	database mydb
	{
		driver: 'postgres';
		connString: 'host=127.0.0.1 port=5432 dbname=mydb user=postgres password=postgres';
		create: 'create.sql';
	}

	create mydb;

Run the script:

	> cd /home/repos/sqlcurrent
	> sqlcurrent script.txt

What this script does:

1. The database variable "mydb" is created with the following properties:
	* driver - the type of database server we are connecting to (such as PostgreSQL, MySQL, SQL Server, MongoDB, InfluxDB).  This determines the Python driver / adapter library to use.
	* connString - the connection string or DSN of the database
	* create - the path to the create script.
2. The 'create.sql' script is run.  Whatever you did in the script happens.
3. An update tracking file is created to track the version of this database.  Since no version was specified in the script, SQL Current uses version 1.0.0.

Try running the script again.  You should get this error:

	mydb ERROR: This database already exists.

SQL Current will not attempt to create a database that already exists.

## Motivation

I've never found a perfect migrations tool made for database administrators.  Everything seems to be code-driven, script-generating, tied to an ORM, expensive, or confusing to use.  So DBAs just don't use anything.  But that doesn't solve any problem because it's still difficult and time-consuming to write and structure schema change scripts.

It doesn't have to be that way.  Let's say we wanted a developer to set up his or her local environment.  What if we could write this:

	create and update database ecommercedb;

or if a DBA wanted to update only the QA environment databases to a specific version.  What if we could just write this:

	update databases to version 1.0.13.1 where environment = qa;

If you want to work with databases this way, then this is the tool for you.  SQL Current is a database migrations scripting engine that lets you manage the changes in multiple databases across several servers using a SQL-like language.

## Summary

SQL Current is a database migrations tool.  To perform a migration (a change to the database schema) you do the following:
* Describe your database topology by defining servers and databases.
* Define your versions by binding them to your SQL change scripts.  You write the check, apply and revert scripts.

## Use Cases

* Developer setting up a local environment.
* Updating specific environments.
* Topology database and customer data scenario.
* Operational database and analytical database scenario.
* Some applications use multiple databases for different purposes, these are called branches.

## Setup

### Python

The interpreter is written in Python.  You will need to get Python.

### ANTLR Python Runtime

	pip install antlr4-python3-runtime

### Java

If you want to compile the grammar, you will need Java.

## Usage

	./sqlcurrent script.txt

## Scripting Language Guide

### Server Definition

A server is a first-class construct in SQL Current.  A server identifies a host on your network.  The server itself may host any number of database services in your topology, which is turn may host any number of physical databases.  Define a server as follows:

	server nexus
	{
		host: 'nexus.sqlcurrent.com';
		environment: 'dev';
		tag: 'env_dev';
	}

Note that you have the ability to apply arbitrary string tags to servers.

### Database Definition

A database is a single physical container of your data.  You must tell SQLCurrent the type of database (e.g. PostgreSQL, MySQL, SQL Server) and the connetion string for it.  Similar to a server, you can apply arbitrary string tags to a database.  Here is an example of a database definition:

	database ecommerce_1
	{
		server: nexus;
		type: 'postgres';
		connString: 'Server=${nexus};database=atomlab';
		environment: 'dev';
		tag: 'env_dev';
	} 

### Database Group Definition

## Other Tools
* Goose https://github.com/pressly/goose
* DbUp https://dbup.readthedocs.io/en/latest/
* Liquibase https://www.liquibase.com - Fake open source tool hidden behind a bunch of pricing pages.  Requires getting Java and sued by Oracle.
* https://github.com/sqlalchemy/alembic
* https://github.com/golang-migrate/migrate
