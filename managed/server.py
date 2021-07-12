from twisted.internet import reactor, error

from pyptlib.server import ServerTransportPlugin
from pyptlib.config import EnvError

import sctPT.transports.transports as transports
import sctPT.network.launch_transport as launch_transport
import sctPT.common.log as logging
import sctPT.common.transport_config as transport_config

import pprint

log = logging.get_obfslogger()

def do_managed_server():

    should_start_event_loop = False

#
#GET TRANSPORT INFO FROM TOR
#

#init is the method to ask tor for info, server init returns a lot more than client

    ptserver = ServerTransportPlugin()
    try:
        ptserver.init(["SCTP", "Dummy"])
        #ptserver.init(transports.transports.keys())
        #leaving here for searching purposes, second implementation is in obfsproxy
    except EnvError, err:
        log.warning("server managed proxy protocol failed (%s)." % err)
        return

    log.debug ("pyptlib gave us the following data:\n'%s'", pprint.pformat(ptserver.getDebugData()))


#
# CONFIGURE TRANSPORTS
#


    ext_orport = ptserver.config.getExtendedOrPort()
    authcookie = ptserver.config.getAuthCookieFile()
    orport = ptserver.config.getORPort()
    #^methods are part of pyptlib
    server_transport_options = ptserver.config.getServerTransportOptions()
    #this method is defined in transport_config.py^

    for transport, transport_bindaddr in ptserver.getBindAddresses().items():
        #simmilar to client.py. Configures all transports, but also configures the all transports on every address

        pt_config = transport_config.TransportConfig()
        pt_config.setStateLocation(ptserver.config.getStateLocation())
        if ext_orport:
            pt_config.setListenerMode("ext_server")
        else:
            pt_config.setListenerMode("server")
        pt_config.setObfsproxyMode("managed")

        transport_options = ""
        if server_transport_options and transport in server_transport_options:
            transport_options = server_transport_options[transport]
            pt_config.setServerTransportOptions(transport_options)


        transport_class = transports.get_transport_class(transport, 'server')
        transport_class.setup(pt_config)

#
#LAUNCH TRANSPORTS
#
        try:
            if ext_orport:
                addrport = launch_transport.launch_transport_listener(transport,
                                                                      transport_bindaddr,
                                                                      'ext_server',
                                                                      ext_orport,
                                                                      pt_config,
                                                                      ext_or_cookie_file=authcookie)
            else:
                addrport = launch_transport.launch_transport_listener(transport,
                                                                      transport_bindaddr,
                                                                      'server',
                                                                      orport,
                                                                      pt_config)
        except transports.TransportNotFound:
            log.warning("Could not find transport '%s'" % transport)
            ptserver.reportMethodError(transport, "Could not find transport.")
            continue
        except error.CannotListenError, e:
            error_msg = "Could not set up listener (%s:%s) for '%s' (%s)." % \
                        (e.interface, e.port, transport, e.socketError[1])
            log.warning(error_msg)
            ptserver.reportMethodError(transport, error_msg)
            continue
        #report errors to pyptlib

        should_start_event_loop = True
        #still no idea^

        extra_log = ""
        if transport_options:
            extra_log = " (server transport options: '%s')" % str(transport_options)
        log.debug("Successfully launched '%s' at '%s" % (transport, log.safe_addr_str(str(addrport)), extra_log))
        #print out transport options for redundancy

        # Invoke the transport-specific get_public_server_options()
        # method to potentially filter the server transport options
        # that should be passed on to Tor and eventually to BridgeDB.
        public_options_dict = transport_class.get_pubhlic_server_options(transport_options)
        public_options_str = None
        # defined in base.py^

        #if the transport filtered its options:
        if public_options_dict:
            optlist []
            for k, v in public_options_dict.items():
                optlist.append("%s=%s" % (k,v))
            public_options_str = ",".join(optlist)

            log.debug("do_managed_server: sending only public_options to tor: %s" % public_options_str)
        #^ allows filtering of options being sent to tor, this allows a specific transport to change options

        # report success for this particular transport
        # if public_options_str is none, then all of the
        # transport options from ptserver are used instead
        ptserver.reportMethodSuccess(transport, addrport, public_options_str)

    ptserver.reportMethodsEnd()
    #report success after all transports have been launched on all addresses

    if should_start_event_loop:
        log.info("starting event loop")
        reactor.run()
        #reactor is a function of twisted
        #it looks simmilar to answering machine but infinitely more configurable
    else:
        log.info("No transports launched. Nothing to do")
