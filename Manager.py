from Tkinter import *

class Manager:
  
	def __init__(self, parent):
		self.parent = parent
		self.systems = []
		self.types = ["Component", "Compartment", "Create New"]

	def addSystem(self, system):
		self.systems.append(system)

	def addType(self, typeIn):
		self.types.append(typeIn)


