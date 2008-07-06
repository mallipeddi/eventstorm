import os
import event
import sys
import socket

from base import BaseServer, BaseConnectionHandler, BaseDeferred
from utils import io

def tcp_server(addr=('', 8080), handler=BaseConnectionHandler):
    bs = BaseServer(addr=addr[0], port=addr[1], connection_handler=handler)

def deferred(operation, opargs=(), callback=None):
    bd = BaseDeferred(operation=operation, opargs=opargs, callback=callback)
