#!/usr/bin/env python3
# coding: utf-8 

from multiprocessing import Lock

class instance_game():
	
	def __init__(self, uuid, password=""):
		self.lock = Lock()
		self.joueur_actif = []
		self.uuid = uuid
		self.password = password
		
		
	def add(self, Joueur):
		self.joueur_actif.append(Joueur)
		
	def update(self):
		pass
		
		
