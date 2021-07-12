import sctPT.transports.dummy as dummy
import sctPT.transports.b64 as b64
import sctPT.transports.sctPT as sctPT


transports = { 'dummy' : {'base': dummy.DummyTransport, 'client' : dummy.DummyClient, 'server' : dummy.DummyServer },
               'b64'   : {'base': b64.B64Transport, 'client' : b64.B64Client, 'server' : b64.B64Server },
               'sctPT' : {'base': sctPT.sctPTTransport, 'client' : sctPT.sctPTClient, 'server' : sctPT.sctPTServer } }

def get_transport_class(name, role):
    # Rewrite equivalent roles.
    if role == 'socks':
        role = 'client'
    elif role == 'ext_server':
        role = 'server'

    # Find the correct class
    if (name in transports) and (role in transports[name]):
        return transports[name][role]
    else:
        raise TransportNotFound

class TransportNotFound(Exception): pass

