'''
 * Component.py
 * 
 * Assumes the selected node is of type component;
 * adds a box where demands of this component can be
 * specified
 * 
 * Major functionalities include:
 *     demand box / create new demand
 *     update sizes of nodes if current system is not 'All'
 *     save/repopulate
 *
'''
from Tkinter import *
import tkSimpleDialog
import networkx as nx

class Component(Frame):
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

	def createDemandLabel(self):
		self.demandGroup.columnconfigure(0, weight=1)
		self.demandGroup.columnconfigure(1, weight=1)

		# 'create new demand' button
		self.createDemandBtn = Button(self.demandGroup, text="New Demand", command=self.createNewDemand, bg=self.color, highlightbackground=self.color)
		self.createDemandBtn.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=E+W)
		self.numDemands = 0

		# create a new demand entry for every system in our manager list (in Manager.py)
		for systemLabel in self.manager.systems:
			self.createNewDemand(systemLabel)

	def createNewDemand(self, label=None):
		# If no label was provided as a parameter, prompt for a label
		if label == None:
			label = tkSimpleDialog.askstring(title="Label", prompt="Enter a Label Name") # Prompt for label
			# if user hit 'Cancel' in dialog window, label=None; return from this function
			if label == None:
				return
			# else user didn't hit 'Cancel', so add the user input as a new system in our manager
			self.manager.addSystem(label)
		
		# Create new Label and corresponding entry box
		self.newDemandLabel = Label(self.demandGroup, text=label, bg=self.color)
		self.newDemandLabel.grid(row=0+self.numDemands, column=0, sticky=E+W)
		newEntry = Entry(self.demandGroup, highlightbackground=self.color, width=9)
		newEntry.grid(row=0+self.numDemands, column=1, padx=5, sticky=E+W)
		self.systemDict[label] = newEntry # save the entry widget in the dictionary systemDict

		# move 'Create New' button down
		self.createDemandBtn.grid(row=1+self.numDemands, column=0, columnspan=2, padx=5, pady=5, sticky=E+W)
		self.numDemands += 1

		# add the new demand/system to the main toolbar dropdown
		if label not in self.leftFrame.optionList:
			self.leftFrame.optionList.insert(len(self.leftFrame.optionList)-2, label)
			self.leftFrame.dropdown.destroy()
			self.leftFrame.dropdown = OptionMenu(self.leftFrame.toolbar, self.leftFrame.v, 
				*self.leftFrame.optionList, command=self.leftFrame.newOptionMenu)
			self.leftFrame.dropdown.configure(highlightbackground="light blue", bg='light blue')
			self.leftFrame.dropdown.pack(side='left')

	def createGeometry(self):
		self.geoGroup = LabelFrame(self.parent, text="Geometry", bg=self.color)
		self.geoGroup.grid(row=2, padx=10, sticky=E+W)

		# x coord
		self.xLabel = Label(self.geoGroup, text="x", bg=self.color)
		self.xLabel.grid(row=self.numCoords, column=1, padx=(5, 0), pady=(0, 5))
		self.xEntry = Entry(self.geoGroup, highlightbackground=self.color, width=5)
		self.xEntry.grid(row=self.numCoords, column=2, pady=(0, 5))
		self.xEntry.insert(0, 0) # initialize to 0
		# y coord
		self.yLabel = Label(self.geoGroup, text="y", bg=self.color)
		self.yLabel.grid(row=self.numCoords, column=3, padx=(5, 0), pady=(0, 5))
		self.yEntry = Entry(self.geoGroup, highlightbackground=self.color, width=5)
		self.yEntry.grid(row=self.numCoords, column=4, pady=(0, 5))
		self.yEntry.insert(0, 0)
		# z coord
		self.zLabel = Label(self.geoGroup, text="z", bg=self.color)
		self.zLabel.grid(row=self.numCoords, column=5, padx=(5, 0), pady=(0, 5))
		self.zEntry = Entry(self.geoGroup, highlightbackground=self.color, width=5)
		self.zEntry.grid(row=self.numCoords, column=6, pady=(0, 5))
		self.zEntry.insert(0, 0)

	def createNewGeo(self):
		# numbers each row of geometry
		idText = str(self.numCoords) + "."
		self.idLabel = Label(self.geoGroup, text=idText, bg=self.color)
		self.idLabel.config(activeforeground='red')
		self.idLabel.grid(row=self.numCoords, column=0, padx=(5, 0), pady=(0, 5))
		# adds fuctionality to be able to delete a row if you click on the number label
		# and turns number label red on scrollover
		self.idLabel.bind('<Button-1>', self.deleteGeo)
		self.idLabel.bind('<Enter>', lambda e: e.widget.config(fg='red'))
		self.idLabel.bind('<Leave>', lambda e: e.widget.config(fg='black'))

		# x, y, z coordinate entries
		self.xLabel = Label(self.geoGroup, text="x", bg=self.color)
		self.xLabel.grid(row=self.numCoords, column=1, padx=(5, 0), pady=(0, 5))
		self.xEntry = Entry(self.geoGroup, highlightbackground=self.color, width=5)
		self.xEntry.grid(row=self.numCoords, column=2, pady=(0, 5))
		self.xEntry.insert(0, 0)
		self.xEntryList.append(self.xEntry)

		self.yLabel = Label(self.geoGroup, text="y", bg=self.color)
		self.yLabel.grid(row=self.numCoords, column=3, padx=(5, 0), pady=(0, 5))
		self.yEntry = Entry(self.geoGroup, highlightbackground=self.color, width=5)
		self.yEntry.grid(row=self.numCoords, column=4, pady=(0, 5))
		self.yEntry.insert(0, 0)
		self.yEntryList.append(self.yEntry)

		self.zLabel = Label(self.geoGroup, text="z", bg=self.color)
		self.zLabel.grid(row=self.numCoords, column=5, padx=(5, 0), pady=(0, 5))
		self.zEntry = Entry(self.geoGroup, highlightbackground=self.color, width=5)
		self.zEntry.grid(row=self.numCoords, column=6, pady=(0, 5))
		self.zEntry.insert(0, 0)
		self.zEntryList.append(self.zEntry)

		# Edge Length Parameter
		self.edgeLabel = Label(self.geoGroup, text="Edge Length", bg=self.color)
		self.edgeLabel.grid(row=self.numCoords, column=7, padx=(5, 0), pady=(0, 5))
		self.edgeEntry = Entry(self.geoGroup, highlightbackground=self.color, width=5)
		self.edgeEntry.grid(row=self.numCoords, column=8, padx=(0, 5), pady=(0, 5))
		self.edgeEntry.insert(0, 0)
		self.edgeEntryList.append(self.edgeEntry)

		self.numCoords += 1

	def updateNodeSizes(self):
		if self.leftFrame.v.get() != 'All' and self.leftFrame.v.get() != 'Create New':
			self.leftFrame.minDemand = 1000000000
			self.leftFrame.maxDemand = -1
			visibleNodes = []

			# for each node on the canvas
			for nodeitem in self.leftFrame.systemsCanvas.find_withtag('node'):
				# if it has a demand value for current system we're in
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

			# update node sizes
			for nodeitem in visibleNodes:
				self.leftFrame.normalNodeSize(nodeitem)
				self.leftFrame.scaleNodeSize(nodeitem)

	def saveNodeAttributes(self):
		# save demands values of this node
		for x in self.manager.systems: 
			# if there is a value for this node
			if self.systemDict[x].get() != None and self.systemDict[x].get() != '':
				# if system doesn't exist in NetworkX already OR if the curr value in NetworkX isn't updated, save the curr value
				if (x not in self.G.node[self.index]) or (self.G.node[self.index][x] != int(self.systemDict[x].get())):
					self.G.node[self.index][x] = int(self.systemDict[x].get())

			# else if a previous value was cleared
			elif x in self.G.node[self.index] and self.systemDict[x].get() == '':
				# if we're not in 'All', hide this node and the edges connected to it bc there isn't a demand value anymore
				if self.leftFrame.v.get() != 'All':
					nodeCoords = self.leftFrame.systemsCanvas.coords(self.index)
					overlapped = self.leftFrame.systemsCanvas.find_overlapping(nodeCoords[0], nodeCoords[1], nodeCoords[2], nodeCoords[3])
					for edge in overlapped:
						if self.leftFrame.checkTag(edge) == 'edge':
							self.leftFrame.systemsCanvas.itemconfig(edge, state='hidden')
					self.leftFrame.systemsCanvas.itemconfig(self.index, state='hidden')
				del self.G.node[self.index][x]

		# save geometry values of this node
		titles = ['x', 'y', 'z']
		values = [self.xEntry.get(), self.yEntry.get(), self.zEntry.get()]

		# for each field, check if coord is updated in NetworkX; if not, save and add to 'updated'
		for i in range(0, len(titles)):
			if (titles[i] not in self.G.node[self.index]) or (self.G.node[self.index][titles[i]] != values[i]):
				self.G.node[self.index][titles[i]] = values[i]

		self.updateNodeSizes()

	def repopulateNodeData(self):
		# repopulate demand values
		for x in self.manager.systems:
			if x in self.G.node[self.index]:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.node[self.index][x])

		# repopulate x, y, z values
		if 'x' in self.G.node[self.index]:
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, self.G.node[self.index]['x'])
		if 'y' in self.G.node[self.index]:
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, self.G.node[self.index]['y'])
		if 'z' in self.G.node[self.index]:
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, self.G.node[self.index]['z'])

	def initUI(self):
		self.demandGroup = LabelFrame(self.parent, text="Demands", bg=self.color)
		self.demandGroup.grid(row=1, padx=10, sticky=E+W)
		self.createDemandLabel()
		self.createGeometry()

		self.repopulateNodeData()
