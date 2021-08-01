import socket
from multiprocessing import Process
import logging
import transport.ServerTransport

class ServerNetwork:

    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def launchTransport(self, sctpaddrport, tcpaddrport):
        self.logger.debug("launching sctp socket to communicate with client")
        sctpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
        sctpsock.bind(sctpaddrport)
        sctpsock.listen(25)
        self.logger.debug("SCTP socket bound and listening")

        self.logger.debug("launching tcp socket to communicate with the tor network")
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.bind(tcpaddrport)
        tcpsock.listen(25)
        self.logger.debug("tcp socket bound and listening")


        self.logger.debug("accepting connections on both sockets")
        self.sctpsocket, address1 = sctpsock.accept()
        self.logger.debug("sctp connection accepted from tor client at" + str(address1))
        self.tcpsocket, address2 = tcpsock.accept()
        self.logger.debug("tcp connection accepted from node at" + str(address2))

        return address1, address2

    def startProxying(self):
        #final method, does not terminate until program is completed
        self.logger.debug("starting processes for sockets")

        self.runningProcesses = []

        servertransport = transport.ServerTransport.serverTransport()
        servertransport.__init__()
        upstreamTransport = Process(target=servertransport.reverseProxy, args=(self.tcpsocket, self.sctpsocket))
        downstreamTransport = Process(target=servertransport.toTorNet, args=(self.sctpsocket, self.tcpsocket))

        upstreamTransport.start()
        downstreamTransport.start()

        self.runningProcesses.append(upstreamTransport)
        self.runningProcesses.append(downstreamTransport)

        return self.isRunning()

    def isRunning(self):
        for t in self.runningProcesses:
            if t.is_alive():
                continue
            elif not t.is_alive():
                return False
        return True