#!/usr/bin/env python3
# coding: utf-8 

import json
import hashlib, time

def do_login(logger, Joueur, packet):
	
	login_file = open("login.json", "r")
	
	login_data = json.load(login_file)
	
	if packet["user"] in login_data:
		temp = login_data[packet["user"]] + str(int(time.time()/10))
		passwd = hashlib.sha224(temp.encode("utf-8")).hexdigest()
		if passwd == packet["pwd"]:
			Joueur.name = packet["user"]
			Joueur.islogin = True
			Joueur.uuid = "secdvfbyuiopvz15"
			logger.debug("Login OK %s, UUID=%s", Joueur.name, Joueur.uuid)
			return True

	return False
