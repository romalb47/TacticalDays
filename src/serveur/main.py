#!/usr/bin/env python3
# coding: utf-8 

import multiprocessing

import classe
import instance
import matchmaking
import login
import network

if __name__ == "__main__":
	import logging
	logging.basicConfig(level=logging.DEBUG)
	
	Joueur_connecté = [] # Structure principale stockant les joueur en attente
	
	server = network.Server("0.0.0.0", 9000, Joueur_connecté)
	try:
		logging.info("Démarrage du serveur")
		server.start()
	except:
		logging.exception("Exception inconnue")
	finally:
		logging.info("Arrêt du serveur")
		for process in multiprocessing.active_children():
			logging.info("Arrêt des processus fils %r", process)
			process.terminate()
			process.join()
	logging.info("Terminé")
