eventstorm

eventstorm is a Python library which provides event-driven I/O using the reactor loop. eventstorm is built using libevent/pyevent and is heavily inspired by the eventmachine Ruby library.

eventstorm is pre-alpha. Play with it at your own risk!

Usage:

    with eventstorm.loop(): # reactor loop
        eventstorm.deferred(to_run, args_to_run, post_run)
        eventstorm.tcp_server(('', 8000), MyHTTPConnectionHandler)
        eventstorm.timer()

TODO

    handle UNIX domain sockets
    handle UDP datagrams
    stream_file_data(/path/to/file)
    remove dependency on `with` stmt
