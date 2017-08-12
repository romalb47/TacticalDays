#!/usr/bin/env python3
# coding: utf-8

import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, surface):
       pygame.sprite.Sprite.__init__(self)

       self.image = surface

       self.rect = self.image.get_rect()


class EntityGroup(pygame.sprite.Group):
	
	def __init__(self):
		pygame.sprite.Group.__init__(self)
