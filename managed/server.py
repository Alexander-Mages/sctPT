from __future__ import absolute_import
import pyptlib_python3.pyptlib.client
from pyptlib_python3.pyptlib.config import EnvError
import pprint
import sys
import logging
import network.ServerNetwork


class managedServer:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def managed_server(self, sctpaddr, serverinterface):
        should_start_threading = False

        sctpaddrport = sctpaddr
        #uncomment for use with pyptlib
        #tcpaddrport = (serverinterface, managed_info['orport'])
        tcpaddrport = (serverinterface, 6000)

    #to enable use with Tor, delete line 44 and 45, and uncomment
    #
    #GET TRANSPORT INFO FROM TOR
    #
    #     try:
    #         config_info = pyptlib_python3.pyptlib.server.init(["sctPT"])
    #     except EnvError as err:
    #         logger.warning("pyptlib could not bootstrap (%s)." % err)
    #         return
    #     logger.debug("data from pyptlib:\n'%s'", pprint.pformat(pyptlib_python3.pyptlib.server.getDebugData()))
    #
    # #CONFIGURE TRANSPORTS
    #
    #     if 'sctPT' in config_info['transports']:
    #         transport = network.ServerNetwork.ServerNetwork()
    #         try:
    #             transport.launchTransport(sctpaddrport, tcpaddrport)
    #         except error.CannotListenError as e:
    #             error_msg = "Couldnt start socket."
    #             logger.warning(error_msg)
    #             pyptlib_python3.pyptlib.server.reportFailure('sctPT', error_msg)
        transport = network.ServerNetwork.ServerNetwork()
        addr1, addr2 = transport.launchTransport(sctpaddrport, tcpaddrport)


    #
    #REPORT SUCCESS TO PYPTLIB AND TOR
    #
        should_start_threading = True
        self.logger.debug("Successfully launched sctPT server")
        self.logger.debug("Sctp connected at "+(str(addr1)) + "\nTcp connected at " + (str(addr2)))

        #enable the below when in use with tor
        # pyptlib_python3.pyptlib.client.reportSuccess('sctPT', socksversion, (socksaddrport), None, None)
        # pyptlib_python3.pyptlib.client.ReportEnd()
        #tells pyptlib everything is finished, wihch then tells tor to start pushing traffic

        if should_start_threading:
            isActiveBool = transport.startProxying()
            if isActiveBool:
                self.logger.info("Data proxying correctly")
        else:
            self.logger.info("No transports launched.")