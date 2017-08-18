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
import uuid as UUID
import paho.mqtt.client as mqtt
from multiprocessing import Pipe

import ressource
import entity

class CPlayer():
	def __init__(self, uuid):
		self.uuid = uuid
		self.name = ""
		self.Entity = entity.EntityGroup()

class network_conn():
	
	def __init__(self, server):
		self.logger = logging.getLogger("network")
		self.server = server
		self.player_uuid = str(UUID.uuid4())
		self.topic = "tacticaldays/"
		self.loginok = False
		self.room_joined =  False
		self.room_uuid = ""
		self.name = ""
		self.Player_list = {}
		self.mqtt = mqtt.Client()
#		self.mqtt.enable_logger(logging.getLogger("MQTT"))
	
	def login(self, login="", password=""):
		if login != "":
			self.mqtt.username_pw_set(username=login,password=password)
		self.name = login
		self.mqtt.on_connect = self._mqtt_on_connect
		self.mqtt.on_message = self._mqtt_on_message
		self.logger.debug("MQTT Connection lancée: %s %s", self.server[0], self.server[1])
		self.mqtt.connect_async(self.server[0], self.server[1], 60)
		self.logger.info("Starting MQTT loop")
		self.mqtt.loop_start()

	def close(self):
		self.mqtt.disconnect()
		self.mqtt.loop_stop()

	def _mqtt_on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			self.logger.info("MQTT Connected!")
			self.loginok = True
		else:
			self.logger.error("MQTT Erreur de connection! (%s)", rc)
			self.loginok = False
		
	def _mqtt_on_message(self, client, userdata, msg):
		data = json.loads(msg.payload.decode("utf-8"))
		self.logger.debug("MQTT Message: %s", data)
		
		if "info" in data:
			if data["info"] == "player_connected":
				self.mqtt.publish(self.room_uuid, '{ "info":"player_present", "uuid":"%s", "name":"%s"}'%(self.player_uuid, self.Player_list[self.player_uuid].name))
			if data["info"] == "player_present":
				if data["uuid"] not in self.Player_list:
					self.logger.debug("Ajout d'un joueur: %s t(%s)", data["name"], data["uuid"])
					self.Player_list[data["uuid"]] = CPlayer(data["uuid"])
					self.Player_list[data["uuid"]].name = data["name"]
		if "cmd" in data:
			if data["cmd"] == "entity_move":
				for Player in self.Player_list.values():
					for Entity in Player.Entity:
						if Entity.uuid == data["entity"]: #TODO Vérifié que le mouvement est valide
							#if Player == self.Player_list[self.player_uuid]:
								#self.logger.debug("Tentative de deplacement de mon unité %s de %s", data["entity"], self.Player_list[data["from"]].name)
								#break
							self.logger.debug("R: Deplacement de %s a %s", data["entity"], data["pos"])
							Entity.setpos(*data["pos"])
			if data["cmd"] == "entity_create":
				New_Entity = ressource.ENTITY[data["ID"]].copy(data["entity"])
				New_Entity.setpos(*data["pos"])
				self.Player_list[data["from"]].Entity.add(New_Entity)
				self.logger.debug("R: Création de l'entité %s a %s appartenant a %s", data["entity"], data["pos"], self.Player_list[data["from"]].name)

	def move_entity(self, entity, pos=(0, 0)):
		self.mqtt.publish(self.room_uuid, '{ "cmd":"entity_move", "from":"%s", "entity":"%s", "pos": [%s, %s] }'%(self.player_uuid, entity.uuid, pos[0], pos[1])) # Envoi du deplacement
		
	def create_entity(self, ID, Joueur_uuid, Entity_uuid="", pos=(0, 0)):
		self.mqtt.publish(self.room_uuid, '{ "cmd":"entity_create", "from":"%s", "entity":"%s", "ID": %s, "pos": [%s, %s] }'%(Joueur_uuid, Entity_uuid, ID, pos[0], pos[1])) # Envoi de la création

		
	def join_room(self, room_uuid):
		if self.room_uuid != "":
			self.mqtt.publish(self.room_uuid, '{ "info":"player_disconnected", "uuid":"%s"}'%(self.player_uuid, ))
			self.mqtt.unsubscribe(self.room_uuid)
		self.room_uuid = self.topic+room_uuid
		self.logger.info("MQTT Subscrib to %s", self.room_uuid)
		self.mqtt.subscribe(self.room_uuid)
		self.mqtt.publish(self.room_uuid, '{ "info":"player_connected", "uuid":"%s", "name":"%s" }'%(self.player_uuid, self.name)) # Envoi d'un message sur le salon prevenant de mon arrivée
		self.Player_list[self.player_uuid] = CPlayer(self.player_uuid) # Création du joueur en lui meme
		self.Player_list[self.player_uuid].name = self.name
		self.room_joined = True
		

