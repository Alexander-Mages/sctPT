import pyptlib

#gather cli arguments somehow

def do_managed_mode():
    if pyptlib.util.checkClientMode():
        log.info('Entering client managed mode')
        #below line nonorig, start everything in managed mode
        #calls on client.py, a file with only this function defined
        managed_client.do_managed_client()
    else:
        log.info('Entering server managed mode')
        #below line nonorig, start managed mode for server
        #calls upon server.py, same directory as client.py, file with only this function defined
        managed_server.do_managed_server()

#add support for external mode later on


#runs setup method for transports
#only used in external mode
#def run_transport_setup(ptconfig):
#    for transport, transport_class in transports.transports.items():
#        transport_class['base'].setup(pt_config)

#def pyobfsproxy
#parses commandline args
#logs startup
#starts heartbeat for every hour
#initiates managed mode if managed arg is there
#if not do external