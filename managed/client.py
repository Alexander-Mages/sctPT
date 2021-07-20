from __future__ import absolute_import
import client
import sctPT.network.launch_transport as launch_transport
import sctPT.transports.transports as transports
import sctPT.common.log as logging
import sctPT.common.transport_config as transport_config
from pyptlib.client import ClientTransportPlugin
from pyptlib.config import EnvError

import pprint

log = logging.get_obfslogger

def do_managed_client():
    #start managed-proxy protocol as client

    should_start_event_loop = False
    #not sure what this does^ adding to prevent errors


#
#GET TRANSPORT INFO FROM TOR
#


    ptclient = ClientTransportPlugin
    try:
        #ptclient.init(transports.transports.keys())
        #or
        ptclient.init(["SCTP", "Dummy"])
        #^ arg is the list of names of transports supported
    except EnvError as err:
        #listens for error from pyptlib
        log.warning("Client managed proxy protocol failed (%s)." % err)
        return
    #^ part of pyptlib, gets transport information from tor

    log.debug("pyptlib gave us the following data:\n'%s'", pprint.pformat(ptclient.getDebugData()))
    #added verbosity, dont see a reason to not use


#
#CONFIGURE TRANSPORTS
#


##TAKE A SECOND LOOK AT THIS
    for transport in ptclient.GetTransports():

        pt_config = transport_config.TransportConfig()
        pt_config.setStateLocation(ptclient.config.getStateLocation())
        pt_config.setListenerMode("socks")
        pt_config.setObfsproxyMode("managed")
        #all 4 functions defined in transport_config.py
    #^configures managed mode parameters, state location and transports list is passed from init()

        transport_class = transports.get_transport_class(transport, 'socks')
    #^Defined in transports.py, used in server.py, client.py, and launch_transport.py
        transport_class.setup(pt_config)
    #check this^

#
#LAUNCH TRANSPORTS
#


        try:
            addrport = launch_transport.launch_transport_listener(transport, None, 'socks', None, pt_config)
            #^defined in launch_transport.py
            #launches transport with parameters and current transport
            #not sure how it decides on one transport yet
        except transports.TransportNotFound:
            log.warning("Could not find transport '%s'" % transport)
            ptclient.reportMethodError(transport, "Could not find transport.")
            continue
        except error.CannotListenError as e:
            error_msg = "Could not set up listener (%s:%s) for '%s' (%s)." % \
                        (e.interface, e.port, transport, e.socketError[1])
            log.warning(error_msg)
            ptclient.reportMethodError(transport, error_msg)
            continue
            #reports errors to pyptlib


#
#REPORT SUCCESS TO PYPTLIB AND TOR
#


        #still have no idea what this is, adding it to prevent errors
        should_start_event_loop = True
        log.debug("Successfully launched '%s' at '%s'" % (transport, log.safe_addr_str(str(addrport))))
        ptclient.reportMethodSuccess(transport, "socks5", addrport, None, None)
        #report success to log and pyptlib

    ptclient.ReportMethodsEnd()
    #tells pyptlib everything is finished, wihch then tells tor to start pushing traffic

    if should_start_event_loop:
        log.info("Starting up the event loop.")
        loop = client.get_running_loop()
        loop.run_forever()
    else:
        log.info("No transports launched. Nothing to do.")

    if not loop.is_running():
        log.info("Event loop not started correctly")