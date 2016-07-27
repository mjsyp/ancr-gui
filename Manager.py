'''
 * Manager.py
 * 
 * Keeps track of all of the systems and types
 * that have been specified
'''
from Tkinter import *

class Manager:
  
	def __init__(self, parent):
		self.parent = parent
		self.systems = []
		self.nodeTypes = ["Component", "Compartment"]
		self.edgeTypes = ["Adjacency", "Residency", "Supply/Demand"]

	def addSystem(self, system):
		self.systems.append(system)

	def addType(self, typeIn):
		self.types.append(typeIn)


