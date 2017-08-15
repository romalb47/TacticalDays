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
import paho.mqtt.client as mqtt
from multiprocessing import Pipe

import ressource
import entity

class CPlayer():
	def __init__(self, uuid):
		self.uuid = uuid
		self.Entity = entity.EntityGroup()


class network_conn():
	
	def __init__(self, address, port=9000):
		self.logger = logging.getLogger("network")
		self.address = address
		self.port = port
		self.player_uuid = ""
		self.loginok = False
		self.room_joined = False
		self.mqtt = mqtt.Client()
		self.pipe = start(self.address, self.port)
		self.Player_list = {}
	
	def login(self, login, password):
		temp = password + str(int(time.time()/10))
		passwd = hashlib.sha224(temp.encode("utf-8")).hexdigest()
		packet = {"cmd":"login", "user":login, "pwd":passwd}
		self.pipe.send(packet)
		
	def join_room(self, room_uuid, passwd=""):
		packet = {"cmd":"join_room", "uuid":room_uuid, "pwd":passwd}
		self.pipe.send(packet)
		
	def _mqtt_on_connect(self, client, userdata, flags, rc):
		self.logger.info("MQTT Connected!")
		self.logger.info("MQTT Subscrib to %s", self.room_uuid)
		self.mqtt.subscribe(self.room_uuid)
		self.mqtt.publish(self.room_uuid, '{ "info":"player_connected", "uuid":"%s" }'%(self.player_uuid, )) # Envoi d'un message sur le salon prevenant de mon arrivée
		self.Player_list[self.player_uuid] = CPlayer(self.player_uuid) # Création du joueur en lui meme
		self.room_joined = True
		
	def _mqtt_on_message(self, client, userdata, msg):
		data = json.loads(msg.payload.decode("utf-8"))
		self.logger.debug("MQTT Message: %s", data)
		
		if "info" in data:
			if data["info"] == "player_connected":
				self.mqtt.publish(self.room_uuid, '{ "info":"player_present", "uuid":"%s" }'%(self.player_uuid, ))
			if data["info"] == "player_present":
				if data["uuid"] not in self.Player_list:
					self.logger.debug("Ajout d'un joueur: %s", data["uuid"])
					self.Player_list[data["uuid"]] = CPlayer(data["uuid"])
		if "cmd" in data:
			if data["cmd"] == "entity_move":
				for Player in self.Player_list.values():
					for Entity in Player.Entity:
						if Entity.uuid == data["entity"]: #TODO Vérifié que le mouvement est valide
#							if Player == self.Player_list[self.player_uuid]:
#								break
							self.logger.debug("R: Deplacement de %s a %s", data["entity"], data["pos"])
							Entity.setpos(*data["pos"])


	def move_entity(self, entity, pos=(0, 0)):
		for Player in self.Player_list.values():
			for Entity in Player.Entity:
				if Entity == entity: #TODO Vérifié que le mouvement est valide
					self.logger.debug("S: Deplacement de %s a %s", Entity.uuid, (pos[0], pos[1]))
					self.mqtt.publish(self.room_uuid, '{ "cmd":"entity_move", "from":"%s", "entity":"%s", "pos": [%s, %s] }'%(self.player_uuid, Entity.uuid, pos[0], pos[1])) # Envoi du deplacement
					Entity.setpos(pos[0], pos[1])
		
	def create_entity(self, ID, Joueur_uuid, Entity_uuid="", pos=(0, 0)):
		New_Entity = ressource.ENTITY[ID].copy(Entity_uuid)
		New_Entity.setpos(pos[0], pos[1])
		self.Player_list[Joueur_uuid].Entity.add(New_Entity)
		
		
	def process_pipe(self):
		if not self.pipe_has_data():
			return False
		
		data = self.pipe.recv()
		
		self.logger.debug("Recv data: %s"%(data, ))
		
		if data["cmd"] == "login":
			if data["status"] == "ok":
				self.loginok = True
				self.player_uuid = data["uuid"]
				self.logger.info("Login OK")
				return "login_ok"
			if data["status"] == "nok":
				self.loginok = False
				self.logger.error("Login Error")
				return "login_nok"
		
		if data["cmd"] == "join_room":
			if data["status"] == "ok":
				self.mqtt.on_connect = self._mqtt_on_connect
				self.mqtt.on_message = self._mqtt_on_message
				self.mqtt.connect(data["server"][0], data["server"][1], 60)
				self.mqtt.loop_start()
				self.room_uuid = data["topic"]
				self.logger.info("Starting MQTT loop")
				return "room_ok"
			if data["status"] == "nok":
				self.room_joined = False
				return "room_nok"
		
	def pipe_has_data(self):
		return self.pipe.poll()

	def close(self):
		self.pipe.send({"cmd":"close"})
		self.mqtt.disconnect()
		self.mqtt.loop_stop()
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
