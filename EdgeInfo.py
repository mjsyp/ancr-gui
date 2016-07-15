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
		self.typeLabel = Label(self.propGroup, text="Type:", bg=self.color)
		self.typeLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E)

		# initialize default options in dropdown to the list in our Manager
		self.optionList = self.manager.types

		# create a StringVar that holds the selected option in the dropdown
		self.v = StringVar()
		self.v.set(self.optionList[0])

		# actual dropdown
		self.dropdown = OptionMenu(self.propGroup, self.v, *self.optionList, command=self.createNewType)
		self.dropdown.config(highlightbackground=self.color)
		self.dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)

	def createNewType(self, event):
		if self.v.get() == "Create New":
			typeLabel = tkSimpleDialog.askstring(title="New Type", prompt="Enter a new type")

			if typeLabel != None:
				# add to manager and to list in dropdown
				self.manager.addType(typeLabel)

				# select new 'type' in dropdown
				self.v.set(self.optionList[len(self.optionList)-2])

				# redraw dropdown
				self.dropdown.grid_forget()
				self.dropdown = OptionMenu(self.propGroup, self.v, *self.optionList, command=self.createNewType)
				self.dropdown.config(highlightbackground=self.color)
				self.dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)

	def createDemandLabel(self):
		# Demand
 		self.demandLabel = Label(self.propGroup, text="Demands:", bg=self.color, anchor=W)
 		self.demandLabel.grid(row=2, column=0, padx=5, sticky=E)

		self.createDemandBtn = Button(self.propGroup, text="New Demand", 
			command=self.createNewDemand, highlightbackground=self.color)
		self.createDemandBtn.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)

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
		self.newDemandLabel = Label(self.propGroup, text=label, bg=self.color)
		self.newDemandLabel.grid(row=2+self.numDemands, column=1)
		newEntry = Entry(self.propGroup, highlightbackground=self.color, width=9)
		newEntry.grid(row=2+self.numDemands, column=2, padx=10)
		self.systemDict[label] = newEntry

		# move 'Create New' button down
		self.createDemandBtn.grid(row=3+self.numDemands, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)
		self.numDemands += 1

		# add new demand to the main toolbar dropdown
		if label not in self.leftFrame.optionList:
			self.leftFrame.optionList.insert(len(self.leftFrame.optionList)-2, label)
			self.leftFrame.dropdown.destroy()
			self.leftFrame.dropdown = OptionMenu(self.leftFrame.toolbar, self.leftFrame.v, 
				*self.leftFrame.optionList, command=self.leftFrame.newOptionMenu)
			self.leftFrame.dropdown.configure(highlightbackground="light blue")
			self.leftFrame.dropdown.pack(side='left')

	def creategeoGroup(self):
		self.geoGroup = LabelFrame(self.parent, text="Geometry", bg=self.color)
		#self.geoGroup.grid(row=4, rowspan=3, columnspan=3, padx=10, sticky=E+W)
		self.geoGroup.grid(row=1, padx=10, sticky=E+W)

		self.createSimpleGeoLabel()

	def createSimpleGeoLabel(self):
		self.geoGroup.columnconfigure(1, weight=1)
		self.geoGroup.columnconfigure(2, weight=1)

		# x, y, z coordinate entries
		self.xLabel = Label(self.geoGroup, text="x", bg=self.color)
		self.xLabel.grid(row=1, column=1, padx=5, sticky=E+W)
		self.xEntry = Entry(self.geoGroup, highlightbackground=self.color, width=8)
		self.xEntry.grid(row=1, column=2, padx=5, sticky=E+W)

		self.yLabel = Label(self.geoGroup, text="y", bg=self.color)
		self.yLabel.grid(row=2, column=1, padx=5, sticky=E+W)
		self.yEntry = Entry(self.geoGroup, highlightbackground=self.color, width=8)
		self.yEntry.grid(row=2, column=2, padx=5, sticky=E+W)

		self.zLabel = Label(self.geoGroup, text="z", bg=self.color)
		self.zLabel.grid(row=3, column=1, padx=5, sticky=E+W)
		self.zEntry = Entry(self.geoGroup, highlightbackground=self.color, width=8)
		self.zEntry.grid(row=3, column=2, padx=5, pady=(1,5), sticky=E+W)

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
		self.propGroup = LabelFrame(self.parent, text="Properties", bg=self.color)
		self.propGroup.grid(row=0, padx=10, sticky=E+W)

		# Name
		self.nameLabel = Label(self.propGroup, text="Name:", bg=self.color)
		self.nameLabel.grid(row=0, column=0, padx=5, pady=(5, 1), sticky=E)
		self.nameEntry = Entry(self.propGroup, highlightbackground=self.color)
		self.nameEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=(5, 1), sticky=E+W)

		# Type, Demand
		self.createTypeLabel()
		self.createDemandLabel()

		# Geometry
		self.creategeoGroup()

		# Notes
		self.notesGroup = LabelFrame(self.parent, text="Notes", bg=self.color)
		self.notesGroup.grid(row=2, padx=10, sticky=E+W)
		self.notes = Text(self.notesGroup, font='TkDefaultFont', width=1, height=12)
		self.notesGroup.columnconfigure(0, weight=1)
		self.notes.grid(row=0, column=0, padx=5, pady=(1, 5), sticky=E+W)
		
		# save button
		self.saveBtn = Button(self.parent, text="Save", command=self.saveAttributes, 
			highlightbackground=self.color)
		self.saveBtn.grid(row=3, padx=10, pady=5, sticky=E)

		# if node attributes have been set previously, populate right pane using the existing data
		self.repopulateData()