#!/usr/bin/env python3
# coding: utf-8

import config
import maps
import ressource
import entity
import divers
import logging
import random
import uuid as UUID

from pygame.locals import *
import pygame
import time


def run(Display, network, map_name):
	
	Map_Data = maps.load_map(map_name)

	Pos_Ecran_Actuelle = [0, 0]

	Size = (Map_Data["size"][0]*32, Map_Data["size"][1]*32)

	Maps_Surface = pygame.Surface(Size)
	
	ScreenSize = Display.get_rect()
	Menu_Width = 0

	pos_curs = (50, 50)
	
	Default_Sprite = entity.Sprite(pygame.Surface((32, 32)))

	Scheduler = pygame.time.Clock()
	
	logging.info("Tentative de connection...")
		
	while True:
		if network.loginok:
			break
		time.sleep(0.1)
	
	logging.info("Connection ok...")
	
	network.join_room("serdtfyugiohjpk")
	
	while True:
		if network.room_joined:
			break
		time.sleep(0.1)

	network.create_entity(1, network.player_uuid, UUID.uuid4(), (random.randint(0, 10), random.randint(0, 10)))
	network.create_entity(1, network.player_uuid, UUID.uuid4(), (random.randint(0, 10), random.randint(0, 10)))

	
	logging.info("Lancement de la bouble principale...")

	Sprite_cliqué = False
	GameRun = True
	while GameRun:
		
		for event in pygame.event.get():	#Attente des événements
			if event.type == MOUSEMOTION:
				pos_curs = event.pos
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					clic_x = event.pos[0]
					clic_y = event.pos[1]
					bloc_x = (Pos_Ecran_Actuelle[0] + clic_x) // 32
					bloc_y = (Pos_Ecran_Actuelle[1] + clic_y) // 32
					Sprite_cliqué = False
					for Player in network.Player_list.values():
						for sprite in Player.Entity:
							sprite_x = sprite.rect.x//32
							sprite_y = sprite.rect.y//32
							if sprite_x==bloc_x and sprite_y==bloc_y:
								Sprite_cliqué = sprite
								logging.debug("Entitée cliqué: %s %s %s"%(bloc_x, bloc_y, Sprite_cliqué))
								break
				if event.button == 3:
					clic_x = event.pos[0]
					clic_y = event.pos[1]
					bloc_x = (Pos_Ecran_Actuelle[0] + clic_x) // 32
					bloc_y = (Pos_Ecran_Actuelle[1] + clic_y) // 32
					if Sprite_cliqué:
						network.move_entity(Sprite_cliqué, (bloc_x, bloc_y))
						logging.debug("Entitée déplacé: %s %s %s"%(bloc_x, bloc_y, Sprite_cliqué))

							
			if event.type == QUIT:
				logging.info("Demande de fermeture...")
				GameRun = False
			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (-15, 0))
				if event.key == K_RIGHT:
					divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (15, 0))
				if event.key == K_UP:
					divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (0, -15))
				if event.key == K_DOWN:
					divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (0, 15))
				if event.key == K_s:
					maps.save_map(map_name, Map_Data)

		if pos_curs[0] < 10:
			divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (-5, 0))
		if pos_curs[0] > config.CFG["screen.size"][0]-10:
			divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (5, 0))
		if pos_curs[1] < 10:
			divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (0, -5))
		if pos_curs[1] > config.CFG["screen.size"][1]-10:
			divers.move_screen(Pos_Ecran_Actuelle, Size, ScreenSize, Menu_Width*32, (0, 5))

		y=0
		for y in range(0, Map_Data["size"][1]):
			for x in range(0, Map_Data["size"][0]):
				try:
					sprite = ressource.SPRITE[ Map_Data["data"][y][x] ]
				except Exception:
					sprite = Default_Sprite
				
				Maps_Surface.blit(sprite.image, (x*32, y*32))

		
		for Player in network.Player_list.values():
			Player.Entity.draw(Maps_Surface)
		
				
		Pos_inversé = (-Pos_Ecran_Actuelle[0], -Pos_Ecran_Actuelle[1])
		Display.blit(Maps_Surface, Pos_inversé)
		
		
		Scheduler.tick_busy_loop(int(config.CFG["screen.fps"]))

		pygame.display.flip()
		Maps_Surface.fill(0)
		Display.fill(0)
