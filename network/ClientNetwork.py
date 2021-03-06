import time
import socket
import socks
import transport.ClientTransport
import logging
#threading but with better performance, allows multiple cores to be used, syntax is a little odder, but performance is important
from multiprocessing import Process

class ClientNetwork:

    def launchTransport(self, socksaddrport, sctpaddrport, socksVersion):
        self.logger = logging.getLogger(__name__)

        self.logger.debug("launching socks proxy to communicate with the tor browser...")
        sockssock = socks.socksocket()
        #socksVersion = "SOCKS5"  # this will need to be defined somewhere else, i.e. pyptlib

        if socksVersion == 5:
            sockssock.set_proxy(socks.SOCKS5, "127.0.0.1")
        elif socksVersion == 5:
            sockssock.set_proxy(socks.SOCKS4, "127.0.0.1")  # subsequent argument is port if desired
        else:
                self.logger.error("error")

        sockssock.bind(socksaddrport)
        sockssock.listen(25)
        self.logger.debug("socks listening on " + str(socksaddrport))

        self.logger.debug("launching sctp socket...")
        self.sctpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)


        self.logger.debug("attempting to connect to Tor bridge and Tor Browser")
        self.sockssocket, address = sockssock.accept()
        self.logger.debug("socks connection accepted from tor browser at" + str(address))
        err = self.sctpsocket.connect_ex(sctpaddrport)
        self.logger.debug("sctp connected to bridge at" + str(sctpaddrport))


    def startProxying(self):
        #final method, does not terminate until program is completed
        self.logger.debug("Starting Processes for sockets")

        self.runningProcesses = []

        clienttransport = transport.ClientTransport.clientTransport()
        clienttransport.__init__()
        upstreamTransport = Process(target=clienttransport.proxyUpstream, args=(self.sctpsocket, self.sockssocket))
        downstreamTransport = Process(target=clienttransport.proxyDownstream, args=(self.sockssocket, self.sctpsocket))

        downstreamTransport.start()
        upstreamTransport.start()

        self.runningProcesses.append(downstreamTransport)
        self.runningProcesses.append(upstreamTransport)

        return self.isRunning()


    def isRunning(self):
        for t in self.runningProcesses:
            if t.is_alive():
                continue
            elif not t.is_alive():
                return False
        return True

