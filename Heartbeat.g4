grammar Heartbeat;

heartbeat: counter status checksum EOF;

counter: INT;
status: INT;
checksum: INT;

INT: [0-9]+;
WS: [ \t\r\n]+ -> skip;
