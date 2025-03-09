# SQL Current

SQL Current is a database migrations tool with the following properties:
* Everything is driven by DDL or DML scripts (SQL or otherwise) that you write.
* It's open-source and totally free to use for any purpose.

## Motivation

I've never found a perfect migrations tool made for database administrators.  Everything seems to be code-driven, script-generating, tied to an ORM, expensive, or confusing to use.  So DBAs just don't use anything.  But that doesn't solve any problem because it's still difficult and time-consuming to write and structure schema change scripts.

It doesn't have to be that way.  Let's say we wanted to update our QA environment databases.  What if we could just write this:

	update databases to version 1.0.13.1 where environment = 'qa';

If you want something like this, then this is the tool for you.  SQL Current is a database migrations scripting engine that lets you manage the changes in multiple databases across several servers using a SQL-like language.

## Summary

SQL Current is a database migrations tool.  To perform a migration (a change to the database schema) you do the following:
* Describe your database topology by defining servers and databases.
* Define your versions by binding them to your SQL change scripts.  You write the check, apply and revert scripts.

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
