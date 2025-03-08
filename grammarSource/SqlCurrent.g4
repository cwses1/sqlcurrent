grammar SqlCurrent;

WS: [ \t\n\r]+ -> skip;
INT_LITERAL: [0-9]+;
SYMBOL_ID: [_a-zA-Z0-9]+;
STRING_LITERAL: '\'' ([_a-zA-Z0-9] | '.' | ':' | '=' | '$' | '{' | '}' | ';')* '\'';

sqlCurrentScript: statement+;

statement: serverStatement | databaseStatement;

serverStatement: 'server' SYMBOL_ID '{' serverPropList '}';
serverPropList: (serverProp ';')+;
serverProp: SYMBOL_ID ':' STRING_LITERAL;

databaseStatement: 'database' SYMBOL_ID '{' databasePropList '}';
databasePropList: (databaseProp ';')+;
databaseProp: SYMBOL_ID ':' expr
	| 'server' ':' SYMBOL_ID;

expr: STRING_LITERAL | SYMBOL_ID;
