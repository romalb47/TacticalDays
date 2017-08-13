#!/usr/bin/env python3
# coding: utf-8

import pygame, time
from pygame.locals import *
import random
import logging
import sys, os, multiprocessing

import config
import game
import ressource
import maps_edit
import network


def init_game():
	"""Initialisation de la partie applicative"""
		
	logging.basicConfig(level=logging.DEBUG)

	logging.info("Chargement de la configuration...")
	config.load_config("config.json")
	
	
def init_graph():
	"""Initialisation de la partie graphique"""
	
	pygame.init() # Initialisation de pygame
	
	logging.info("Initialisation de pygame...")
	Screen = pygame.display.set_mode( config.CFG["screen.size"] )
	
	pygame.key.set_repeat(100, 20)
	
	logging.info("Chargement des ressources...")
	ressource.load_sprite_from_folder("data")
	ressource.load_entity_from_folder("data")
	
	return(Screen)
	


if __name__ == "__main__":
	"""Tâche principale"""
		
	init_game()

	Display = init_graph()
	
	logging.info("Lancement du jeu...")
	
	if len(sys.argv) > 1 :
		map_name = sys.argv[1]
	else:
		map_name = "pierre"
	
	maps_edit.run(Display, map_name, (int(sys.argv[2]), int(sys.argv[3])))


	
#	logging.info("Connection...")
#	net = network.network_conn("localhost", 9000)

#	game.run(Display, net, map_name)
	
	
#	net.close()

	logging.info("Jeux fini!")
	

"""


pygame.init()

pygame.key.set_repeat(100, 100)
pygame.mouse.set_visible(False)

fenetre = pygame.display.set_mode( (640, 480) )

Nbr_Bloc_x = 640/16
Nbr_Bloc_y = 480/16

Fichier_texture = res_zip.ressourceFile("res.zip")

textures = []

curseur = Fichier_texture.get_texture("res/curseur.png").convert_alpha()

textures.append( Fichier_texture.get_texture("res/pierre.png").convert_alpha() )
textures.append( Fichier_texture.get_texture("res/sable.png").convert_alpha() )
textures.append( Fichier_texture.get_texture("res/terre.png").convert_alpha() )

pika = Fichier_texture.get_texture("res/pika.png").convert_alpha()
coord_pika = pika.get_rect()
chat = Fichier_texture.get_texture("res/chat.png").convert_alpha()
coord_chat = chat.get_rect()
coord_chat = coord_chat.move(16*39, 16*28)

carte = []
y=0
while y < Nbr_Bloc_y:
	x=0
	carte.append([])
	while x < Nbr_Bloc_x:
		ordre_texture = random.randint(0, len(textures)-1 )
		carte[y].append(ordre_texture)
		x += 1
	y +=1

compteur = 0
pos_curs = (640, 480)
#BOUCLE INFINIE
continuer = 1
while continuer:
	for event in pygame.event.get():	#Attente des événements
		if event.type == MOUSEMOTION:
			print (str(event.pos))
			pos_curs = event.pos
		if event.type == QUIT:
			continuer = 0
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				coord_pika = coord_pika.move(-16, 0)
			if event.key == K_RIGHT:
				coord_pika = coord_pika.move(16, 0)
			if event.key == K_UP:
				coord_pika = coord_pika.move(0, -16)
			if event.key == K_DOWN:
				coord_pika = coord_pika.move(0, 16)
			if event.key == K_q:
				coord_chat = coord_chat.move(-16, 0)
			if event.key == K_d:
				coord_chat = coord_chat.move(16, 0)
			if event.key == K_z:
				coord_chat = coord_chat.move(0, -16)
			if event.key == K_s:
				coord_chat = coord_chat.move(0, 16)

	if compteur > 3:	
		compteur = 0	
		if coord_chat.x > coord_pika.x:
			coord_chat = coord_chat.move(-16, 0)
		if coord_chat.x < coord_pika.x:
			coord_chat = coord_chat.move(16, 0)
		if coord_chat.y > coord_pika.y:
			coord_chat = coord_chat.move(0, -16)
		if coord_chat.y < coord_pika.y:
			coord_chat = coord_chat.move(0, 16)
				
	compteur += 1			
	
	# Code d'affichage!
	
	
	y=0
	while y < Nbr_Bloc_y:
		x=0
		while x < Nbr_Bloc_x:
			ordre_texture = carte[y][x]
			
			fenetre.blit(textures[ordre_texture], (x*16, y*16))

			x += 1
		y +=1
	
	
	fenetre.blit(chat, coord_chat)
	fenetre.blit(pika, coord_pika)

	fenetre.blit(curseur, pos_curs)
	
	# ----------
	
	#Rafraichissement
	pygame.display.flip()
	fenetre.fill(0)
	time.sleep(0.05)
"""
