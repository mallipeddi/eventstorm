from __future__ import with_statement
import eventstorm
import threading

class Pinger(eventstorm.BaseConnectionHandler):
    def receive_data(self, data):
        self.send_data("ping")
class Ponger(eventstorm.BaseConnectionHandler):
    def receive_data(self, data):
        self.send_data("pong")

class PingPongThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        with eventstorm.loop():
            eventstorm.tcp_server(addr=('', 8000), handler=Pinger)
            eventstorm.tcp_server(addr=('', 9000), handler=Ponger)

def test_reactor_loop():
    t = PingPongThread()
    t.start()
    
    import time
    time.sleep(1)
    
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    err = s.connect_ex(('', 8000))
    print err
    s.send("hello")
    data = s.recv(1024)
    s.close()
    assert data == "ping"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('', 9000))
    s.send("hello")
    data = s.recv(1024)
    s.close()
    assert data == "pong"

def test_exception_inside_reactor_loop():
    
    class SomeException(Exception):
        def __init__(self, message):
            Exception.__init__(self, message)
    
    try:
        with eventstorm.loop():
            raise SomeException("some exception")
    except SomeException, e:
        assert True
        return
    
    assert False
