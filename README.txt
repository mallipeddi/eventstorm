TODO
    class MyHandler(eventstorm.BaseHandler):
        def receive_data(self, data):
            pass
    eventstorm.start_server((addr, port), handler=MyHandler)
    
    eventstorm.run([])
    
    jQuery("#id1", function() {
    
    });
    jQuery(".class1").addClass("class2").hide("slow", function() { //callback });
    
    eventstorm.deferred()
    
    with open('/path/to/file','w') as f:
        for line in f:
            pass
    
    with eventstorm.loop(): # http://docs.python.org/whatsnew/pep-343.html
        eventstorm.start_server()
        eventstorm.timer()
        