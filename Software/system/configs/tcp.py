# a lightweight, fast implementation of message bus based on zeromq

host = "tcp://127.0.0.1"
port = 5000
addresses = {}

def topic(name):
    if name in addresses:
        return addresses[name]
    else:
        global port
        port += 1
        address = host + ":" + str(port)
        addresses[name] = address
        return address
