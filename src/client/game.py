#!/usr/bin/env python3
# coding: utf-8

import config
import maps
import ressource

from pygame.locals import *
import pygame


def run(Display, map_name):
	
	Map_Data = maps.load_map(map_name)

	Pos_Ecran_Actuelle = [0, 0]

	Size = (Map_Data["size"][0]*32, Map_Data["size"][1]*32)

	Maps_Surface = pygame.Surface(Size)

	pos_curs = (0, 0)

	Scheduler = pygame.time.Clock()

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

		y=0
		while y < Map_Data["size"][1]:
			x=0
			while x < Map_Data["size"][0]:
				sprite = ressource.SPRITE[ Map_Data["data"][y][x] ]
				Maps_Surface.blit(sprite.image, (x*32, y*32))

				x += 1
			y +=1
				
		Pos_inversé = (Pos_Ecran_Actuelle[0], Pos_Ecran_Actuelle[1])
		Display.blit(Maps_Surface, Pos_inversé)
		
		Scheduler.tick_busy_loop(int(config.CFG["screen.fps"]))
		pygame.display.flip()
		Maps_Surface.fill(0)
		Display.fill(0)
