from __future__ import absolute_import
import client
import sctPT.network.launch_transport as launch_transport
import sctPT.transports.transports as transports
import sctPT.common.log as logging
import sctPT.common.transport_config as transport_config
from pyptlib.client import ClientTransportPlugin
from pyptlib.config import EnvError

import pprint

#add logger support, take obfsproxy example
log = logging.get_logger

def managed_client(addr, socksVersion, socksPort):
    client = pyptlib.client
    should_start_threading = False

    sctpaddrport = (addr)
    socksaddrport = (("localhost", socksPort))
    socksversion = socksVersion
#
#GET TRANSPORT INFO FROM TOR
#
    try:
        config_info = client.init(["sctPT"])
    except EnvError as err:
        log.warning("pyptlib could not bootstrap (%s)." % err)
        return
    log.debug("data from pyptlib:\n'%s'", pprint.pformat(client.getDebugData()))
#
#CONFIGURE TRANSPORTS
#
    #figure out where to put state location, it is provided inside of info
    if 'sctPT' in config_info['transports']:
        try:
            #you might want to pass the config stuff, revisit.
            transport = network.ClientNetwork
            try:
                transport.launchTransport(socksaddrport, sctpaddrport, socksversion)
            except error.ProxyError as e:
                error_msg = "Socks Version not supported, attempting to launch transport using other rev. (5/4)"
                log.warning(error_msg)
                try:
                    if socksversion == 5:
                        transport.launchTransport(socksaddrport, sctpaddrport, 4)
                    elif socksversion == 4:
                        transport.launchTransport(socksaddrport, sctpaddrport, 5)
                except error.ProxyError as e:
                    error_msg = "PySocks Error: (%s:%s) for sctPT (%s)" % \
                                (e.interface, e.port, e.socketError[1])
                    log.warning(error_msg)
                    client.reportFailure('sctPT', error_msg)
        except error.CannotListenError as e:
            error_msg = "Couldnt start sockets (%s:%s) for sctPT (%s)." % \
                            (e.interface, e.port, e.socketError[1])
            log.warning(error_msg)
            client.reportFailure('sctPT', error_msg)
#
#REPORT SUCCESS TO PYPTLIB AND TOR
#
    should_start_threading = True
    log.debug("Successfully launched sctPT. Socks listening at: '%s'" % (log.safe_addr_str(str(addrport))))
    log.debug("SCTP listening at: '%'" % (socksaddrport))
    client.reportSuccess('sctPT', socksversion, (socksaddrport), None, None)
    client.ReportEnd()
    #tells pyptlib everything is finished, wihch then tells tor to start pushing traffic

    if should_start_threading:
        #args might be suitable to have here
        isActiveBool = transport.startProxying()
        if isActiveBool:
            log.info("Data proxying correctly")
    else:
        log.info("No transports launched.")