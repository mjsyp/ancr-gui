from Tkinter import *

class Manager:
  
	def __init__(self, parent):
		self.parent = parent
		self.systems = []
		self.types = ["Hello", "World"]

	def addSystem(self, system):
		self.systems.append(system)

	def searchSystems(self, system):
		for x in self.systems:
			if x == system:
				return true
		return false

	def addType(self, typeIn):
		self.types.append(typeIn)

	def searchTypes(self, typeIn):
		for x in self.types:
			if x == typeIn:
				return true
		return false


