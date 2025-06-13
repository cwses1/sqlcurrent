# SQL Current
SQL Current is database migrations scripting engine written in Python.  It works with any database that has a Python driver.

It has its own language called **Current Script**.  You use Current Script to define your database topology (servers, databases, branches, environments, versions, configurations) and execute commands against the topology (create, update, revert, check, apply configuration, reset etc.) so you can manage changes to your entire database infrastructure easily.

Current Script looks like a combination of CSS and SQL.  Here's an example:

	database alpha
	{
		driver: 'postgres';
		connString: 'host=127.0.0.1 port=5432 dbname=alpha user=postgres password=postgres';
		create: './create.sql';
	}

	database zappa
	{
		driver: 'postgres';
		connString: 'host=127.0.0.1 port=5432 dbname=zappa user=postgres password=postgres';
		create: './create.sql';
	}

	version 1.0.1
	{
		apply: './create_new_table.sql';
	}

	version 1.1.0
	{
		apply: './create_another_table.sql';
	}

	//
	// THESE ARE COMMENTS.  THIS IS THE PART OF CURRENT SCRIPT THAT LOOKS LIKE SQL.  YOU CAN ALSO USE /* */ FOR COMMENTS.
	//
	create database alpha;
	create database zappa;
	update databases to version 1.1.0 where id in (alpha, zappa);
	select databases;

SQL Current is designed to solve everything from the simplest to the most difficult database setup, versioning, and migration problems that dadta and software teams face in the industry today.

SQL Current is currently in an experiemental alpha stage.  The following databases have been tested against it:
* PostgreSQL
* SQL Server

## Getting Started

One of the simplest, shortest scripts you can write is this:

	database mydb
	{
		driver: 'postgres';
		connString: 'host=127.0.0.1 port=5432 dbname=mydb user=postgres password=postgres';
		create: './create.sql';
	}

	create database mydb;

The above script defines a database, creates that database, and keeps track of that fact in an **update tracking file**.  This is how you would run the script from the command line:

	> sqlcurrent script.txt

If the script is successful you would get a message similar to this:

	mydb: Database created with version '1.0.0'.

If you ran the script twice in a row you would get this error:

	mydb: This database already exists.

SQL Current will not attempt to create a database that already exists.  Versions always start at 1.0.0.

## Setup

### Python

SQL Current is written in Python.  You will need to get Python.

https://www.python.org

### ANTLR Python Runtime

	pip install antlr4-python3-runtime

### Python Database Drivers

	pip install psycopg
	pip install pymssql

## Usage

	./sqlcurrent script.txt

## Script Breakdown

Let's go through the script in greater detail:

	database mydb
	{
		driver: 'postgres';
		connString: 'host=127.0.0.1 port=5432 dbname=mydb user=postgres password=postgres';
		create: './create.sql';
	}

	create mydb;

1. We *define* a database `mydb` with the following properties:
	* `driver`: The type of database we are connecting to.
	* `connString`: The connection details.
	* `create`: The path to the create script.
1. `create mydb;` creates the database by connecting to `mydb` and executes the create script `./create.sql` against it.
1. An update tracking file is created at `./sqlcurrent_updatetracking/default/mydb.txt` to track the version of this database.  The version defaults to 1.0.0.

## Motivation

I've never found a perfect migrations tool made for database administrators.  Everything seems to be code-driven, script-generating, tied to an ORM, expensive, or confusing to use.  So DBAs just don't use anything.  But that doesn't solve any problem because it's still difficult and time-consuming to write and structure schema change scripts.

It doesn't have to be that way.  Let's say we wanted a developer to set up his or her local environment.  What if we could write this:

	create and update database ecommercedb;

or if a DBA wanted to update only the QA environment databases to a specific version.  What if we could just write this:

	update databases to version 1.0.13.1 where environment = qa;

If you want to work with databases this way, then this is the tool for you.  SQL Current is a database migrations scripting engine that lets you manage the changes in multiple databases across several servers using a SQL-like language.

## Use Cases

* Developer setting up a local environment.
* Updating specific environments.
* Topology database and customer data scenario.
* Operational database and analytical database scenario.
* Some applications use multiple databases for different purposes, these are called branches.

## Summary

SQL Current is a database migrations tool.  To perform a migration (a change to the database schema) you do the following:
* Describe your database topology by defining servers and databases.
* Define your versions by binding them to your SQL change scripts.  You write the check, apply and revert scripts.


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

## Other Database Migration Tools
Here are some other database migration tools to consider.

### DbUp

https://dbup.readthedocs.io/en/latest/

For SQL databases.  The strategy this product takes is you build a console application using .NET.  It has a pretty good philosophy where the developer assumes that change scripts are the correct way to go (he's right).  It's been around for several years, and I've seen this DbUp used successfully in a .NET shop before.  However, you are bound to .NET, so this might not be for you if you are not a .NET developer.

### Goose

https://github.com/pressly/goose

Goose is pretty cool.  It's powerful, terse, and is my favorite of the group.  However, it only supports one database at a time via .env files or environment variables, and you must follow its migration file rules.  It's written in golang, but you won't be tied to the golang platform unless you want to create embedded migrations.  I've seen this used successfully before.

### Liquibase

https://www.liquibase.com

This is a full system that can do a lot of things, but it's complex and half of the documentation pushes you to buy their Pro version.  It's powered by Java.

### alembic

https://github.com/sqlalchemy/alembic

Database migrations for SQLAlchemy.  Migration scripts are written in Python.

### migrate

https://github.com/golang-migrate/migrate

### Visual Studio Database Edition

Various reviews on this.

### Red Gate SQL Compare

This is for schema comparisons and can be used in a very limited fashion in a database migrations context.  The way you'd have to make this work is have a reference database, and apply the diffs from the source database to the target database.
