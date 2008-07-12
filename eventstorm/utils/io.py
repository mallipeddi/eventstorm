import socket, errno, os
from datetime import datetime

BUFFER_LENGTH = 4096
BACKLOG = 5

def server_socket(addr, port):
    """ Return a new non-blocking listening socket bound to the given interface and port. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)
    sock.bind(('', port))
    sock.listen(BACKLOG)
    return sock

def client_socket(addr, port):
    """ Return a new non-blocking client socket connected to the given address and port. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex((addr, port))
    return sock

def server_unix_socket(filepath):
    """ Return a new non-blocking listening UNIX domain socket bound to the given filepath. """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        os.remove(filepath)
    except OSError:
        pass
    sock.setblocking(False)
    sock.bind(filepath)
    sock.listen(BACKLOG)
    return sock

def client_unix_socket(filepath):
    pass
