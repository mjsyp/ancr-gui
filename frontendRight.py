from Tkinter import *
import tkSimpleDialog
import networkx as nx

class FrontendRight(Frame):
	def __init__(self, parent, nodeIndex, G, systemList):
		Frame.__init__(self, parent)

		self.parent = parent
		self.nodeIndex = nodeIndex
		self.G = G

		# sync Demands with toolbar dropdown, but delete "Create New" and "All"
		self.systemList = list(systemList)
		try:
 			self.systemList.remove('Create New')
 			self.systemList.remove('Chill Water')
 			self.systemList.remove('All')
 		except ValueError:
 			pass

		for x in self.G.node[self.nodeIndex]:
			if (x not in ['Name', 'Type', 'x', 'y', 'z'] and x not in systemList):
				self.systemList.append(x)

		# initialize a dictionary where each system = None
		self.systemDict = {}
		for x in self.systemList:
			self.systemDict[x] = None

		self.color = "dark gray"
		self.initUI()

	def createTypeLabel(self):
		self.typeLabel = Label(self.parent, text="Type:", bg=self.color)
		self.typeLabel.grid(row=2, column=0)

		self.typeMenu = Frame(self.parent, highlightbackground=self.color)
		self.typeMenu.grid(row=2, column=1, padx=10)
		self.optionList = ['Hello', 'World']
		self.v = StringVar()
		self.v.set(self.optionList[0])
		self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
		self.dropdown.config(bg=self.color)
		self.dropdown.grid(row=2, column=1)

		self.createTypeBtn = Button(self.parent, text="Create New", 
			command=self.createNewType, highlightbackground=self.color)
		self.createTypeBtn.grid(row=2, column=2)

	def createNewType(self):
		typeLabel = tkSimpleDialog.askstring(title="New Type", prompt="Enter a new type")

		if typeLabel != None:
			self.optionList.append(typeLabel)
			self.v.set(self.optionList[len(self.optionList)-1])
			self.dropdown.grid_forget()
			self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
			self.dropdown.configure(bg=self.color)
			self.dropdown.grid(row=2, column=1)

	def createDemandLabel(self):
		# Demand
 		self.demandLabel = Label(self.parent, text="Demand:", bg=self.color)
 		self.demandLabel.grid(row=3, column=0, padx=5)

		self.createDemandBtn = Button(self.parent, text="Create New", 
			command=self.createNewDemand, highlightbackground=self.color)
		self.createDemandBtn.grid(row=4, column=1)

		self.numDemands = 0

		for x in self.systemList:
			self.createNewDemand(x)

	def createNewDemand(self, label=None):
		if label == None: # prompt for a label if none was provided as a parameter
			label = tkSimpleDialog.askstring(title="Label", prompt="Enter a Label Name") # Prompt for label
			# add new label to systemList
			if label != None: # check for 'Cancel' option
				self.systemList.append(label) # add new system to systemList

		if label != None: # check for 'Cancel' option
			# Create new label and corresponding entry
			self.newDemandLabel = Label(self.parent, text=label, bg=self.color)
			self.newDemandLabel.grid(row=3+self.numDemands, column=1)
			newEntry = Entry(self.parent, highlightbackground=self.color)
			newEntry.grid(row=3+self.numDemands, column=2, padx=10)
			newEntry.insert(0, '0')
			if label not in self.G.node[self.nodeIndex]:
				self.G.node[self.nodeIndex][label] = 0
			self.systemDict[label] = newEntry

			# delete existing buttons/labels
			if hasattr(self, 'createDemandBtn'):
				self.createDemandBtn.grid_forget()
			if hasattr(self, 'geometryLabel'):
				self.geometryLabel.grid_forget()
			if hasattr(self, 'xLabel'):
				self.xLabel.grid_forget()
			if hasattr(self, 'xEntry'):
				self.xEntry.grid_forget()
			if hasattr(self, 'yLabel'):
				self.yLabel.grid_forget()
			if hasattr(self, 'yEntry'):
				self.yEntry.grid_forget()
			if hasattr(self, 'zLabel'):
				self.zLabel.grid_forget()
			if hasattr(self, 'zEntry'):
				self.zEntry.grid_forget()

			# Move down to make room for new demand label
			self.createDemandBtn.grid(row=4+self.numDemands, column=1)
			self.geometryLabel.grid(row=5+self.numDemands, column=0)
			self.xLabel.grid(row=5+self.numDemands, column=1)
			self.xEntry.grid(row=5+self.numDemands, column=2)
			self.yLabel.grid(row=6+self.numDemands, column=1)
			self.yEntry.grid(row=6+self.numDemands, column=2)
			self.zLabel.grid(row=7+self.numDemands, column=1)
			self.zEntry.grid(row=7+self.numDemands, column=2)

			self.numDemands += 1

	def createGeometryLabel(self):
		self.geometryLabel = Label(self.parent, text="Geometry:", bg=self.color)
		self.geometryLabel.grid(row=5, column=0, padx=5)

		self.xLabel = Label(self.parent, text="x", bg=self.color)
		self.xLabel.grid(row=5, column=1, padx=1, pady=1)
		self.xEntry = Entry(self.parent, highlightbackground=self.color)
		self.xEntry.grid(row=5, column=2)

		self.yLabel = Label(self.parent, text="y", bg=self.color)
		self.yLabel.grid(row=6, column=1, padx=1, pady=1)
		self.yEntry = Entry(self.parent, highlightbackground=self.color)
		self.yEntry.grid(row=6, column=2)

		self.zLabel = Label(self.parent, text="z", bg=self.color)
		self.zLabel.grid(row=7, column=1, padx=1, pady=1)
		self.zEntry = Entry(self.parent, highlightbackground=self.color)
		self.zEntry.grid(row=7, column=2)

	def repopulateData(self):
		if 'Name' in self.G.node[self.nodeIndex] and self.G.node[self.nodeIndex]['Name'] != None:
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.node[self.nodeIndex]['Name'])
		if 'Type' in self.G.node[self.nodeIndex] and self.G.node[self.nodeIndex]['Type'] != None:
			self.v.set(self.G.node[self.nodeIndex]['Type'])
		if 'x' in self.G.node[self.nodeIndex]:
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, self.G.node[self.nodeIndex]['x'])
		if 'y' in self.G.node[self.nodeIndex]:
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, self.G.node[self.nodeIndex]['y'])
		if 'z' in self.G.node[self.nodeIndex]:
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, self.G.node[self.nodeIndex]['z'])
		for x in self.systemList:
			self.systemDict[x].delete(0, END)
			self.systemDict[x].insert(0, self.G.node[self.nodeIndex][x])

	def saveAttributes(self):
		self.G.node[self.nodeIndex]['Name'] = self.nameEntry.get()
		self.G.node[self.nodeIndex]['Type'] = self.v.get()
		self.G.node[self.nodeIndex]['x'] = self.xEntry.get()
		self.G.node[self.nodeIndex]['y'] = self.yEntry.get()
		self.G.node[self.nodeIndex]['z'] = self.zEntry.get()

		# Demands
		for x in self.systemList:
			self.G.node[self.nodeIndex][x] = self.systemDict[x].get()

	def initUI(self):
		# Title
		self.title = Label(self.parent, text="Node " + str(self.nodeIndex), bg=self.color)
		self.title.grid(row=0, columnspan=3, sticky=N, pady=10)

		# Name
		self.nameLabel = Label(self.parent, text="Name:", bg=self.color)
		self.nameLabel.grid(row=1, column=0, padx=5)

		self.nameEntry = Entry(self.parent, highlightbackground=self.color)
		self.nameEntry.grid(row=1, column=1, columnspan=2, sticky=E+W, padx=10)

		# Type, Demand, Geometry
		self.createTypeLabel()
		self.createGeometryLabel()
		self.createDemandLabel() # create demand last bc placement relies on type and geometry labels

		# if node attributes have been set previously, populate right pane using the existing data
		self.repopulateData()

		# save button
		self.saveBtn = Button(self.parent, text="Save", command=self.saveAttributes, 
			highlightbackground=self.color)
		self.saveBtn.pack(side="bottom")

