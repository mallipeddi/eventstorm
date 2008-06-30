import event
import socket
from eventstorm.utils import io

class BaseConnection(object):
    def __init__(self, sock, addr):
        self._sock = sock
        self.addr = addr
        
        def _handle_read(ev, sock, evtype, *args):
            try:
                data = sock.recv(1024)
            except socket.error, e:
                print e
                sock.close()
                return
            self.receive_data(data)
            ev = event.event(_handle_read, handle=self._sock, evtype=event.EV_READ)
            ev.add()
            
        ev = event.event(_handle_read, handle=self._sock, evtype=event.EV_READ)
        ev.add()
    
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
    def __init__(self, addr='', port=8080, connection_handler=BaseConnection):
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
