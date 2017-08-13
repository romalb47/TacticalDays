#!/usr/bin/env python3
# coding: utf-8

import config
import maps
import ressource
import entity

from pygame.locals import *
import pygame


def run(Display, map_name, size):
	
	Map_Data = maps.new_maps(size)

	Pos_Ecran_Actuelle = [0, 0]

	Size = (size[0]*32, size[1]*32)
	
	ScreenSize = Display.get_rect()

	Maps_Surface = pygame.Surface(Size)
	
	Menu_Width = int(config.CFG["mapeditor.menu_width"])
	Menu_Surface = pygame.Surface((Menu_Width*32, ScreenSize.height))
	Pos_Menu_Surface = Menu_Surface.get_rect()
	Pos_Menu_Surface.x = ScreenSize.width - Menu_Width*32

	pos_curs = (0, 0)

	Scheduler = pygame.time.Clock()

	SpriteGroup = entity.EntityGroup()

	ListeSprite = []
	Position = 0
	for Sp_i in sorted(ressource.SPRITE):
		if Sp_i < 1000:
			continue
		Sp = ressource.SPRITE[Sp_i]
		Pos_x = (Position%Menu_Width) * 32
		Pos_y = (Position//Menu_Width) * 32
		Position += 1
		Menu_Surface.blit(Sp.image, (Pos_x, Pos_y))
		
		ListeSprite.append({"id":Sp.data["ID"]})

	Texture_Séléctionné = 0

	GameRun = True
	while GameRun:
		
		for event in pygame.event.get():	#Attente des événements
			if event.type == MOUSEMOTION:
				pos_curs = event.pos
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					clic_x = event.pos[0]
					clic_y = event.pos[1]
					
					if clic_x > Pos_Menu_Surface.x: # Si clique dans le menu de gauche
						bloc_x = (clic_x - Pos_Menu_Surface.x) // 32
						bloc_y = (clic_y) // 32
						Texture_Séléctionné = bloc_y*Menu_Width + bloc_x
					if clic_x < Pos_Menu_Surface.x:
						bloc_x = (Pos_Ecran_Actuelle[0] + clic_x) // 32
						bloc_y = (Pos_Ecran_Actuelle[1] + clic_y) // 32
						Id = int(ListeSprite[Texture_Séléctionné]["id"])
						print(str(Map_Data["data"][bloc_y][bloc_x]))

						Map_Data["data"][bloc_y][bloc_x] = Id
						print("Bloc cliqué: %s %s %s"%(bloc_x, bloc_y, Id))
						
			
			if event.type == QUIT:
				GameRun = False
			if event.type == KEYDOWN:
				if event.key == K_LEFT:
					Pos_Ecran_Actuelle[0] -= 3
				if event.key == K_RIGHT:
					Pos_Ecran_Actuelle[0] += 3
				if event.key == K_UP:
					Pos_Ecran_Actuelle[1] -= 3
				if event.key == K_DOWN:
					Pos_Ecran_Actuelle[1] += 3
				if event.key == K_s:
					maps.save_map(map_name, Map_Data)

		if pos_curs[0] < 10:
			Pos_Ecran_Actuelle[0] -= 3
		if pos_curs[0] > config.CFG["screen.size"][0]-10:
			Pos_Ecran_Actuelle[0] += 3
		if pos_curs[1] < 10:
			Pos_Ecran_Actuelle[1] -= 3
		if pos_curs[1] > config.CFG["screen.size"][1]-10:
			Pos_Ecran_Actuelle[1] += 3

		y=0
		while y < Map_Data["size"][1]:
			x=0
			while x < Map_Data["size"][0]:
				sprite = ressource.SPRITE[ Map_Data["data"][y][x] ]
				Maps_Surface.blit(sprite.image, (x*32, y*32))

				x += 1
			y +=1
		
		
		SpriteGroup.draw(Maps_Surface)
		
		Pos_inversé = (-Pos_Ecran_Actuelle[0], -Pos_Ecran_Actuelle[1])
		Display.blit(Maps_Surface, Pos_inversé)
		
		Display.blit(Menu_Surface, Pos_Menu_Surface)
		
		Scheduler.tick_busy_loop(int(config.CFG["screen.fps"]))
		pygame.display.flip()
		Maps_Surface.fill(0)
		Display.fill(0)
