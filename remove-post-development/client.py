import asyncio



#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPROTO_SCTP)



















async def tcp_echo_client(message):
    sock = socket.socket(socket.AF_INET, socket.IPPROTO_SCTP)
    sock.connect(("192.168.1.6", 8888))
    reader, writer = await asyncio.open_connection(sock=sock)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client('Hello World!'))





# async def clientecho(message):
#     reader, writer = await asyncio.open_connection(host="192.168.1.6", port=4444, proto=132)
#
#     writer.write(message)
#
#     data = await reader.read()
#     writer.close()
#
# asyncio.run(clientecho('hello world'))