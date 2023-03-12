import asyncio
import cowsay
import shlex

clients = {}

AVAILABLE_COWS = set(cowsay.list_cows())


async def chat(reader, writer):
    is_registered = False
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    exit_flag = False
    while not reader.at_eof() and not exit_flag:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                msg = q.result().decode().strip()
                cmd = shlex.split(msg)
                if len(cmd) == 0:
                    # empty command
                    continue
                if cmd[0] == "who":
                    writer.write(f"Registered cows: {', '.join(clients.keys())}\n".encode())
                    await writer.drain()
                elif cmd[0] == "cows":
                    writer.write(f"Available cows: {', '.join(AVAILABLE_COWS)}\n".encode())
                elif cmd[0] == "login":
                    if is_registered:
                        writer.write("You already registered as {me}\n".encode())
                        await writer.drain()
                    else:
                        assert len(cmd) > 1, "There should be a name for login"
                        try_name = cmd[1]
                        if try_name in AVAILABLE_COWS:
                            AVAILABLE_COWS.remove(try_name)
                            me = cmd[1]
                            clients[me] = asyncio.Queue()
                            writer.write(f"Registered as {me}\n".encode())
                            await writer.drain()
                            is_registered = True
                            receive.cancel()
                            receive = asyncio.create_task(clients[me].get())
                        else:
                            writer.write("Cow is already taken\n".encode())
                            await writer.drain()
                elif cmd[0] == "say":
                    if not is_registered:
                        writer.write("You should be registered to use chat\n".encode())
                        await writer.drain()
                    else:
                        assert len(cmd) == 3, "Invalid command length"
                        _, target_cow, text = cmd 
                        await clients[target_cow].put(f"\n{me} says to you:\n{cowsay.cowsay(text, cow=me)}")
                        writer.write(f"you say to {target_cow}:\n{cowsay.cowsay(text, cow=me)}".encode())
                        await writer.drain()
                elif cmd[0] == "yield":
                    if not is_registered:
                        writer.write("You should be registered to use chat\n".encode())
                        await writer.drain()
                    else:
                        for out in clients.values():
                            if out is not clients[me]:
                                await out.put(f"\n`{me} says to all:\n{cowsay.cowsay(cmd[1], cow=me)}")
                        writer.write(f"you say to all:\n{cowsay.cowsay(cmd[1], cow=me)}".encode())
                        await writer.drain()
                elif cmd[0] == "quit":
                    exit_flag = True
                    break
                else:
                    writer.write("Invalid command".encode())
                    await writer.drain()

            elif q is receive and is_registered:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print("Removed cow:", me)
    del clients[me]
    AVAILABLE_COWS.add(me)
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
