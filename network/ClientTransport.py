import time
import socket
import socks
import threading
#threading but with better performance, allows multiple cores to be used, syntax is a little odder, but performance is important
from multiprocessing import Process

class ClientTransport():
    #will need to eventually implement both socks versions
    print("launching socks proxy to communicate with the tor browser...")
    sockssock = socks.socksocket()

    socksversion = "SOCKS5" # this will need to be defined somewhere else

    if socksversion == "SOCKS5":
        sockssock.set_proxy(socks.SOCKS5, "127.0.0.1")
    elif socksversion == "SOCKS4":
        sockssock.set_proxy(socks.SOCKS4, "127.0.0.1") #subsequent argument is port if desired
    elif socksversion == "HTTP":
        sockssock.set_proxy(socks.HTTP, "127.0.0.1")
    else:
        print("error")
        #add an exception here, might want to look into custom errors

    sockssock.bind(("127.0.0.1", 9050)) #whatever port tor uses for socks
    sockssock.listen(25)


    print("launching upstream->downstream sctp socket on port 6000...")
    sctpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    sctpsock.bind(("0.0.0.0", 6000))
    sctpsock.listen(25)

    #initialize pool
    #controls threads running with concurrency

    #source is sctp traffic from bridge, destination is socks/tor browser
    def proxyUpstream(source, dest):
        while True:
            print("second works")
            data = source.recv(4096)
            if data == '':
                break
            dest.sendall(data)

            #spawn concurrent threads


    #source is socks/tor browser, destination is tor bridge
    def proxyDownstream(source, dest):
        while True:
            #this buffer size is arbitrary and holds no reasoning, probably want to change if helps performance
            print("first")
            data = source.recv(4096)
            if data == '':
                break
            dest.sendall(data)


    print("1")
    sctpsocket, address = sctpsock.accept()
    print("sctp connection accepted from bridge at", address)
    print("2")
    sockssocket, address = sockssock.accept()
    print("socks connection accepted from tor browser at", address)


    #CHANGE NAME OF SOCKSSOCKET, IT IS WAY TOO SIMIMLAR TO SOCKSOCKET
    #no idea whether to use multiprocessing, threading, concurrency, or asyncrynosity

    #whichever one of these runs first, is the one that starts
    upstreamTransport = threading.Thread(target=proxyUpstream, args=(sctpsocket, sockssocket))
    downstreamTransport = threading.Thread(target=proxyDownstream, args=(sockssocket, sctpsocket))

    downstreamTransport.start()
    upstreamTransport.start()

    downstreamTransport.join()
    upstreamTransport.join()


    # except (ConnectionError):
    #     print("one of the connections has terminated. btw, make this more verbose with more cases")
    #
    # except (SystemExit, KeyboardInterrupt):
