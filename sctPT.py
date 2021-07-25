from __future__ import absolute_import
import sys
import argparse
import pyptlib_python3.pyptlib.config
import managed.client
import logging

def do_managed_mode(addr, socksVersion, socksPort):
    managedclient = managed.client.managedClient
    managedclient.managed_client(addr, socksVersion, socksPort)

    #commenting so it can be used without tor
    # if pyptlib_python3.pyptlib.config.checkClientMode():
    #     log.info('Entering client managed mode')
    #     #below line nonorig, start everything in managed mode
    #     #calls on client.py, a file with only this function defined
    #     managed.client.managed_client(addr, socksVersion, socksPort)
    # else:
    #     log.info('Entering server managed mode')
    #     #below line nonorig, start managed mode for server
    #     #calls upon server.py, same directory as client.py, file with only this function defined
    #     managed_server.do_managed_server()

#gather command line arguments
#all paramaters have defaults, theoretically tor would never pass a parameter
bindinterface = ''
bindport = ''
managedorexternalmode = ''
socksversion = ''
socksport = ''
verbose = True
parser = argparse.ArgumentParser(description='SCTP Based Pluggable Transport\nnote: ensure firewall rules and network configuration are suitable for SCTP')
parser.add_argument('--bind-interface', dest='bindinterface', action='store_const', const=bindinterface, default="0.0.0.0",
                    help='Interface for outward facing SCTP Socket to bind to, (default: `0.0.0.0`)')
parser.add_argument('--bind-port', dest='bindport', action='store_const', const=bindport, default=443,
                    help='Port for outward facing SCTP Socket to bind to, (default: 443)')
parser.add_argument('--managed-or-external', dest='managedorexternalmode', action='store_const', const=managedorexternalmode, default="managed",
                    help='Managed or external mode, in 99%% of use cases managed is ideal (default: `managed`)')
parser.add_argument('--socks-version', dest='socksversion', action='store_const', const=socksversion, default=5,
                    help='Socks version to be used, Socks5 is idea excepting certain cases (default: 5)')
parser.add_argument('--socks-port', dest='socksport', action='store_const', const=socksport, default=9050,
                    help='Port for socks to listen on, dependent on Tor configuration (default: 9050)')
parser.add_argument('--verbose', dest='verbose', action='store_true', default=True,
                    help='Toggle logging verbosity, (default: true, change after development)')
args = parser.parse_args()

parser.print_help()

addr = ((args.bindinterface, args.bindport))
socksVersion = args.socksversion
socksPort = args.socksport
isverbose = args.verbose
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
    do_managed_mode(addr, socksVersion, socksPort)
else:
    print("external mode not supported at this time")
