#!/usr/bin/env python3
# coding: utf-8

def move_screen(to_move, limit, screen_size, menu_size, move):

	if limit[0] > (screen_size.width-menu_size):
		if to_move[0]+move[0] <= 0:
			to_move[0] = 0
			
		if to_move[0]+move[0] > 0:
			to_move[0] += move[0]

		if to_move[0]+move[0] >= limit[0]-(screen_size.width-menu_size):
			to_move[0] = limit[0]-(screen_size.width-menu_size)


	if limit[1] > screen_size.height:
		if to_move[1]+move[1] <= 0:
			to_move[1] = 0
			
		if to_move[1]+move[1] > 0:
			to_move[1] += move[1]

		if to_move[1]+move[1] >= limit[1]-screen_size.height:
			to_move[1] = limit[1]-screen_size.height
				
	return True
