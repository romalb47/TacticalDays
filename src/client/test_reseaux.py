#!/usr/bin/env python3
# coding: utf-8 

import multiprocessing
import time
import socket
import json

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("localhost", 9000))
	data = {"cmd":"login", "user":"pir17", "pwd":"98745"}
	time.sleep(2)
	print(json.dumps(data))
	sock.sendall(json.dumps(data).encode("utf-8"))
	sock.sendall(json.dumps(data).encode("utf-8"))
	sock.sendall(json.dumps(data).encode("utf-8"))
	sock.sendall(json.dumps(data).encode("utf-8"))
	
	
	
	
#	result = sock.recv(1024)
#	print(result)
	sock.close()
