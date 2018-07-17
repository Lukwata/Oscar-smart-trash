# a lightweight, fast implementation of message bus based on zeromq

host = "ipc:///tmp/"

def topic(name):
    return host + name
