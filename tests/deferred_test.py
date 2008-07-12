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

def some_disk_operation():
    f = open("fixture.txt", "r")
    count = 0
    for line in f:
        count += 1
    return count

def on_complete_some_disk_operation(lines):
    print "Line count: %s" % lines

class DiskOperationThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        with eventstorm.loop():
            eventstorm.deferred(some_disk_operation, callback=on_complete_some_disk_operation)

def test_read_from_disk():
    t = DiskOperationThread()
    t.start()
    
    print "Waiting for answer..."
    assert True
