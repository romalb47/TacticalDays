#!/usr/bin/env python3
# coding: utf-8

import config
import maps
import ressource
import entity

from pygame.locals import *
import pygame


def run(Display):

	pos_curs = (0, 0)

	Scheduler = pygame.time.Clock()

	GameRun = True
	while GameRun:
		
		for event in pygame.event.get():	#Attente des événements
			if event.type == MOUSEMOTION:
				pos_curs = event.pos				
			if event.type == QUIT:
				GameRun = False

		
		Scheduler.tick_busy_loop(int(config.CFG["screen.fps"]))
		pygame.display.flip()
		Maps_Surface.fill(0)
		Display.fill(0)
