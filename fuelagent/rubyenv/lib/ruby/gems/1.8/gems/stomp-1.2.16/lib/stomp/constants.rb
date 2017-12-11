# -*- encoding: utf-8 -*-

module Stomp

  # Client generated frames
  CMD_CONNECT     = "CONNECT"
  CMD_STOMP       = "STOMP"
  CMD_DISCONNECT  = "DISCONNECT"
  CMD_SEND        = "SEND"
  CMD_SUBSCRIBE   = "SUBSCRIBE"
  CMD_UNSUBSCRIBE = "UNSUBSCRIBE"
  CMD_ACK         = "ACK"
  CMD_NACK        = "NACK"
  CMD_BEGIN       = "BEGIN"
  CMD_COMMIT      = "COMMIT"
  CMD_ABORT       = "ABORT"

  # Server generated names
  CMD_CONNECTED = "CONNECTED"
  CMD_MESSAGE   = "MESSAGE"
  CMD_RECEIPT   = "RECEIPT"
  CMD_ERROR     = "ERROR"

  # Protocols
  SPL_10 = "1.0"
  SPL_11 = "1.1"
  SPL_12 = "1.2"

  # Stomp 1.0 and 1.1
  SUPPORTED = [SPL_10, SPL_11, SPL_12]

  # 1.9 Encoding Name
  UTF8 = "UTF-8"
  #
  # Octet 0
  #
  NULL = "\0"
  #
  # New line
  #
  NL = "\n"
  NL_ASCII = 0x0a
  #
  # Line Feed (New Line)
  #
  LF = "\n"
  LF_ASCII = 0x0a
  #
  # New line
  #
  CR = "\r"
  CR_ASCII = 0x0d
  #
  # Back Slash
  #
  BACK_SLASH = "\\"
  BACK_SLASH_ASCII = 0x5c
  #
  # Literal colon
  #
  LITERAL_COLON = ":"
  COLON_ASCII = 0x3a
  #
  # Literal letter c
  #
  LITERAL_C = "c"
  C_ASCII = 0x63
  #
  # Literal letter n
  #
  LITERAL_N = "n"
  N_ASCII = 0x6e
  #
  # Codec from/to values.
  #
  ENCODE_VALUES = [
    "\\\\\\\\", "\\", # encoded, decoded
    "\\" + "n", "\n",
    "\\" + "r", "\r",
    "\\c", ":",
  ]

  #
  DECODE_VALUES = [
    "\\\\", "\\", # encoded, decoded
    "\\" + "n", "\n",
    "\\" + "r", "\r",
    "\\c", ":",
  ]

  # A fairly safe and generally supported ciphers list.
  DEFAULT_CIPHERS = [
    ["DHE-RSA-AES256-SHA", "TLSv1/SSLv3", 256, 256], 
    ["DHE-DSS-AES256-SHA", "TLSv1/SSLv3", 256, 256], 
    ["AES256-SHA", "TLSv1/SSLv3", 256, 256], 
    ["EDH-RSA-DES-CBC3-SHA", "TLSv1/SSLv3", 168, 168], 
    ["EDH-DSS-DES-CBC3-SHA", "TLSv1/SSLv3", 168, 168], 
    ["DES-CBC3-SHA", "TLSv1/SSLv3", 168, 168], 
    ["DHE-RSA-AES128-SHA", "TLSv1/SSLv3", 128, 128], 
    ["DHE-DSS-AES128-SHA", "TLSv1/SSLv3", 128, 128], 
    ["AES128-SHA", "TLSv1/SSLv3", 128, 128], 
    ["RC4-SHA", "TLSv1/SSLv3", 128, 128], 
    ["RC4-MD5", "TLSv1/SSLv3", 128, 128], 
    ["EDH-RSA-DES-CBC-SHA", "TLSv1/SSLv3", 56, 56], 
    ["EDH-DSS-DES-CBC-SHA", "TLSv1/SSLv3", 56, 56],
    ["DES-CBC-SHA", "TLSv1/SSLv3", 56, 56], 
    ["EXP-EDH-RSA-DES-CBC-SHA", "TLSv1/SSLv3", 40, 56], 
    ["EXP-EDH-DSS-DES-CBC-SHA", "TLSv1/SSLv3", 40, 56], 
    ["EXP-DES-CBC-SHA", "TLSv1/SSLv3", 40, 56], 
    ["EXP-RC2-CBC-MD5", "TLSv1/SSLv3", 40, 128], 
    ["EXP-RC4-MD5", "TLSv1/SSLv3", 40, 128],
  ]

  # stomp URL regex pattern, for e.g. login:passcode@host:port or host:port
  URL_REPAT = '((([\w~!@#$%^&*()\-+=.?:<>,.]*\w):([\w~!@#$%^&*()\-+=.?:<>,.]*))?@)?([\w\.\-]+):(\d+)'

  # Failover URL regex, for e.g.
  #failover:(stomp+ssl://login1:passcode1@remotehost1:61612,stomp://login2:passcode2@remotehost2:61613)
  FAILOVER_REGEX = /^failover:(\/\/)?\(stomp(\+ssl)?:\/\/#{URL_REPAT}(,stomp(\+ssl)?:\/\/#{URL_REPAT})*\)(\?(.*))?$/

end # Module Stomp
