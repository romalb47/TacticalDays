#!/usr/bin/env python3
# coding: utf-8 

import threading
import socket, select
from multiprocessing import Pipe
import json
import time

import classe
import instance
import login
import matchmaking


def network_packet_decode(logger, data, Joueur, sock, pipe):
	packet_data = json.loads(data.decode("utf-8"))
	logger.debug("Données reçu: %s", packet_data)
			
	if packet_data["cmd"] == "login":
		if not login.do_login(logger, Joueur, packet_data):
			Joueur.login_error += 1
			logger.debug("Erreur de login %s", Joueur.login_error)
			sock.sendall(json.dumps({"cmd":"login", "status":"error"}).encode("utf-8"))
			if Joueur.login_error>5:
				return False
		else:
			sock.sendall(json.dumps({"cmd":"login", "status":"ok", "uuid":Joueur.uuid}).encode("utf-8"))

	else:
		pipe.send(packet_data)
	
	
	return True
	
def pipe_packet_decode(logger, data, sock):
	if data["cmd"] == "close":
		return False
		
	sock.sendall( json.dumps(data).encode("utf-8") )
	logger.debug("Send data %s", data)
	return True


def handle(connection, address, pipe, Joueur):
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger("process-%r" % (address,))
	data_in_waiting = b""
	data_complete = False

	try:
		logger.debug("Connection de %r", address)
		running = True
		while running:
			
			fno_to_read = select.select([connection, pipe], [], [])

			for to_read in fno_to_read[0]:
				if to_read == connection:
					data = connection.recv(1)
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
						if not network_packet_decode(logger, data_in_waiting, Joueur, connection, pipe):
							running = False
							break
							
				if to_read == pipe:
					if not pipe_packet_decode(logger, pipe.recv(), connection):
						running = False
						break

			if pipe.closed:
				running = False
				
	except:
		logger.exception("Probleme de requete")
	finally:
		logger.debug("Fermeture de la socket")
		Joueur.islogin = False
		pipe.close()
		connection.close()

class Server(object):
	def __init__(self, hostname, port):
		import logging
		self.logger = logging.getLogger("server")
		self.hostname = hostname
		self.port = port

	def start(self):
		self.logger.debug("Ecoute port "+ str(self.hostname) +":"+ str(self.port))
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(1)

		matchmaking_process = threading.Thread(target=matchmaking.run)
		matchmaking_process.daemon = True
		matchmaking_process.start()
		self.logger.debug("Processus matchmaker démarré %r", matchmaking_process)
		
		while True:
			conn, address = self.socket.accept()
			self.logger.debug("Connection entrante")
						
			self.logger.debug("Création du joueur...")
			parent_conn, child_conn = Pipe()
			
			Nouveau_Joueur = classe.Joueur(parent_conn)
			
			matchmaking.JOUEUR_CONNECTE.append(Nouveau_Joueur) # Mise a dispo du nouveau joueur pour le thread de matchmaking
			
			process = threading.Thread(target=handle, args=(conn, address, child_conn, Nouveau_Joueur))
			process.daemon = True
			process.start()
			self.logger.debug("Processus fils démarré %r", process)
