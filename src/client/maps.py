#!/usr/bin/env python3
# coding: utf-8

import json

import config



def load_map(name):
	
	with open("maps/" + name + ".json", "r") as f:
		data = json.load(f)
		
	return data
	
	
def save_map(name, carte):
	
	with open("maps/" + name + ".json", "w") as f:
		data = json.dump(carte, f, indent=4)
		
	return True
	
	
def new_maps(size):
	a = {}
	a["size"] = list(size)
	new_list = []
	
	for i in range(0, size[1]):
		new_list.append([])
		for j in range(0, size[0]):
			new_list[i].append(10013)
	
	a["data"] = new_list
	
	return(a)
