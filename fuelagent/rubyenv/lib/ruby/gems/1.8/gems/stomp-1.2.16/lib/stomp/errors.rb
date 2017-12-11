# -*- encoding: utf-8 -*-

module Stomp

  # Module level container for Stomp gem error classes.
  module Error

    # InvalidFormat is raised if:
    # * During frame parsing if a malformed frame is detected.
    class InvalidFormat < RuntimeError
      def message
        "Invalid message - invalid format"
      end
    end

    # InvalidServerCommand is raised if:
    # * An invalid STOMP COMMAND is received from the server.
    class InvalidServerCommand < RuntimeError
      def message
        "Invalid command from server"
      end
    end

    # InvalidMessageLength is raised if:
    # * An invalid message length is detected during a frame read.
    class InvalidMessageLength < RuntimeError
      def message
        "Invalid content length received"
      end
    end

    # PacketParsingTimeout is raised if:
    # * A frame read has started, but does not complete in 5 seconds.
    # * Use :parse_timeout connect parameter to override the timeout.
    class PacketParsingTimeout < RuntimeError
      def message
        "Packet parsing timeout"
      end
    end

    # SocketOpenTimeout is raised if:
    # * A timeout occurs during a socket open.
    class SocketOpenTimeout < RuntimeError
      def message
        "Socket open timeout"
      end
    end

    # NoCurrentConnection is raised if:
    # * Any method is called when a current connection does not exist.
    # * And @closed_check is true (the default).
    class NoCurrentConnection < RuntimeError
      def message
        "no current connection exists"
      end
    end

    # MaxReconnectAttempts is raised if:
    # * The maximum number of retries has been reached for a reliable connection.
    class MaxReconnectAttempts < RuntimeError
      def message
        "Maximum number of reconnection attempts reached"
      end
    end

    # DuplicateSubscription is raised if:
    # * A duplicate subscription ID is detected in the current session.
    class DuplicateSubscription < RuntimeError
      def message
        "duplicate subscriptions are disallowed"
      end
    end

    # ProtocolError11p - base class of 1.1 CONNECT errors
    class ProtocolError11p < RuntimeError
      def message
        "STOMP 1.1+ CONNECT error"
      end
    end

    # ProtocolErrorConnect is raised if:
    # * Incomplete Stomp 1.1 headers are detected during a connect.
    class ProtocolErrorConnect < ProtocolError11p
      def message
        "STOMP 1.1+ CONNECT error, missing/incorrect CONNECT headers"
      end
    end

    # UnsupportedProtocolError is raised if:
    # * No supported Stomp protocol levels are detected during a connect.
    class UnsupportedProtocolError < ProtocolError11p
      def message
        "unsupported protocol level(s)"
      end
    end

    # InvalidHeartBeatHeaderError is raised if:
    # * A "heart-beat" header is present, but the values are malformed.
    class InvalidHeartBeatHeaderError < ProtocolError11p
      def message
        "heart-beat header value is malformed"
      end
    end

    # SubscriptionRequiredError is raised if:
    # * No subscription id is specified for a Stomp 1.1 subscribe.
    class SubscriptionRequiredError < RuntimeError
      def message
        "a valid subscription id header is required"
      end
    end

    # UTF8ValidationError is raised if:
    # * Stomp 1.1 headers are not valid UTF8.
    class UTF8ValidationError < RuntimeError
      def message
        "header is invalid UTF8"
      end
    end

    # MessageIDRequiredError is raised if:
    # * No messageid parameter is specified for ACK or NACK.
    class MessageIDRequiredError < RuntimeError
      def message
        "a valid message id is required for ACK/NACK"
      end
    end

    # SSLClientParamsError is raised if:
    # * Incomplete SSLParams are specified for an SSL connect.
    class SSLClientParamsError < RuntimeError
      def message
        "certificate and key files are both required"
      end
    end

    # StompServerError is raised if:
    # * Invalid (nil) data is received from the Stomp server.
    class StompServerError < RuntimeError
      def message
        "Connected, header read is nil, is this really a Stomp Server?"
      end
    end

    # SSLNoKeyFileError is raised if:
    # * A supplied key file does not exist.
    class SSLNoKeyFileError < RuntimeError
      def message
        "client key file does not exist"
      end
    end

    # SSLUnreadableKeyFileError is raised if:
    # * A supplied key file is not readable.
    class SSLUnreadableKeyFileError < RuntimeError
      def message
        "client key file can not be read"
      end
    end

    # SSLNoCertFileError is raised if:
    # * A supplied SSL cert file does not exist.
    class SSLNoCertFileError < RuntimeError
      def message
        "client cert file does not exist"
      end
    end

    # SSLUnreadableCertFileError is raised if:
    # * A supplied SSL cert file is not readable.
    class SSLUnreadableCertFileError < RuntimeError
      def message
        "client cert file can not be read"
      end
    end

    # SSLNoTruststoreFileError is raised if:
    # * A supplied SSL trust store file does not exist.
    class SSLNoTruststoreFileError < RuntimeError
      def message
        "a client truststore file does not exist"
      end
    end

    # SSLUnreadableTruststoreFileError is raised if:
    # * A supplied SSL trust store file is not readable.
    class SSLUnreadableTruststoreFileError < RuntimeError
      def message
        "a client truststore file can not be read"
      end
    end

    # LoggerConnectionError is not raised by the gem.  It may be 
    # raised by client logic in callback logger methods to signal
    # that a connection should not proceed.
    class LoggerConnectionError < RuntimeError
    end

    # NilMessageError is raised if:
    # * Invalid (nil) data is received from the Stomp server in a client's
    # listener thread, and the connection is not reliable.
    class NilMessageError < RuntimeError
      def message
        "Received message is nil, and connection not reliable"
      end
    end

    # MalformedFailoverOptionsError is raised if failover URL
    # options can not be parsed
    class MalformedFailoverOptionsError < RuntimeError
      def message
        "failover options are malformed"
      end
    end

    # ConnectReadTimeout is raised if:
    # * A read for CONNECTED/ERROR is untimely
    class ConnectReadTimeout < RuntimeError
      def message
        "Connect read for CONNECTED/ERROR timeout"
      end
    end

  end # module Error

end # module Stomp

