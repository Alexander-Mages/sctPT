import asyncio
import obfsproxy.network.buffer as buffer
import socket
import sctp
import obfsproxy.network.network.circuit as circuit


# library is for python3, only barrier to switching is pyptlib

#asyncio has an api that is supposedly faster than working directly with sockets, but working with sockets directly is an option
#asyncio has methods for socket operations that work asyncrously (too lazy to open google for spelling)


class B64SCTPSocket:
    # addr is an object with attributes for host and port

    def __init__(self):
        self.sctpsock = sctp.sctpsocket_tcp(socket.AF_INET)

    def connect(self, addr):
        sctpsock.connect(addr.host, addr.port)
        print("Socket Connection successfully established to " + addr.host + " on port " + addr.port)


    def createconnectionserver(addr):
        sctpsockserv = sctp.sctpsocket_tcp(socket.AF_INET)
        sctpsockserv.bind((socket.gethostname(), addr.port))
        sctpsockserv.listen()

    async def b64datatransportclientsend(data):
        sent = 0
        result = base64.b64encode(data.read())
        sentbool = self.sock.send(result[sent:])
        if sent == 0:
            raise RuntimeError("Could not send over socket")
        sent = 0

    async def b64datatransportclientrecieve(data):
        result = base64.base64decode(data.read())
        #send result over socks to tor
        #theoretically this, but im not sure how to implement this without the buffer/twisted
        self.circuit.upstream.write(decoded_data)




asyncio.run(reactor())

