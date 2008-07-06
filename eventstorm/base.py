import os, socket, sys
import event
from eventstorm.utils import io

class BaseConnectionHandler(object):
    def __init__(self, sock, addr):
        self._sock = sock
        self.addr = addr
        
        read_ev = event.event(self._handle_read, handle=self._sock, evtype=event.EV_READ)
        read_ev.add()
    
    def _handle_read(self, ev, sock, evtype, *args):
        try:
            data = sock.recv(io.BUFFER_LENGTH)
        except socket.error, e:
            print e
            sock.close()
            return
        
        # invoke callback upon receiving data
        self.receive_data(data)
        
        # bind to the read event for more data
        read_ev = event.event(self._handle_read, handle=self._sock, evtype=event.EV_READ)
        read_ev.add()
    
    def receive_data(self, data):
        "Callback func called upon receiving data. User is expected to munge the data as he wishes."
        print "Received data: %s" % data
    
    def send_data(self, data):
        "Send the data over this connection (non-blocking send)."
        def _handle_write(ev, sock, evtype, *args):
            try:
                sent = sock.send(data)
            except socket.error, e:
                print e
                sock.close()
            print "Sent: %d" %  sent
        ev = event.event(_handle_write, handle=self._sock, evtype=event.EV_WRITE)
        ev.add()

class BaseServer(object):
    def __init__(self, addr='', port=8080, connection_handler=BaseConnectionHandler):
        self.addr = addr
        self.port = port
        self._sock = io.server_socket(self.addr, self.port)
        self._connection_handler = connection_handler
        listen_ev = event.event(self._accept_connection, handle=self._sock, evtype=event.EV_READ | event.EV_PERSIST)
        listen_ev.add()
    
    def _accept_connection(self, ev, sock, evtype, *args):
        new_sock, new_addr = sock.accept()
        new_connection = self._connection_handler(new_sock, new_addr)
        self.accept_connection(new_connection)
    
    def accept_connection(self, connection):
        "Callback func called upon accepting a new connection."
        print "accepted new connection..."
    
    def run(self):
        event.dispatch()

class BaseDeferred(object):
    def __init__(self, operation, opargs, callback, path_to_socket):
        self._operation = operation
        self._opargs = opargs
        self._callback = callback
        self._path_to_socket = path_to_socket
        self._data = ""
        
        if os.fork() != 0:
            # in the master process, open a listening unix domain socket, and
            # wait for the result from the slave process.
            
            sock = io.server_domain_socket(self._path_to_socket)
            listen_ev = event.read(sock, self._on_worker_connect, sock)
            listen_ev.add()
        else:
            # in the worker process, run the operation,
            # compute the result and send it back to the master
            # over the domain socket.
            
            result = operation(*opargs)
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self._path_to_socket)
            sock.send(str(result))
            sock.close()
            sys.exit(0)
    
    def _on_worker_connect(self, sock):
        new_sock, new_addr = sock.accept()
        read_ev = event.read(new_sock, self._on_worker_complete, new_sock)
        read_ev.add()
        sock.close()
    
    def _on_worker_complete(self, sock):
        try:
            data = sock.recv(io.BUFFER_LENGTH)
        except socket.error, e:
            sock.close()
            return
        self._data += data
        if self._callback is not None:
            self._callback(self._data)
        
        # FIXME - handle result data longer than io.BUFFER_LENGTH ?   
        #read_ev = event.read(sock, self._on_worker_complete, sock)
        #read_ev.add()
        