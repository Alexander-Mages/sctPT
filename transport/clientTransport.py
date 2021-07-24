
import transport.ClientDataTransform
class clientTransport:
#initializing object: clienttransport = ClientNetwork()
#when this is completed, __init__() is run. Beyond that, you have to call the methods in the class
#init should not contain any code here, but methods should be specialized

#source is sctp traffic from bridge, destination is socks/tor browser
    def proxyUpstream(self, source, dest):
        while True:
            data = source.recv(4096)
            if data == '':
                break
            finaldata = transport.ClientDataTransform.unobfuscateData(data)
            dest.sendall(data)

            #spawn concurrent threads


    #source is socks/tor browser, destination is tor bridge
    def proxyDownstream(self, source, dest):
        while True:
            #this buffer size is arbitrary and holds no reasoning, probably want to change if helps performance
            data = source.recv(4096)
            if data == '':
                break
            finaldata = transport.ClientDataTransform.obfuscateData(data)
            dest.sendall(data)