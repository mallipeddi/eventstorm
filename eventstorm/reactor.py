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
        if tb is None: # if there were no exceptions in the `with` block
            event.dispatch()
            return True
        else:
            return False
