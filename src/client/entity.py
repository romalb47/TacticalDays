#!/usr/bin/env python3
# coding: utf-8

import pygame
import random

class Entity(pygame.sprite.Sprite):

	def __init__(self, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.data = ""
		
		self.uuid = random.randint(0, 999999999999)

		self.image = surface
		self.alternate = []

		self.rect = self.image.get_rect()
		
		self.pos = [0, 0]
	
	def copy(self):
		new = Entity(self.image.copy())
		new.data = self.data
		return new
		
	def setpos(self, x, y):
		self.pos = [x, y]
		self.rect.x = x*32
		self.rect.y = y*32

class Sprite(pygame.sprite.Sprite):

	def __init__(self, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.data = ""

		self.image = surface
		self.alternate = []

		self.rect = self.image.get_rect()


class EntityGroup(pygame.sprite.Group):
	pass
"""		
	def __init__(self):
		self.sprite = []
		
	
	def add(self, sprite):
		self.sprite.append(sprite)
		
	def draw(self, surface):
		for s in self.sprite:
			surface.blit(s.image, s.rect)
"""
