#!/usr/bin/python
#import sys
#import os
import daemon
#import socket
import threading
import SocketServer
import signal
import lockfile
import grp
from logger import logger

    
import config
import driver

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            #cur_thread = threading.current_thread()
            response = driver.parse_msg(data)
            #"{}: {}".format(cur_thread.name, data)
            print response
            self.request.send(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

#
context = daemon.DaemonContext(
    working_directory='/var/lib/',
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/driver_SDN.pid'),
    )

context.signal_map = {
    signal.SIGTERM: driver.program_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: driver.reload_service_config,
    }

daemon_gid = grp.getgrnam('daemon').gr_gid
context.gid = daemon_gid

def listen():
#if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = config.host, config.port

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    #LOG print "Server loop running in thread:", server_thread.name
    server.serve_forever()

if __name__ == '__main__':
    with daemon.DaemonContext():
        #try:
        listen()
        #except Exception, e:
            #print e
            #logger.log_error(e)
