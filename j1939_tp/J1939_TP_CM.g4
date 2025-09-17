grammar J1939_TP_CM;

tp_cm_rts
    : controlByte totalMessageSize totalNumPackets maxPacketsPerCTS pgn EOF
    ;

controlByte       : '10' ;           // RTS control byte
totalMessageSize  : UINT8 UINT8 ;     // 2 bytes
totalNumPackets   : UINT8 ;           // 1 byte
maxPacketsPerCTS  : UINT8 ;           // 1 byte
pgn               : UINT8 UINT8 UINT8 ; // 3 bytes

// Lexer rules
UINT8  : [0-9A-F] [0-9A-F] ;         // Always exactly two hex digits
WS     : [ \t\r\n]+ -> skip ;        // Skip whitespace