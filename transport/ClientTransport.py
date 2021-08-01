import logging
from transport.ClientDataTransform import DataTransform

class clientTransport:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

#source is sctp traffic from bridge, destination is socks/tor browser
    def proxyUpstream(self, source, dest):
        while True:
            #4096 is arbitrary
            data = source.recv(4096)
            if data == '':
                break
            datatransform = DataTransform()
            finaldata = datatransform.unobfuscateData(data)
            dest.sendall(finaldata)
            self.logger.debug("data sent upstream")


    #source is socks/tor browser, destination is tor bridge
    def proxyDownstream(self, source, dest):
        while True:
            data = source.recv(4096)
            if data == '':
                break
            datatransform = DataTransform()
            finaldata = datatransform.obfuscateData(data)
            dest.sendall(finaldata)
            self.logger.debug("data sent downstream")