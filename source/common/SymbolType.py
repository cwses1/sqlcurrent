"""
This is used for symbol types in the symbol table but also for general expression types.
"""
class SymbolType ():
	NotAssigned = 0
	String = 1
	Server = 2
	Database = 3
	DatabaseServerType = 4
	Solution = 5
	Branch = 6
	Environment = 7
	ReferenceToSymbol = 8
	List = 9
	Version = 10 # VERSION TYPE
	Int32 = 11
	PropertyName = 12
	VersionNumber = 13 # JUST THE VERSION NUMBER '1.2.1' STORED AS A STRING
	Configuration = 14
