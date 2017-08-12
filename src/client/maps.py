#!/usr/bin/env python3
# coding: utf-8

import json

import config



def load_map(name):
	
	with open("maps/" + name + ".json", "r") as f:
		data = json.load(f)
		
	return data
	
	
	
