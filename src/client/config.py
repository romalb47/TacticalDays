#!/usr/bin/env python3
# coding: utf-8

import json

CFG = {}

def load_config(filename):
	global CFG
	with open(filename, "r") as f:
		CFG = json.load(f)

def save_config(filename):
	global CFG
	with open(filename, "w") as f:
		CFG = json.dump(CONFIG, f)
