#!/usr/bin/env python3
# coding: utf-8 

class Joueur():
	def __init__(self, pipe):
		self.tcp_pipe = pipe
		self.uuid = 0
		self.name = ""
		self.islogin = False
		self.login_error = 0
		self.in_room = 0
		self.instance = 0
