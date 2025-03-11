grammar SqlCurrent;

LINE_COMMENT: '//' ~( '\n'|'\r' )* '\r'? '\n' -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
WS: [ \t\n\r]+ -> skip;
INT_LITERAL: [0-9]+;
SYMBOL_ID: [_a-zA-Z][_a-zA-Z0-9]+;
STRING_LITERAL: '\'' ([ _a-zA-Z0-9] | '.' | ':' | '=' | '$' | '{' | '}' | ';' | '/')* '\'';
VERSION_ID: [0-9]+ '.' [0-9]+ '.' [0-9]+;

sqlCurrentScript: statement+;

statement: serverStatement
	| databaseStatement
	| versionStatement
	| createDatabaseStatement
	| solutionStatement
	| branchStatement
	| environmentStatement;

serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
serverPropList: (serverProp ';')+;
serverProp: (SYMBOL_ID | 'solution' | 'environment' | 'branch') ':' expr;

databaseStatement: 'database' SYMBOL_ID '{' databasePropList '}';
databasePropList: (databaseProp ';')+;
databaseProp: (SYMBOL_ID | 'solution' | 'branch' | 'server' | 'create' | 'environment') ':' expr;

expr: STRING_LITERAL | SYMBOL_ID;

versionStatement: 'version' VERSION_ID ('for' 'branch' expr)? '{' versionPropList '}';
versionPropList: (versionProp ';')+;
versionProp: (SYMBOL_ID | 'branch') ':' expr;

createDatabaseStatement: 'create' 'database'? SYMBOL_ID;

solutionStatement: 'solution' SYMBOL_ID '{' solutionPropList '}';
solutionPropList: (solutionProp ';')+;
solutionProp: SYMBOL_ID ':' expr;

branchStatement: 'branch' SYMBOL_ID '{' branchPropList '}';
branchPropList: (branchProp ';')+;
branchProp: (SYMBOL_ID | 'solution') ':' expr;

environmentStatement: 'environment' SYMBOL_ID '{' environmentPropList '}';
environmentPropList: (environmentProp ';')+;
environmentProp: (SYMBOL_ID | 'solution') ':' expr;
