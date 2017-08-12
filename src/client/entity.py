#!/usr/bin/env python3
# coding: utf-8

import pygame

class Entity(pygame.sprite.Sprite):

	def __init__(self, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.data = ""

		self.image = surface

		self.rect = self.image.get_rect()
	
	def copy(self):
		new = Entity(self.image.copy())
		new.data = self.data
		return new

	def move(self, x, y):
		self.rect = self.rect.move(x, y)

class Sprite(pygame.sprite.Sprite):

	def __init__(self, surface):
		pygame.sprite.Sprite.__init__(self)
		
		self.data = ""

		self.image = surface

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
