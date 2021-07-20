import socket
import asyncio

async def handle_echo(reader, writer):
    data = await sock.recv(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    sock.bind(("0.0.0.0", 8888))
    sock.listen(10)
    await sock_accept(sock)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())




#asyncio takes care of buffer for you

#server:
# async def sctptotcp(reader, writer):
#     data = await reader.read()
#     #gets address of client presumably for logging reasons
#     addr = writer.get_extra_info('peername')
#     log.debug(f"recieved something from {addr}")
#
#     #define transport as a function
#     #you might not need all the configuration code, since this transport simply changes tcp to sctp, and doesnt manipulate data
#     #message = transports.sctPT.upstream_from_client(data), maybe some validation
#
#     writer.write(data)
#     await writer.drain()
#     writer.close()
#
# async def main():
#     #client_connected_cb quote from docs: The client_connected_cb callback is called whenever a new client connection is established.
#     # It receives a (reader, writer) pair as two arguments, instances of the StreamReader and StreamWriter classes.
#     server = await asyncio.start_server(client_connected_cb=sctptotcp, host='0.0.0.0', port=8888, flags=socket.IPPROTO_SCTP)
#     #does not support proto arg, using flag^
#     addr = server.sockets[0].getsockname()
#     #log.debug(f"serving on {addr}")
#
#     async with server:
#         await server.serve_forever()
#
# asyncio.run(main())

