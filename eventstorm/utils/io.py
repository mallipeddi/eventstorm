import socket

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
