from __future__ import absolute_import
import pyptlib_python3.pyptlib.client
from pyptlib_python3.pyptlib.config import EnvError
import pprint
import sys
import logging
import network.ClientNetwork


class managedClient:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def managed_client(self, addr, socksVersion, socksPort):
        should_start_threading = False

        sctpaddrport = (addr)
        socksaddrport = (("localhost", socksPort))
        socksversion = socksVersion

    #the below code relies on pyptlib, to enable it, delete lines 60 and 61 and uncomment
    #
    #GET TRANSPORT INFO FROM TOR
    #
        # try:
        #     #config_info = pyptlib_python3.pyptlib.client.init(["sctPT"])
        # except EnvError as err:
        #     logger.warning("pyptlib could not bootstrap (%s)." % err)
        #     return
        # logger.debug("data from pyptlib:\n'%s'", pprint.pformat(pyptlib_python3.pyptlib.client.getDebugData()))
    #
    #CONFIGURE TRANSPORTS
    #
        #figure out where to put state location, it is provided inside of info
        # if 'sctPT' in config_info['transports']:
        #     try:
        #         #you might want to pass the config stuff, revisit.
        #         transport = network.ClientNetwork
        #         try:
        #             transport.launchTransport(socksaddrport, sctpaddrport, socksversion)
        #         except error.ProxyError as e:
        #             error_msg = "Socks Version not supported, attempting to launch transport using other rev. (5/4)"
        #             logger.warning(error_msg)
        #             try:
        #                 if socksversion == 5:
        #                     transport.launchTransport(socksaddrport, sctpaddrport, 4)
        #                 elif socksversion == 4:
        #                     transport.launchTransport(socksaddrport, sctpaddrport, 5)
        #             except error.ProxyError as e:
        #                 error_msg = "PySocks Error: (%s:%s) for sctPT (%s)" % \
        #                             (e.interface, e.port, e.socketError[1])
        #                 logger.warning(error_msg)
        #                 pyptlib_python3.pyptlib.client.reportFailure('sctPT', error_msg)
        #     except error.CannotListenError as e:
        #         error_msg = "Couldnt start sockets (%s:%s) for sctPT (%s)." % \
        #                         (e.interface, e.port, e.socketError[1])
        #         logger.warning(error_msg)
        #         pyptlib_python3.pyptlib.client.reportFailure('sctPT', error_msg)
        transport = network.ClientNetwork.ClientNetwork()
        transport.launchTransport(socksaddrport, sctpaddrport, socksversion)
    #
    #REPORT SUCCESS TO PYPTLIB AND TOR
    #
        should_start_threading = True
        self.logger.debug("Successfully launched sctPT. Socks listening at: " + (str(socksaddrport)))
        self.logger.debug("SCTP listening at: " + str((socksaddrport)))

        #enable this when using with tor
        # pyptlib_python3.pyptlib.client.reportSuccess('sctPT', socksversion, (socksaddrport), None, None)
        # pyptlib_python3.pyptlib.client.ReportEnd()
        #tells pyptlib everything is finished, wihch then tells tor to start pushing traffic

        if should_start_threading:
            #args might be suitable to have here
            isActiveBool = transport.startProxying()
            if isActiveBool:
                self.logger.info("Data proxying correctly")
        else:
            self.logger.info("No transports launched.")