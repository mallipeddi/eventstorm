import os, socket, sys
import event
from eventstorm.utils import io

class BaseConnectionHandler(object):
    def __init__(self, sock, addr):
        self._sock = sock
        self.addr = addr
        self._to_be_sent = "" # write buffer
        
        self._sock.setblocking(False)
        
        self._read_ev = event.event(self._handle_read, handle=self._sock, evtype=event.EV_READ|event.EV_PERSIST)
        self._read_ev.add()
    
    def _handle_read(self, ev, sock, evtype, *args):
        try:
            data = sock.recv(io.BUFFER_LENGTH)
        except socket.error, e:
            print e, e.args[0] # errno
            sock.close()
            self._read_ev.delete()
            self.handle_close(error=e.args[0])
            return
        
        if len(data) == 0: # connection closed by the other party
            sock.close()
            self._read_ev.delete()
            self.handle_close()
            return
        
        # invoke callback upon receiving data
        self.receive_data(data)
    
    def receive_data(self, data):
        "Callback func called upon receiving data. User is expected to munge the data as he wishes."
        print "Received data: %s" % data
    
    def send_data(self, data):
        "Send the data over this connection."
        def _handle_write():
            try:
                sent = self._sock.send(self._to_be_sent)
            except socket.error, e:
                print e, e.args[0]
                self._sock.close()
                self.handle_close(error=e.args[0])
                return
            if sent < len(self._to_be_sent):
                # all the data to be sent has not been sent yet.
                # so reschedule a new write event to send the rest of the data.
                self._to_be_sent = self._to_be_sent[sent:]
                ev = event.write(self._sock, _handle_write)
                ev.add()
        
        # append data to the write buffer
        self._to_be_sent += data
        
        # schedule a write event
        ev = event.write(self._sock, _handle_write)
        ev.add()

    def handle_close(self, error=None):
        """Callback func called when the socket closes.
        
        User is expected to override this method and do any clean-up."""
        
        if error is not None:
            print "Connection closed due to error (errno = %d)" % error
        else:
            print "Connection closed."

class BaseServer(object):
    def __init__(self, addr=('', 8080), connection_handler=BaseConnectionHandler):
        self.addr, self.port = addr
        self._sock = io.server_socket(self.addr, self.port)
        self._connection_handler = connection_handler
        listen_ev = event.event(self._accept_connection, handle=self._sock, evtype=event.EV_READ | event.EV_PERSIST)
        listen_ev.add()
    
    def _accept_connection(self, ev, sock, evtype, *args):
        new_sock, new_addr = sock.accept()
        new_connection = self._connection_handler(new_sock, new_addr)
        self.accept_connection(new_connection)
    
    def accept_connection(self, connection):
        "Callback function called upon accepting a new connection."
        print "accepted new connection..."
    
    def run(self):
        event.dispatch()

class BaseDeferred(object):
    def __init__(self, operation, opargs, callback):
        self._operation = operation
        self._opargs = opargs
        self._callback = callback
        self._result_buffer = ""
        
        somePid = os.fork()
        
        if somePid != 0:
            # in the master process, open a listening unix domain socket, and
            # wait for the result from the slave process.
            
            sock = io.server_unix_socket("/tmp/eventstorm_p_%d" % somePid)
            listen_ev = event.read(sock, self._on_worker_connect, sock)
            listen_ev.add()
        else:
            # in the worker process, run the operation,
            # compute the result and send it back to the master
            # over the domain socket.
            
            result = operation(*opargs)
            sock = io.client_unix_socket("/tmp/eventstorm_p_%d" % os.getpid(), blocking=True)
            sock.sendall(str(result))
            sock.close()
            os._exit(0)
    
    def _on_worker_connect(self, sock):
        new_sock, new_addr = sock.accept()
        new_sock.setblocking(False)
        
        self._worker_read_ev = event.event(self._on_worker_complete, handle=new_sock, evtype=event.EV_READ|event.EV_PERSIST)
        self._worker_read_ev.add()
        
        #read_ev = event.read(new_sock, self._on_worker_complete, new_sock)
        #read_ev.add()
        
        # close the listening server socket since there's only 1 worker
        sock.close()
    
    def _on_worker_complete(self, ev, sock, evtype, *args):
        try:
            data = sock.recv(io.BUFFER_LENGTH)
        except socket.error, e:
            print e, e.args[0] # errno
            sock.close()
            self._worker_read_ev.delete()
            return

        if len(data) == 0: # connection closed by the worker process
            # clean-up
            sock.close()
            self._worker_read_ev.delete()
            
            # send the result received from the worker to
            # the user-supplied callback function (if any)
            if self._callback is not None:
                self._callback(self._result_buffer)
            return
        else: # append data received from worker to the result buffer
            self._result_buffer += data
        