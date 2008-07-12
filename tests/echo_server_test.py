import eventstorm
from datetime import datetime
import threading

class EchoServer(eventstorm.BaseServer):
    def accept_connection(self, connection):
        pass
class EchoHandler(eventstorm.BaseConnectionHandler):
    def receive_data(self, data):
        self.send_data(data)

def test_simple_echo():
    class EchoServerThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self._echo_server = EchoServer(connection_handler=EchoHandler)
        def run(self):
            self._echo_server.run()
    t = EchoServerThread()
    t.start()
    
    import socket
    msg = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." * 10
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('', 8080))
    except socket.error, e:
        print e, e.args[0]
        s.close()
        assert False
        return
    
    # send all of msg to server
    try:
        s.sendall(msg)
    except socket.error, e:
        print e, e.args[0]
        s.close()
        assert False
        return
    
    # recv all of msg from server
    accData = ""
    while(True):
        try:
            data = s.recv(eventstorm.utils.io.BUFFER_LENGTH)
        except socket.error, e:
            print e, e.args[0]
            s.close()
            assert False
            return            
        if len(data) == 0:
            #print "Connection closed"
            s.close()
            assert False
            return
        else:
            print data
            accData += data
        if len(accData) >= len(msg):
            break
    s.close()
    assert accData == msg
