#!/usr/bin/env python3
# coding: utf-8 

import time
import instance
import logging

JOUEUR_CONNECTE = []
INSTANCE_JEU = []

def run(): # Récupere les pipe des client et demarre les instances a la demande
	global JOUEUR_CONNECTE, INSTANCE_JEU
	logger = logging.getLogger("matchmaking")
	
	while True:
		for Joueur in JOUEUR_CONNECTE:
			if not Joueur.islogin:
				continue
							
			if Joueur.tcp_pipe.poll(): # Le joueur a des donnée en attente
				data = Joueur.tcp_pipe.recv()
				logger.debug("Reception de données de %s : %s"%(Joueur.name, str(data)))
				if data["cmd"] == "join_room":
					room_uuid = data["uuid"]
					room_pwd = data["pwd"]
					
					
					for Instance in INSTANCE_JEU:
						if room_uuid == Instance.uuid and room_pwd == Instance.password:
							logger.info("Transfere de %s dans l'instance %s"%(Joueur.name, room_uuid))
							Joueur.in_room = room_uuid
							Joueur.instance = Instance
							Instance.add(Joueur)
							
							Joueur.tcp_pipe.send({"cmd":"join_room", "status":"ok", "server":("192.168.40.236", 1883), "topic":Instance.mqtt_topic})
							
							break
					
					if not Joueur.in_room:
						logger.info("Création l'instance %s pour %s"%(room_uuid, Joueur.name))
						nouvelle_instance = instance.instance_game(room_uuid, room_pwd)
						Joueur.in_room = room_uuid
						Joueur.instance = nouvelle_instance
						nouvelle_instance.add(Joueur)
						INSTANCE_JEU.append(nouvelle_instance)
						Joueur.tcp_pipe.send({"cmd":"join_room", "status":"ok", "server":("192.168.40.236", 1883), "topic":nouvelle_instance.mqtt_topic})

	
		time.sleep(1)

