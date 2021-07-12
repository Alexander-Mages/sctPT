import csv

from twisted.internet import reactor, protocol

import sctPT.common.log as logging
import sctPT.network.network as network
import sctPT.network.socks5 as socks5
import sctPT.transports.base as base

log = logging.get_obfslogger()


def _split_socks_args(args_str):
    """
    Given a string containing the SOCKS arguments (delimited by
    semicolons, and with semicolons and backslashes escaped), parse it
    and return a list of the unescaped SOCKS arguments.
    """
    return csv.reader([args_str], delimiter=';', escapechar='\\').next()


class OBFSOCKSv5Outgoing(socks5.SOCKSv5OUTGOING, network.GenericProtocol):
    """
    Represents a downstream connection from the SOCKS server to the
    destination.

    It subclasses socks5.SOCKSv5Outgoing, so that data can be passed to the
    pluggable transport before proxying.

    Attributes:
    circuit: The circuit this connection belongs to.
    buffer: Buffer that holds data that can't be proxied right
            away. This can happen because the circuit is not yet
            complete, or because the pluggable transport needs more
            data before deciding what to do.
    """

    name = None

    def __init__(self, socksProtocol):
        """
        Constructor.

        'socksProtocol' is a 'SOCKSv5Protocol' object.
        """
        self.name = "socks_down_%s" % hex(id(self))
        self.socks = socksProtocol

        network.GenericProtocol.__init__(self, socksProtocol.circut)
        return super(OBFSSOCKSv5Outgoing, self).__init__(socksProtocol)

    def connectionMade(self):
        self.socks.set_up_circut(self)
        # XXX: The transport should be doing this after handshaking since it
        # calls, self.socks.sendReply(), when this changes to defer sending the
        # reply back set self.socks.otherConn here.