#!/usr/bin/env python3
# coding: utf-8 

import json

def do_login(logger, Joueur, packet):
	
	login_file = open("login.json", "r")
	
	login_data = json.load(login_file)
	
	if packet["user"] in login_data:	
		if login_data[packet["user"]] == packet["pwd"]:
			Joueur.name = packet["user"]
			Joueur.uuid = "secdvfbyuiopvz15"
			logger.debug("Login OK %s, UUID=%s", Joueur.name, Joueur.uuid)
			return True

	return False
