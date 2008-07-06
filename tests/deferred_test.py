from __future__ import with_statement
import eventstorm
import threading

def factorial(n):
    f = 1
    count = n
    while(count>0):
        f *= count
        count -= 1
    return f

def on_complete_factorial(f):
    print "Factorial = " + str(f)

class FactorialThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        with eventstorm.loop():
            eventstorm.deferred(factorial, (5, ), on_complete_factorial)
            eventstorm.deferred(factorial, (10, ), on_complete_factorial)

def test_deferred_factorial():
    t = FactorialThread()
    t.start()
    
    print "Waiting for answer..."
    assert True

def test_invalid_callback():
    try:
        eventstorm.deferred(factorial, (10, ), 10) # 10 is an invalid callback
    except eventstorm.exceptions.CallbackNotCallableException, e:
        assert True
        return
    assert False
