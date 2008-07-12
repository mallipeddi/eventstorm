import os
import event
import sys
import socket
from datetime import datetime

from base import BaseServer, BaseConnectionHandler, BaseDeferred
from utils import io
from exceptions import CallbackNotCallableException

def tcp_server(addr=('', 8080), handler=BaseConnectionHandler):
    bs = BaseServer(addr, handler)

def deferred(operation, opargs=(), callback=None):
    if callback is not None and not callable(callback):
        raise CallbackNotCallableException("%s is not callable." % callback)
    
    # TODO - check if supplied opargs tuple matches the signature of the supplied callback?
    # http://mail.python.org/pipermail/python-list/2004-January/246503.html
    
    bd = BaseDeferred(operation=operation, opargs=opargs, callback=callback)
