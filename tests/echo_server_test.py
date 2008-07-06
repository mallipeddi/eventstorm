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
    msg = 'Hello, world'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('', 8080))
    s.send(msg)
    data = s.recv(1024)
    s.close()
    assert data == msg
