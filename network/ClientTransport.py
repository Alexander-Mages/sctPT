import eventlet
import socket
import socks


#this file only supports one socks and one sctp connection, servers work with many, so threads will have to be spawned on connection
#e.g.
# while True:
#     try:
#         new_sock, address = sctpsock.accept()
#         print("accepted", address)
#         pool.spawn_n(handle, new_sock.makefile('rw'))
#     except (SystemExit, KeyboardInterrupt):
#         break

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
pool = eventlet.GreenPool()

#source is socks/tor browser, destination is tor bridge
def proxyDownstream(source, dest):
    while True:
        #this buffer size is arbitrary and holds no reasoning, probably want to change if helps performance
        print("first")
        data = source.recv(4096)
        if data == '':
            break
        dest.sendall(data)

#source is sctp traffic from bridge, destination is socks/tor browser
def proxyUpstream(source, dest):
    print("second works")
    while True:
        data = source.recv(4096)
        if data == '':
            break
        dest.sendall(data)

        #spawn concurrent threads

while True:
    print("at loop")
    try:
        pile = eventlet.GreenPile(pool)

        print("1")
        sctpsocket, address = sctpsock.accept()
        print("sctp connection accepted from bridge at", address)
        sockssocket, address = sockssock.accept()
        print("socks connection accepted from tor browser at", address)
        pile.spawn(proxyDownstream(source=sockssocket, dest=sctpsocket))
        print("here")
        pile.spawn(proxyUpstream(source=sctpsocket, dest=sockssocket))
    except (SystemExit, KeyboardInterrupt):
        break


# except (ConnectionError):
#     print("one of the connections has terminated. btw, make this more verbose with more cases")
#
# except (SystemExit, KeyboardInterrupt):
