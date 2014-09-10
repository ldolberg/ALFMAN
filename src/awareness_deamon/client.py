#!/usr/bin/python
import socket
import config
import json


def client(ip, port, messages):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
    	for msg in messages:
	        sock.send(msg)
	        response = sock.recv(1024)
    		print "Received: {}".format(response)
	        
    finally:
    	sock.close()


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    ip, port = config.host,config.port    
    client(ip, port, [json.dumps({'type':'auth','user':'app','password':'app',"pid":9113}),"Hello World 2"])

