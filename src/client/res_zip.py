#!/usr/bin/env python3
# coding: utf-8

import zipfile, glob, pygame
from io import BytesIO

class ressourceFile():
	
	def __init__(self, path):
		self.zipFile = zipfile.ZipFile(path)
		self.file_list = self.zipFile.namelist()
		
	def get_file(self, filename):
		data = self.zipFile.read(filename)
		data_io = BytesIO(data)
		return(data_io)

	def get_texture(self, filename):
		data = self.get_file(filename)

		try: surf = pygame.image.load(data, filename)
		except: pass
		
		return(surf)
