#!/usr/bin/env python3
# coding: utf-8

import pygame, time
from pygame.locals import *

import res_zip

pygame.init()

#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((640, 480))

pygame.key.set_repeat(400, 30)

Fichier_texture = res_zip.ressourceFile("res.zip")

#Chargement et collage du fond
fond = Fichier_texture.get_texture("res/background.jpg").convert()
fenetre.blit(fond, (0,0))

#Chargement et collage du personnage
perso = Fichier_texture.get_texture("res/perso.png").convert_alpha()
position_perso = perso.get_rect()
fenetre.blit(perso, position_perso)

#Rafraîchissement de l'écran
pygame.display.flip()

debut = time.time()
cpt = 0

#BOUCLE INFINIE
continuer = 1
while continuer:
	for event in pygame.event.get():	#Attente des événements
		if event.type == QUIT:
			continuer = 0
		if event.type == KEYDOWN:
			if event.key == K_DOWN:	#Si "flèche bas"
				#On descend le perso
				position_perso = position_perso.move(0,3)
			if event.key == K_UP:
				#On descend le perso
				position_perso = position_perso.move(0,-3)
			if event.key == K_RIGHT:
				#On descend le perso
				position_perso = position_perso.move(3,0)
			if event.key == K_LEFT:
				#On descend le perso
				position_perso = position_perso.move(-3,0)
	
	#Re-collage
	fenetre.blit(fond, (0,0))	
	fenetre.blit(perso, position_perso)
	#Rafraichissement
	pygame.display.flip()
	cpt += 1
