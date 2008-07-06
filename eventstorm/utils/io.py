import socket
import os
from datetime import datetime

BUFFER_LENGTH = 1024
LQUEUE_SIZE = 500

def server_socket(addr, port):
    """ Return a new listening socket bound to the given interface and port. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.listen(LQUEUE_SIZE)
    return sock

def client_socket(addr, port):
    """ Return a new (non-blocking) client socket connected to the given address and port. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.connect_ex((addr, port))
    return sock

def server_domain_socket(filepath):
    """ Return a new listening UNIX domain socket bound to the given filepath. """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove(filepath)
    except OSError:
        pass
    sock.bind(filepath)
    sock.listen(1)
    return sock


def unique_domain_socket_name():
    while True:
        now = datetime.now()
        fname = "/tmp/%s_%s%s" % (str(os.getpid()), now.strftime("%Y%m%d%H%M%S"), getattr(now, 'microsecond'))
        if not os.path.exists(fname):
            break
    return fname
