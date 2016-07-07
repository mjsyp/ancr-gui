from Tkinter import *

class Manager:
  
	def __init__(self, parent):
		self.parent = parent
		self.systems = []
		self.types = ["Hello", "World"]

	def addSystem(self, system):
		self.systems.append(system)

	def addType(self, typeIn):
		self.types.append(typeIn)


