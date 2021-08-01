from __future__ import absolute_import
import sys
import argparse
import pyptlib_python3.pyptlib.config
import managed.client
import managed.server
import logging

def do_managed_mode(sctpaddr, socksVersion, socksPort, serverinterface, serverbool):
    #This code uses command line args to choose client or server. default is client
    if serverbool == True:
        managedclient = managed.server.managedServer()
        managedclient.managed_server(sctpaddr, serverinterface)
    else:
        managedclient = managed.client.managedClient()
        managedclient.managed_client(sctpaddr, socksVersion, socksPort)

    #This code uses pyptlib to look for Tor set environmental variables
    # if pyptlib_python3.pyptlib.config.checkClientMode():
    #     log.info('Entering client managed mode')
    #     managed.client.managed_client(sctpaddr, socksVersion, socksPort)
    # else:
    #     log.info('Entering server managed mode')
    #     managed.server.managed_server(sctpaddr, serverinterface)

bindinterface = ''
bindport = ''
managedorexternalmode = ''
socksversion = ''
socksport = ''
servint = ''
verbose = True
parser = argparse.ArgumentParser(description='SCTP Based Pluggable Transport\nnote: ensure firewall rules and network configuration are suitable for SCTP')
parser.add_argument('--bind-interface', dest='bindinterface', action='store_const', const=bindinterface, default="0.0.0.0",
                    help='Interface for SCTP Socket to bind to, (default: `0.0.0.0`)')
parser.add_argument('--bind-port', dest='bindport', action='store_const', const=bindport, default=6000,
                    help='Port for SCTP Socket to bind to, (default: 6000)')
parser.add_argument('--server-interface', dest='servint', action='store_const', const=servint, default="0.0.0.0",
                    help='Interface facing tor network, (default: 0.0.0.0)')
parser.add_argument('--managed-or-external', dest='managedorexternalmode', action='store_const', const=managedorexternalmode, default="managed",
                    help='Managed or external mode, in 99%% of use cases managed is ideal (default: `managed`)')
parser.add_argument('--socks-version', dest='socksversion', action='store_const', const=socksversion, default=5,
                    help='Socks version to be used, Socks5 is idea excepting certain cases (default: 5)')
parser.add_argument('--socks-port', dest='socksport', action='store_const', const=socksport, default=9050,
                    help='Port for socks to listen on, dependent on Tor configuration (default: 9050)')
parser.add_argument('--verbose', dest='verbose', action='store_true', default=True,
                    help='Toggle logging verbosity, (default: true, change after development)')
parser.add_argument('--server', dest='server', action='store_true', default=False,
                    help='Toggle server mode, (default: false)')
args = parser.parse_args()

parser.print_help()

sctpaddr = ((args.bindinterface, args.bindport))
socksVersion = args.socksversion
socksPort = args.socksport
isverbose = args.verbose
serverinterface = args.servint
serverbool = args.server
#configure logger
if isverbose:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stdout, level=logging.WARN)
#output_file_handler = logging.FileHandler("sctPT_log.log")
# stdout_handler = logging.StreamHandler(sys.stdout)
# logger.addHandler(stdout_handler)
logger = logging.getLogger(__name__)
#logger.addHandler(output_file_handler)


if args.managedorexternalmode == "managed":
    do_managed_mode(sctpaddr, socksVersion, socksPort, serverinterface, serverbool)
else:
    print("external mode not supported at this time")
