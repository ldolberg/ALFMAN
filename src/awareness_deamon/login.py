#!/usr/bin/python
import sys
#import os
import daemon
import socket
import threading
import SocketServer
import signal
import lockfile
import grp
from logger import logger
import json
    
import config
import driver
ip = config.host
port =config.port

def test_login(pid):
    #os.popen('pidof chromium-browser').read().strip()
    d={'type':'auth','user':'app','password':'app','pid':'%s'%pid}
    message = json.dumps(d)
    print "Sent: {}".format(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(message)
    response = sock.recv(1024)
    print "Received: {}".format(response)
    sock.close()

if __name__ == '__main__':
    test_login(sys.argv[1])