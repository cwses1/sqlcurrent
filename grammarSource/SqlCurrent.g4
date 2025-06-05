grammar SqlCurrent;

LINE_COMMENT: '//' ~( '\n'|'\r' )* '\r'? '\n' -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
WS: [ \t\n\r]+ -> skip;
INT_LITERAL: [0-9]+;
SYMBOL_ID: [_a-zA-Z][_a-zA-Z0-9]+;
STRING_LITERAL: '\'' ([ _a-zA-Z0-9] | '.' | ':' | '=' | '$' | '{' | '}' | ';' | '/' | '%' | '?' | '^' | '*' | '@')* '\'';
VERSION_ID: [0-9]+ '.' [0-9]+ '.' [0-9]+;

sqlCurrentScript: statement+;

statement: serverStatement
	| databaseStatement
	| versionStatement
	| createDatabaseStatement
	| solutionStatement
	| branchStatement
	| environmentStatement
	| createDatabaseListStatement
	| updateDatabaseStatement
	| updateDatabaseListStatement
	| selectDatabaseListStatement
	| revertDatabaseListStatement
	| checkDatabaseListStatement
	| revertDatabaseStatement
	| configurationStatement
	| applyConfigurationToDatabaseStatement
	| applyConfigurationToDatabaseListStatement
	| printSymbolsStatement
	| checkDatabaseStatement
	| resetDatabaseStatement
	;

serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
serverPropList: (serverProp ';')+;
serverProp: (SYMBOL_ID | 'solution' | 'environment' | 'branch') ':' expr;

databaseStatement: 'database' SYMBOL_ID '{' databasePropList '}';
databasePropList: (databaseProp ';')+;
databaseProp: (SYMBOL_ID | 'solution' | 'branch' | 'server' | 'create' | 'environment' | 'version' | 'check' | 'reset') ':' expr;

expr: STRING_LITERAL | SYMBOL_ID | VERSION_ID;

versionStatement: 'version' VERSION_ID ('in'? 'branch' expr)? '{' versionPropList '}';
versionPropList: (versionProp ';')+;
versionProp: (SYMBOL_ID | 'branch' | 'revert' | 'check' | 'apply' | 'precheck') ':' expr;

createDatabaseStatement: 'create' 'database'? SYMBOL_ID ';';

solutionStatement: 'solution' SYMBOL_ID '{' solutionPropList '}';
solutionPropList: (solutionProp ';')+;
solutionProp: SYMBOL_ID ':' expr;

branchStatement: 'branch' SYMBOL_ID '{' branchPropList '}';
branchPropList: (branchProp ';')+;
branchProp: (SYMBOL_ID | 'solution' | 'create' | 'version' | 'reset' | 'check') ':' expr;

environmentStatement: 'environment' SYMBOL_ID '{' environmentPropList '}';
environmentPropList: (environmentProp ';')+;
environmentProp: (SYMBOL_ID | 'solution') ':' expr;

createDatabaseListStatement: 'create' 'databases' whereClause? orderByClause? ';';

whereClause: 'where' whereExpr;

whereExpr: ('any' | 'every')? (SYMBOL_ID | 'solution' | 'branch' | 'environment' | 'server') ('=' | '!=' | 'not'? 'in' | 'not'? 'like' | 'not'? 'matches') (simpleWhereExprList | simpleWhereExpr | whereExpr) (('and' | 'or') whereExpr)?
	| '(' whereExpr ')' (('and' | 'or') whereExpr)?;

simpleWhereExpr: SYMBOL_ID | STRING_LITERAL;

simpleWhereExprList: '(' ')'
	| '(' simpleWhereExpr (',' simpleWhereExpr)* ')';

orderByClause: 'order' 'by' orderBySegment (',' orderBySegment)?;
orderBySegment: SYMBOL_ID ('asc' | 'descending')?;

updateDatabaseStatement: 'update' 'database'? SYMBOL_ID toVersionClause? ';';
toVersionClause: 'to' 'version'? VERSION_ID;

updateDatabaseListStatement: 'update' 'databases' toVersionClause? whereClause? orderByClause? ';';
selectDatabaseListStatement: 'select' 'databases' whereClause? orderByClause? ';';
revertDatabaseListStatement: 'revert' 'databases' toVersionClause whereClause? orderByClause? ';';
checkDatabaseListStatement: 'check' 'databases' whereClause? orderByClause? ';';
revertDatabaseStatement: 'revert' 'database'? SYMBOL_ID toVersionClause ';';
checkDatabaseStatement: 'check' 'database'? SYMBOL_ID ('version' VERSION_ID)? ';';
resetDatabaseStatement: 'reset' 'database'? SYMBOL_ID ';';

configurationStatement: 'configuration' SYMBOL_ID 'in' 'branch' expr? '{' configurationPropList '}';
configurationPropList: (configurationProp ';')+;
configurationProp: (SYMBOL_ID | 'environment' | 'version' | 'apply' | 'precheck' | 'check' | 'revert') ':' expr;

applyConfigurationToDatabaseStatement: 'apply' 'configuration'? SYMBOL_ID 'to' 'database'? SYMBOL_ID ';';
applyConfigurationToDatabaseListStatement: 'apply' 'configuration'? SYMBOL_ID 'to' 'databases' whereClause? orderByClause? ';';

printSymbolsStatement: 'print' 'symbols' ';';
