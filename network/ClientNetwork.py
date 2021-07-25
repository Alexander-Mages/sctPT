import time
import socket
import socks
from threading import Thread
import transport.clientTransport
import logging
#threading but with better performance, allows multiple cores to be used, syntax is a little odder, but performance is important
from multiprocessing import Process

class ClientNetwork():


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
            # add an exception here, might want to look into custom errors
        sockssock.bind(("127.0.0.1", 9050))  # whatever port tor uses for socks
        sockssock.listen(25)

        self.logger.debug("launching sctp socket on port 6000...")
        sctpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
        sctpsock.bind(("0.0.0.0", 6000))
        sctpsock.listen(25)
        self.logger.debug("socket bound and socket listening")

        #BUG
        #sctp must connect first, im not sure exactly how to do this better.
        #maybe threads?
        self.logger.debug("accepting connections on both sockets")
        self.sockssocket, address = sockssock.accept()
        self.logger.debug("socks connection accepted from tor browser at" + str(address))
        self.sctpsocket, address = sctpsock.accept()
        self.logger.debug("sctp connection accepted from bridge at" + str(address))

        # self.sctpsocket = sctpsocket
        # self.sockssocket = sctpsocket

        # CHANGE NAME OF SOCKSSOCKET, IT IS WAY TOO SIMIMLAR TO SOCKSOCKET
        # no idea whether to use multiprocessing, threading, concurrency, or asyncrynosity

        # whichever one of these runs first, is the one that starts

    def startProxying(self):
        #final method, does not terminate until program is completed
        self.logger.debug("Starting Processes for sockets")

        self.runningProcesses = []

        clienttransport = transport.clientTransport.clientTransport()
        clienttransport.__init__()
        upstreamTransport = Thread(target=clienttransport.proxyUpstream, args=(self.sctpsocket, self.sockssocket))
        downstreamTransport = Thread(target=clienttransport.proxyDownstream, args=(self.sockssocket, self.sctpsocket))

        downstreamTransport.start()
        upstreamTransport.start()
        
        # downstreamTransport.join()4
        # upstreamTransport.join()

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
