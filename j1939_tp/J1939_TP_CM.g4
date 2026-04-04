grammar J1939_TP_CM;

// ==========================================================
// TP_CM_RTS (Control Byte = 0x10)
// ==========================================================

// Byte 0 : controlByte (rts)
// Byte 1-2 : totalMessageSize
// Byte 3 : totalNumPackets
// Byte 4 : maxPacketsPerCTS
// Byte 5-7 : pgn

tp_cm_rts
    : controlByte_rts totalMessageSize totalNumPackets maxPacketsPerCTS pgn EOF
    ;

controlByte_rts
    : '10'
    ;

// ==========================================================
// TP_CM_CTS (Control Byte = 0x11)
// ==========================================================

// Byte 0 : controlByte (cts)
// Byte 1 : numPackets
// Byte 2 : nextPacket
// Byte 3-4 : reserved
// Byte 5-7 : pgn

tp_cm_cts
    : controlByte_cts numPackets nextPacket reserved pgn EOF
    ;

controlByte_cts
    : '11'
    ;

// ==========================================================
// Field Definitions
// ==========================================================

totalMessageSize
    : UINT8 UINT8
    ;

totalNumPackets
    : UINT8
    ;

maxPacketsPerCTS
    : UINT8
    ;

numPackets
    : UINT8
    ;

nextPacket
    : UINT8
    ;

reserved
    : UINT8 UINT8
    ;

pgn
    : UINT8 UINT8 UINT8
    ;

// ==========================================================
// Lexer Rules (Hex Byte Input)
// ==========================================================

UINT8
    : [0-9A-F] [0-9A-F]
    ;

// Allow spaces between bytes
WS
    : [ \t\r\n]+ -> skip
    ;