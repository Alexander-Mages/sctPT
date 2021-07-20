from __future__ import absolute_import
import sctPT.network.network as network
import sctPT.transports.transports as transports
import sctPT.network.socks as socks
import sctPT.network.extended_orport as extended_orport

from twisted.internet import reactor

def launch_transport_listener(transport, bindaddr, role, remote_addrport, pt_config, ext_or_cookie_file=None):

     transport_class = transports.get_transport_class(transport, role)
     listen_host = bindaddr[0] if bindaddr else 'localhost'
     listen_port = int(bindaddr[1]) if bindaddr else 0

     if role == 'socks':
         factory = socks.OBFSSOCKSv5Factory(transport_class, pt_config)
     elif role == 'ext_server':
         assert(remote_addrport and ext_or_cookie_file)
         factory = extended_orport.ExtORPortServerFactory(remote_addrport, ext_or_cookie_file, transport, transport_class, pt_config)
     else:
         assert(remote_addrport)
         factory = network.StaticDestinationServerFactory(remote_addrport, role, transport_class, pt_config)

     addrport = reactor.listenTCP(listen_port, factory, interface=listen_host)

     return (addrport.getHost().host, addrport.getHost().port)