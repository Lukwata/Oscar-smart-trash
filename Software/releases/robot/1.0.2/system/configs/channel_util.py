import channel_main as channel

server_channels = set()
local_channels = set()


def server(port):
    if port in server_channels:
        raise RuntimeError("port [" + str(port) + "] is already taken")
    else:
        server_channels.add(port)
        return channel.SERVER + ":" + str(port)


def local(name):
    if name in local_channels:
        raise RuntimeError("channel [" + name + "] is already taken")
    else:
        local_channels.add(name)
        return channel.LOCAL + "/" + name

