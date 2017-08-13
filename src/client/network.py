#!/usr/bin/env python3
# coding: utf-8 

import multiprocessing
import time
import socket
import json
import logging
import hashlib
import select
import random
from multiprocessing import Pipe

class network_conn():
	
	def __init__(self, address, port):
		self.address = address
		self.port = port
		self.loginok = False
		self.pipe = start(self.address, self.port)
	
	def login(self, login, password):
		temp = password + str(int(time.time()/10))
		passwd = hashlib.sha224(temp.encode("utf-8")).hexdigest()
		packet = {"cmd":"login", "user":login, "pwd":passwd}
		self.pipe.send(packet)
		
	def join_room(self, room_uuid, passwd=""):
		packet = {"cmd":"join_room", "uuid":room_uuid, "pwd":passwd}
		self.pipe.send(packet)
		
	def move_entity(self, uuid, pos):
		packet = {"cmd":"join_room", "uuid":room_uuid, "pwd":passwd}
		self.pipe.send(packet)
		
	def process_pipe(self):
		if not self.pipe_has_data():
			return False
		
		data = self.pipe.recv()
		
		if data["cmd"] == "login":
			if data["status"] == "ok":
				self.loginok = True
				return "login_ok"
			if data["status"] == "nok":
				self.loginok = False
				return "login_nok"
		
	def pipe_has_data(self):
		return self.pipe.poll()

	def close(self):
		self.pipe.send({"cmd":"close"})
		self.pipe.close()


def network_packet_decode(logger, data, pipe):
	data = json.loads(data.decode("utf-8"))
	pipe.send(data)
	return True
	
	
def pipe_packet_decode(logger, data, sock):
	if data["cmd"] == "close":
		return False
		
	sock.sendall( json.dumps(data).encode("utf-8") )
	return True


def handle(pipe, address, port):
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger("network-%s:%s" % (address,port))
	data_in_waiting = b""
	data_complete = False

	try:
		logger.debug("Connection de %s:%s" % (address,port))
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((address, port))
		
		running = True
		while running:
			
			fno_to_read = select.select([sock, pipe], [], [], 0.5)

			for to_read in fno_to_read[0]:
				if to_read == sock:
					data = sock.recv(1)
					if data == b"":
						logger.debug("Socket fermée par le partenaire")
						running = False
						break
						
					if data == b"{":
						data_in_waiting = data
						data_complete = False
					elif data == b"}":
						data_in_waiting += data
						data_complete = True
					else:
						data_in_waiting += data
					
					if data_complete:
						if not network_packet_decode(logger, data_in_waiting, pipe):
							running = False
							break
							
				if to_read == pipe:
					if not pipe_packet_decode(logger, pipe.recv(), sock):
						running = False
						break

			if pipe.closed:
				running = False

	except:
		logger.exception("Probleme de requete")
	finally:
		logger.debug("Fermeture de la socket")
		sock.close()


def start(addresse, port):
	parent_conn, child_conn = Pipe()
	
	process = multiprocessing.Process(target=handle, args=(child_conn, addresse, port))
	process.daemon = True
	process.start()
	
	logging.debug("Processus réseau démarré %r", process)
	
	return(parent_conn)
