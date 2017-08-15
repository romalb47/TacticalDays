#!/usr/bin/env python3
# coding: utf-8 

from multiprocessing import Lock
import uuid as UUID

class instance_game():
	
	def __init__(self, uuid, password=""):
		self.lock = Lock()
		self.joueur_actif = []
		self.uuid = uuid
		self.mqtt_topic = "tacticaldays/" + str(UUID.uuid4())
		self.password = password
		
		
	def add(self, Joueur):
		self.joueur_actif.append(Joueur)
		
	def update(self):
		pass
		
		
