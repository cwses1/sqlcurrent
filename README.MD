# SQL Current

## Motivation

I've never found a good, easy-to-use database migrations tool that is made for a hardcore database administrator.  Everything seems to be code-driven, expensive, or confusing to use.

It's difficult and time-consuming to write and structure schema change scripts.

But it doesn't have to be that way.  What if we could update our QA databases just by writing this:

	update databases
	to version 1.0.0.0
	where environment = 'qa';

If you want something like this, then this is the tool for you.  This is a database migrations scripting engine that lets you manage the changes in multiple databases across several servers using a SQL-like language.

## Summary

This is a database migrations system.  To perform a migration (a change to the database schema) you do the following:
* Describe your database topology by defining servers and databases.
* Define your versions by binding them to your SQL change scripts.  You write the check, apply and revert scripts.
* 


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
