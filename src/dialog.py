#!/usr/bin/env python
# -*- coding: utf-8 -*-

dialogContent=[
"Hello welcome, please smile",\
"Your smile is good ",\
"Do you want to experience NTU Tour? (y/n) ",\
"Play off NTU Tour (delete)",\
"Your partner is coming",\
"I want to leave bug hole (Esc)",\
"Goodbye",\
"Find your partner by smiling",\
"keep smiling, then bug hole will open"

]##index from 0 to 8

class Dialog:
	def __init__(self):
		pass

	def load(self,index):
		text = dialogContent[index]
		return text