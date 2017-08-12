#!/usr/bin/env python3
# coding: utf-8 

import multiprocessing
import socket, select
from multiprocessing import Pipe
import json
import time

import classe
import login


def Data_packet_decode(logger, data, Joueur):
	packet_data = json.loads(data.decode("utf-8"))
	logger.debug("Données reçu: %s", packet_data)
			
	if packet_data["cmd"] == "login":
		if not login.do_login(logger, Joueur, packet_data):
			time.sleep(3)
			Joueur.login_error += 1
			logger.debug("Erreur de login %s", Joueur.login_error)
			if Joueur.login_error>5:
				return False
	

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
						if not Data_packet_decode(logger, data_in_waiting, Joueur):
							running = False
							break


					#connection.sendall(data)
										
				if to_read == pipe:
					pass
				
	except:
		logger.exception("Probleme de requete")
	finally:
		logger.debug("Fermeture de la socket")
		connection.close()

class Server(object):
	def __init__(self, hostname, port, Joueur_connecté):
		import logging
		self.logger = logging.getLogger("server")
		self.hostname = hostname
		self.port = port
		self.Joueur_connecté = Joueur_connecté

	def start(self):
		self.logger.debug("Ecoute port "+ str(self.hostname) +":"+ str(self.port))
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(1)

		while True:
			conn, address = self.socket.accept()
			self.logger.debug("Connection entrante")
						
			self.logger.debug("Création du joueur...")
			parent_conn, child_conn = Pipe()
			
			Nouveau_Joueur = classe.Joueur(parent_conn)
			
			self.Joueur_connecté.append(Nouveau_Joueur)
			
			process = multiprocessing.Process(target=handle, args=(conn, address, child_conn, Nouveau_Joueur))
			process.daemon = True
			process.start()
			self.logger.debug("Processus fils démarré %r", process)
