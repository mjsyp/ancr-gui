from Tkinter import *
import tkSimpleDialog
import networkx as nx
from datetime import datetime

class NodeInfo(Frame):
	def __init__(self, parent, leftFrame, index, G, manager):
		Frame.__init__(self, parent)

		self.parent = parent
		self.leftFrame = leftFrame
		self.index = index
		self.G = G
		self.manager = manager

		self.systemDict = {}
 		self.color = "dark gray" 
		self.initUI()

	def createTypeLabel(self):
		self.typeLabel = Label(self.parent, text="Type:", bg=self.color)
		self.typeLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E)

		# initialize default options in dropdown to the list in our Manager
		self.optionList = self.manager.types

		# Create frame to hold the OptionMenu
		self.typeMenu = Frame(self.parent, bg=self.color)
		self.typeMenu.grid(row=1, column=1, padx=5)

		# create a StringVar that holds the selected option in the dropdown
		self.v = StringVar()
		self.v.set(self.optionList[0])

		# actual dropdown
		self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
		self.dropdown.config(bg=self.color, highlightbackground=self.color)
		self.dropdown.grid(row=1, column=1, pady=5)

		# 'Create New' button
		self.createTypeBtn = Button(self.parent, text="Create New", 
			command=self.createNewType, highlightbackground=self.color)
		self.createTypeBtn.grid(row=1, column=2)

	def createNewType(self):
		typeLabel = tkSimpleDialog.askstring(title="New Type", prompt="Enter a new type")

		if typeLabel != None:
			# add to manager and to list in dropdown
			self.manager.addType(typeLabel)

			# select new 'type' in dropdown
			self.v.set(self.optionList[len(self.optionList)-1])

			# redraw dropdown
			self.dropdown.grid_forget()
			self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
			self.dropdown.config(bg=self.color, highlightbackground=self.color)
			self.dropdown.grid(row=1, column=1, pady=5)

	def createDemandLabel(self):
		# Demand
 		self.demandLabel = Label(self.parent, text="Demand:", bg=self.color, anchor=W)
 		self.demandLabel.grid(row=2, column=0, padx=5, sticky=E)

		self.createDemandBtn = Button(self.parent, text="Create New", 
			command=self.createNewDemand, highlightbackground=self.color)
		self.createDemandBtn.grid(row=2, column=1, pady=5)

		self.numDemands = 0

		for x in self.manager.systems:
			self.createNewDemand(x)

	def createNewDemand(self, label=None):
		# If no label was provided as a parameter, prompt for a label
		if label == None:
			label = tkSimpleDialog.askstring(title="Label", prompt="Enter a Label Name") # Prompt for label
			# If user didn't hit 'Cancel' in dialog window, add new key to manager's systems
			if label != None: 
				self.manager.addSystem(label)
			else:
				return
		
		# Create new label and corresponding entry
		self.newDemandLabel = Label(self.parent, text=label, bg=self.color)
		self.newDemandLabel.grid(row=2+self.numDemands, column=1)
		newEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		newEntry.grid(row=2+self.numDemands, column=2, padx=10)
		self.systemDict[label] = newEntry

		# move widgets down to make room for new demand label
		self.createDemandBtn.grid(row=3+self.numDemands, column=1, pady=5)
		for item in self.parent.grid_slaves():
			if int(item.grid_info()["row"]) > (3 + self.numDemands):
				newRow = int(item.grid_info()["row"]) + self.numDemands + 1
				item.grid_configure(row=newRow)

		self.numDemands += 1

		# add new demand to the main toolbar dropdown
		if label not in self.leftFrame.optionList:
			self.leftFrame.optionList.insert(len(self.leftFrame.optionList)-2, label)
			self.leftFrame.dropdown.destroy()
			self.leftFrame.dropdown = OptionMenu(self.leftFrame.toolbar, self.leftFrame.v, 
				*self.leftFrame.optionList, command=self.leftFrame.newOptionMenu)
			self.leftFrame.dropdown.configure(bg="light blue")
			self.leftFrame.dropdown.pack(side='left')

	def createGeometryLabel(self):
		self.geometryLabel = Label(self.parent, text="Geometry:", bg=self.color, anchor=W)
		self.geometryLabel.grid(row=4, column=0, padx=5, sticky=E)

		self.xLabel = Label(self.parent, text="x", bg=self.color)
		self.xLabel.grid(row=4, column=1, padx=1)
		self.xEntry = Entry(self.parent, highlightbackground=self.color, width=8)
		self.xEntry.grid(row=4, column=2)

		self.yLabel = Label(self.parent, text="y", bg=self.color)
		self.yLabel.grid(row=5, column=1, padx=1)
		self.yEntry = Entry(self.parent, highlightbackground=self.color, width=8)
		self.yEntry.grid(row=5, column=2)

		self.zLabel = Label(self.parent, text="z", bg=self.color)
		self.zLabel.grid(row=6, column=1, padx=1)
		self.zEntry = Entry(self.parent, highlightbackground=self.color, width=8)
		self.zEntry.grid(row=6, column=2)

		# Edge Length Parameter
		self.edgeLabel = Label(self.parent, text="Edge Length", bg=self.color)
		self.edgeLabel.grid(row=7, column=1, padx=1)
		self.edgeEntry = Entry(self.parent, highlightbackground=self.color, width=8)
		self.edgeEntry.grid(row=7, column=2)

	def repopulateData(self):
		if 'Name' in self.G.node[self.index] and self.G.node[self.index]['Name'] != None:
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.node[self.index]['Name'])
		if 'Type' in self.G.node[self.index] and self.G.node[self.index]['Type'] != None:
			self.v.set(self.G.node[self.index]['Type'])
		if 'x' in self.G.node[self.index]:
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, self.G.node[self.index]['x'])
		if 'y' in self.G.node[self.index]:
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, self.G.node[self.index]['y'])
		if 'z' in self.G.node[self.index]:
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, self.G.node[self.index]['z'])
		if 'EdgeLength' in self.G.node[self.index] and self.G.node[self.index]['EdgeLength'] != None:
			self.edgeEntry.delete(0, END)
			self.edgeEntry.insert(0, self.G.node[self.index]['EdgeLength'])
		if 'Notes' in self.G.node[self.index]:
			self.notes.delete('0.0', END)
			self.notes.insert('0.0', self.G.node[self.index]['Notes'])
        
		for x in self.manager.systems:
			if x in self.G.node[self.index]:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.node[self.index][x])

	def updateNodeSizes(self):
		if self.leftFrame.v.get() != 'All' and self.leftFrame.v.get() != 'Create New':
			self.leftFrame.minDemand = 1000000000
			self.leftFrame.maxDemand = -1
			visibleNodes = []

			for nodeitem in self.leftFrame.systemsCanvas.find_withtag('node'):
				if self.leftFrame.v.get() in self.G.node[nodeitem]:
					visibleNodes.append(nodeitem) # add to a list of visible nodes

					# find minimum and maximum values for this demand
					thisDemand = self.G.node[nodeitem][self.leftFrame.v.get()]
					if abs(thisDemand) < self.leftFrame.minDemand:
						self.leftFrame.minDemand = abs(thisDemand)
					if abs(thisDemand) > self.leftFrame.maxDemand:
						self.leftFrame.maxDemand = abs(thisDemand)

			# delete old '+' or '-' labels
			self.leftFrame.systemsCanvas.delete('label')

			for nodeitem in visibleNodes:
				# update node sizes
				self.leftFrame.normalNodeSize(nodeitem)
				self.leftFrame.scaleNodeSize(nodeitem)

	def saveAttributes(self):
		titles = ['Name', 'Type', 'x', 'y', 'z', 'EdgeLength', 'Notes']
		values = [self.nameEntry.get(), self.v.get(), float(self.xEntry.get()), float(self.yEntry.get()), 
			float(self.zEntry.get()), float(self.edgeEntry.get()), self.notes.get('0.0', END)]
		updated = []

		# for each field, check if value is updated in NetworkX; if not, save and add to 'updated'
		for i in range(0, len(titles)):
			if (titles[i] not in self.G.node[self.index]) or (self.G.node[self.index][titles[i]] != values[i]):
				self.G.node[self.index][titles[i]] = values[i]

				# make sure we don't log a save when the value is empty string or endl
				if values[i] != '' and values[i] != '\n':
					updated.append(titles[i])

		if self.leftFrame.labels == 1:
			self.leftFrame.hideLabels()
			self.leftFrame.showLabels()

		# Demands
		for x in self.manager.systems: # for each system
			if self.systemDict[x].get() != None and self.systemDict[x].get() != '': # if there is a value for this node
				# if system doesn't exist in NetworkX already OR if the curr value in NetworkX isn't updated
				if (x not in self.G.node[self.index]) or (self.G.node[self.index][x] != int(self.systemDict[x].get())):
					updated.append(x)
					self.G.node[self.index][x] = int(self.systemDict[x].get())

		self.updateNodeSizes()

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Saved attributes of node " + str(self.index)
		log = log + " in the following fields: "
		for field in updated:
			log = log + str(field) + ", "
		log = log[:-2]

		self.leftFrame.appendLog(log)



	def initUI(self):
		# Name
		self.nameLabel = Label(self.parent, text="Name:", bg=self.color)
		self.nameLabel.grid(row=0, column=0, padx=5, pady=5, sticky=E)
		self.nameEntry = Entry(self.parent, highlightbackground=self.color)
		self.nameEntry.grid(row=0, column=1, columnspan=2, sticky=E+W, padx=5)

		# Notes
		self.notesLabel = Label(self.parent, text="Notes:", bg=self.color)
		self.notesLabel.grid(row=8, column=0, padx=5, sticky=E)
		self.notes = Text(self.parent, font='TkDefaultFont', width=1, height=8)
		self.notes.grid(row=8, column=1, columnspan=2, rowspan=8, padx=5, pady=10, sticky=E+W)
		
		# save button
		self.saveBtn = Button(self.parent, text="Save", command=self.saveAttributes, 
			highlightbackground=self.color)
		self.saveBtn.grid(row=16, column=2, padx=5, sticky=E)

		# Type, Demand, Geometry
		self.createTypeLabel()
		self.createGeometryLabel()
		self.createDemandLabel() # create demand last bc placement relies on type and geometry labels

		# if node attributes have been set previously, populate right pane using the existing data
		self.repopulateData()