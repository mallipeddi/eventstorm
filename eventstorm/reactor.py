"""
with eventstorm.loop(): # http://docs.python.org/whatsnew/pep-343.html
    eventstorm.tcp_server()
    eventstorm.timer()
"""
import event
class loop(object):
    def __enter__(self):
        event.init()
    
    def __exit__(self, type, value, tb):
        event.dispatch()
        return True
