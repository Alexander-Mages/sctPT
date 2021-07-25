import logging
from transport.ServerDataTransform import DataTransform
class clientTransport:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.datatransform = DataTransform()


#source is sctp traffic from tor, destination is tor network tcp
    def reverseProxy(self, source, dest):
        while True:
            #numbers larger than 4096 work
            data = source.recv(4096)
            if data == '':
                break
            finaldata = self.datatransform.unobfuscateData(data)
            dest.sendall(finaldata)
            self.logger.debug("data sent to tor node")