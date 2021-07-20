import eventlet
import socket

def handle(fd):
    print("client connected")
    while True:
        #pass through every non-eof line
        x = fd.readline()
        if not x:
            break
        print(x)
        fd.write(x)
        fd.flush()
        print("echoed", x, end=' ')
    print("client disconnected")

print("server socket listening on port 6000")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
server.bind(("0.0.0.0", 6000))
server.listen(10)
pool = eventlet.GreenPool()

while True:
    try:
        new_sock, address = server.accept()
        print("accepted", address)
        pool.spawn_n(handle, new_sock.makefile('rw'))
    except (SystemExit, KeyboardInterrupt):
        break
