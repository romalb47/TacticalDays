#!/usr/bin/env python3
# coding: utf-8

import json

import config
import logging


def load_map(name):
	try:
		with open("maps/" + name + ".json", "r") as f:
			data = json.load(f)
			logging.info("Chargements de la carte "+str(name))
	except Exception:
		return False
	return data
	
	
def save_map(name, carte):
	
	with open("maps/" + name + ".json", "w") as f:
		data = json.dump(carte, f, indent=4)
		logging.info("Sauvegarde de la carte "+str(name))
		
	return True
	
	
def new_maps(size):
	a = {}
	a["size"] = list(size)
	new_list = []
	
	for i in range(0, size[1]):
		new_list.append([])
		for j in range(0, size[0]):
			new_list[i].append(10013)
	
	a["data"] = new_list
	
	return(a)
