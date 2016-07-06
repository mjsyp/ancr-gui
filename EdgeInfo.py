from Tkinter import *
import tkSimpleDialog
import networkx as nx
from datetime import datetime

class EdgeInfo(Frame):
	def __init__(self, parent, leftFrame, index, nodes, G, manager):
		Frame.__init__(self, parent)

		self.parent = parent
		self.leftFrame = leftFrame
		self.index = index
		self.nodes = nodes
		self.G = G
		self.manager = manager

		self.systemDict = {}
 		self.color = "dark gray"
		self.initUI()

	def createTypeLabel(self):

		self.typeLabel = Label(self.parent, text="Type:", bg=self.color, anchor=W)
		self.typeLabel.grid(row=2, column=0, padx=5, pady=5, sticky=E)

		# initialize default options in dropdown to the list in our Manager
		self.optionList = self.manager.types

		# Create frame to hold the OptionMenu
		self.typeMenu = Frame(self.parent, highlightbackground=self.color)
		self.typeMenu.grid(row=2, column=1, padx=10)

		# create a StringVar that holds the selected option in the dropdown
		self.v = StringVar()
		self.v.set(self.optionList[0])

		# actual dropdown
		self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
		self.dropdown.config(bg=self.color, highlightbackground=self.color)
		self.dropdown.grid(row=2, column=1)

		# 'Create New' button
		self.createTypeBtn = Button(self.parent, text="Create New", 
			command=self.createNewType, highlightbackground=self.color)
		self.createTypeBtn.grid(row=2, column=2)

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
			self.dropdown.configure(bg=self.color, highlightbackground=self.color)
			self.dropdown.grid(row=2, column=1)

	def createDemandLabel(self):
		# Demand
 		self.demandLabel = Label(self.parent, text="Demand:", bg=self.color, anchor=W)
 		self.demandLabel.grid(row=3, column=0, padx=5, pady=5, sticky=E)

		self.createDemandBtn = Button(self.parent, text="Create New", 
			command=self.createNewDemand, highlightbackground=self.color)
		self.createDemandBtn.grid(row=3, column=1)

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
		self.newDemandLabel.grid(row=3+self.numDemands, column=1)
		newEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		newEntry.grid(row=3+self.numDemands, column=2, padx=10)
		self.systemDict[label] = newEntry

		# move widgets down to make room for new demand label
		self.createDemandBtn.grid(row=4+self.numDemands, column=1)

		for item in self.parent.grid_slaves():
			if int(item.grid_info()["row"]) > (4 + self.numDemands):
				newRow = int(item.grid_info()["row"]) + self.numDemands + 1
				item.grid_configure(row=newRow)

		self.numDemands += 1

		if label not in self.leftFrame.optionList:
			self.leftFrame.optionList.insert(len(self.leftFrame.optionList)-2, label)
			self.leftFrame.dropdown.destroy()
			self.leftFrame.dropdown = OptionMenu(self.leftFrame.toolbar, self.leftFrame.v, 
				*self.leftFrame.optionList, command=self.leftFrame.newOptionMenu)
			self.leftFrame.dropdown.configure(bg="light blue")
			self.leftFrame.dropdown.pack(side='left')

	def createGeometryLabel(self):
		self.geometryLabel = Label(self.parent, text="Geometry:", bg=self.color, anchor=W)
		self.geometryLabel.grid(row=5, column=0, padx=5, pady=5, sticky=E)

		self.xLabel = Label(self.parent, text="x", bg=self.color)
		self.xLabel.grid(row=5, column=1, padx=1, pady=1)
		self.xEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		self.xEntry.grid(row=5, column=2)

		self.yLabel = Label(self.parent, text="y", bg=self.color)
		self.yLabel.grid(row=6, column=1, padx=1, pady=1)
		self.yEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		self.yEntry.grid(row=6, column=2)

		self.zLabel = Label(self.parent, text="z", bg=self.color)
		self.zLabel.grid(row=7, column=1, padx=1, pady=1)
		self.zEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		self.zEntry.grid(row=7, column=2)

	def repopulateData(self):
		if ('Name' in self.G.edge[self.nodes[0]][self.nodes[1]]) and (self.G.edge[self.nodes[0]][self.nodes[1]]['Name'] != None):
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.edge[self.nodes[0]][self.nodes[1]]['Name'])
		if ('Type' in self.G.edge[self.nodes[0]][self.nodes[1]]) and (self.G.edge[self.nodes[0]][self.nodes[1]]['Type'] != None):
			self.v.set(self.G.edge[self.nodes[0]][self.nodes[1]]['Type'])
		if 'x' in self.G.edge[self.nodes[0]][self.nodes[1]]:
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, self.G.edge[self.nodes[0]][self.nodes[1]]['x'])
		if 'y' in self.G.edge[self.nodes[0]][self.nodes[1]]:
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, self.G.edge[self.nodes[0]][self.nodes[1]]['y'])
		if 'z' in self.G.edge[self.nodes[0]][self.nodes[1]]:
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, self.G.edge[self.nodes[0]][self.nodes[1]]['z'])
		if 'Notes' in self.G.edge[self.nodes[0]][self.nodes[1]]:
			self.notes.delete('0.0', END)
			self.notes.insert('0.0', self.G.edge[self.nodes[0]][self.nodes[1]]['Notes'])
        
		for x in self.manager.systems:
			if x in self.G.edge[self.nodes[0]][self.nodes[1]]:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.edge[self.nodes[0]][self.nodes[1]][x])

	def saveAttributes(self):
		titles = ['Name', 'Type', 'x', 'y', 'z', 'Notes']
		values = [self.nameEntry.get(), self.v.get(), int(self.xEntry.get()), 
			int(self.yEntry.get()), int(self.zEntry.get()), self.notes.get('0.0', END)]
		updated = []

		# for each field, check if value is updated in NetworkX; if not, save and add to 'updated'
		for i in range(0, len(titles)):
			if (titles[i] not in self.G.edge[self.nodes[0]][self.nodes[1]]) or (self.G.edge[self.nodes[0]][self.nodes[1]][titles[i]] != values[i]):
				self.G.edge[self.nodes[0]][self.nodes[1]][titles[i]] = values[i]

				# make sure we don't log a save when the value is empty string or endl
				if values[i] != '' and values[i] != '\n':
					updated.append(titles[i])

		# Demands
		for x in self.manager.systems: # for each system
			if self.systemDict[x].get() != None and self.systemDict[x].get() != '': # if there is a value for this demand
				# if system doesn't exist in NetworkX already OR if the curr value in NetworkX isn't updated
				if (x not in self.G.edge[self.nodes[0]][self.nodes[1]]) or (self.G.edge[self.nodes[0]][self.nodes[1]][x] != int(self.systemDict[x].get())):
					updated.append(x)
					self.G.edge[self.nodes[0]][self.nodes[1]][x] = int(self.systemDict[x].get())

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Saved attributes of edge between node " 
 		log = log + str(self.nodes[0]) + " and node " + str(self.nodes[1]) + " (ID = " + str(self.index) + ")"
		log = log + " in the following fields: "
		for field in updated:
			log = log + str(field) + ", "
		log = log[:-2]
		self.leftFrame.appendLog(log)

	def initUI(self):
		# Name
		self.nameLabel = Label(self.parent, text="Name:", bg=self.color)
		self.nameLabel.grid(row=1, column=0, padx=5, pady=10, sticky=E)

		self.nameEntry = Entry(self.parent, highlightbackground=self.color)
		self.nameEntry.grid(row=1, column=1, columnspan=2, sticky=E+W, padx=10)

		# Notes
		self.notesLabel = Label(self.parent, text="Notes:", bg=self.color)
		self.notesLabel.grid(row=8, column=0, padx=5, pady=5, sticky=E)
		self.notes = Text(self.parent, height=8, width=25, font='TkDefaultFont')
		self.notes.grid(row=8, column=1, columnspan=2, rowspan=8, pady=5, padx=10)

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

