import logging
from transport.ServerDataTransform import DataTransform

class serverTransport:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.datatransform = DataTransform()


#source is sctp traffic from tor, destination is tor network tcp
    def toTorNet(self, source, dest):
        while True:
            #numbers larger than 4096 work
            data = source.recv(4096)
            if data == '':
                break
            finaldata = self.datatransform.unobfuscateData(data)
            dest.sendall(finaldata)
            self.logger.debug("data recieved from client, forwarded sent to tor node")

#source is tor network tcp, destination is tor client over sctp
    def reverseProxy(self, source, dest):
        while True:
            data = source.recv(4096)
            if data == '':
                break
            finaldata = self.datatransform.obfuscateData(data)
            dest.sendall(finaldata)
            self.logger.debug("data recieved from tor node, forwarded over sctp to client")