#!/usr/bin/env python3
# coding: utf-8

import config
import maps
import ressource
import entity

from pygame.locals import *
import pygame


def run(Display, map_name):
	
	Map_Data = maps.load_map(map_name)

	Pos_Ecran_Actuelle = [0, 0]

	Size = (Map_Data["size"][0]*32, Map_Data["size"][1]*32)

	Maps_Surface = pygame.Surface(Size)

	pos_curs = (0, 0)
	
	Default_Sprite = entity.Sprite(pygame.Surface((32, 32)))

	Scheduler = pygame.time.Clock()

	SpriteGroup = entity.EntityGroup()
	
	temp = ressource.ENTITY[1].copy()
	temp.setpos(1, 1)
	SpriteGroup.add( temp )
	
	temp = ressource.ENTITY[2].copy()
	temp.setpos(2, 9)
	SpriteGroup.add( temp )
	
	temp = ressource.ENTITY[3].copy()
	temp.setpos(9, 5)
	SpriteGroup.add( temp )
	
	temp = ressource.ENTITY[4].copy()
	temp.setpos(5, 7)
	SpriteGroup.add( temp )
	
	temp = ressource.ENTITY[5].copy()
	temp.setpos(7, 5)
	SpriteGroup.add( temp )


	GameRun = True
	while GameRun:
		
		for event in pygame.event.get():	#Attente des événements
			if event.type == MOUSEMOTION:
				pos_curs = event.pos				
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

		if pos_curs[0] < 10:
			Pos_Ecran_Actuelle[0] -= 3
		if pos_curs[0] > config.CFG["screen.size"][0]-10:
			Pos_Ecran_Actuelle[0] += 3
		if pos_curs[1] < 10:
			Pos_Ecran_Actuelle[1] -= 3
		if pos_curs[1] > config.CFG["screen.size"][1]-10:
			Pos_Ecran_Actuelle[1] += 3

		y=0
		for y in range(0, Map_Data["size"][1]):
			for x in range(0, Map_Data["size"][0]):
				try:
					sprite = ressource.SPRITE[ Map_Data["data"][y][x] ]
				except Exception:
					sprite = Default_Sprite
				
				Maps_Surface.blit(sprite.image, (x*32, y*32))

		
		
		SpriteGroup.draw(Maps_Surface)
		
				
		Pos_inversé = (-Pos_Ecran_Actuelle[0], -Pos_Ecran_Actuelle[1])
		Display.blit(Maps_Surface, Pos_inversé)
		
		Scheduler.tick_busy_loop(int(config.CFG["screen.fps"]))
		pygame.display.flip()
		Maps_Surface.fill(0)
		Display.fill(0)
