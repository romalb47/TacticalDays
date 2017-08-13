#!/usr/bin/env python3
# coding: utf-8

import pygame
import pathlib
import logging
import json

import res_zip
import entity

SPRITE = {}
ENTITY = {}

def load_sprite_from_file(filename):
	global SPRITE
	zipFile = res_zip.ressourceFile(filename)
	
	for f in zipFile.file_list: # Pour tout les fichier du zip
		if f.endswith(".json"): # Si fini par json
			img = f[:-4] + "png"
			if img in zipFile.file_list: # Et qu'il y a une ressource associé
				try:
					logging.info("Chargement de "+str(f))
					surface = zipFile.get_texture(img)
					new_entity = entity.Sprite(surface)
					data = zipFile.get_file(f).read()
					new_entity.data = json.loads(data.decode())
					SPRITE[new_entity.data["ID"]] = new_entity
				except Exception:
					logging.error("Erreur de chargement de "+str(f))
					continue
				

def load_sprite_from_folder(path = '.'):
	logging.info("Chargement des sprites...")
	liste = sorted(pathlib.Path(path).glob('*.szip'))
	for entry in liste:
		logging.info("Ouverture de "+str(entry.name))
		load_sprite_from_file(str(entry))
	
def load_entity_from_file(filename):
	global ENTITY
	zipFile = res_zip.ressourceFile(filename)
	
	for f in zipFile.file_list: # Pour tout les fichier du zip
		if f.endswith(".json"): # Si fini par json
			img = f[:-4] + "png"
			if img in zipFile.file_list: # Et qu'il y a une ressource associé
				try:
					logging.info("Chargement de "+str(f))
					surface = zipFile.get_texture(img)
					new_entity = entity.Entity(surface)
					data = zipFile.get_file(f).read()
					new_entity.data = json.loads(data.decode())
					ENTITY[new_entity.data["ID"]] = new_entity
				except Exception:
					logging.error("Erreur de chargement de "+str(f))
					continue

def load_entity_from_folder(path = '.'):
	logging.info("Chargement des entitées...")
	liste = sorted(pathlib.Path(path).glob('*.ezip'))
	for entry in liste:
		logging.info("Ouverture de "+str(entry.name))
		load_entity_from_file(str(entry))
	
	
