from Tkinter import *
import tkSimpleDialog
import networkx as nx

class Component(Frame):
	def __init__(self, parent, leftFrame, index, G, manager, nodes=None):
		Frame.__init__(self, parent)

		self.parent = parent
		self.leftFrame = leftFrame
		self.index = index
		self.G = G
		self.manager = manager
		self.nodes = nodes

		self.systemDict = {}
 		self.color = "dark gray" 
		self.initUI()

	def createDemandLabel(self):
		self.demandGroup.columnconfigure(0, weight=1)
		self.demandGroup.columnconfigure(1, weight=1)

		self.createDemandBtn = Button(self.demandGroup, text="New Demand", command=self.createNewDemand, bg=self.color, highlightbackground=self.color)
		self.createDemandBtn.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=E+W)
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
		self.newDemandLabel = Label(self.demandGroup, text=label, bg=self.color)
		self.newDemandLabel.grid(row=0+self.numDemands, column=0, sticky=E+W)
		newEntry = Entry(self.demandGroup, highlightbackground=self.color, width=9)
		newEntry.grid(row=0+self.numDemands, column=1, padx=5, sticky=E+W)
		self.systemDict[label] = newEntry

		# move 'Create New' button down
		self.createDemandBtn.grid(row=1+self.numDemands, column=0, columnspan=2, padx=5, pady=5, sticky=E+W)
		self.numDemands += 1

		# add new demand to the main toolbar dropdown
		if label not in self.leftFrame.optionList:
			self.leftFrame.optionList.insert(len(self.leftFrame.optionList)-2, label)
			self.leftFrame.dropdown.destroy()
			self.leftFrame.dropdown = OptionMenu(self.leftFrame.toolbar, self.leftFrame.v, 
				*self.leftFrame.optionList, command=self.leftFrame.newOptionMenu)
			self.leftFrame.dropdown.configure(highlightbackground="light blue", bg='light blue')
			self.leftFrame.dropdown.pack(side='left')

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

	def saveNodeAttributes(self):
		# save demands
		for x in self.manager.systems: # for each system
			# if there is a value for this node
			if self.systemDict[x].get() != None and self.systemDict[x].get() != '':
				# if system doesn't exist in NetworkX already OR if the curr value in NetworkX isn't updated
				if (x not in self.G.node[self.index]) or (self.G.node[self.index][x] != int(self.systemDict[x].get())):
					self.G.node[self.index][x] = int(self.systemDict[x].get())
			
			elif x in self.G.node[self.index] and self.systemDict[x].get() == '':
				if self.leftFrame.v.get() != 'All':
					nodeCoords = self.leftFrame.systemsCanvas.coords(self.index)
					overlapped = self.leftFrame.systemsCanvas.find_overlapping(nodeCoords[0], nodeCoords[1], nodeCoords[2], nodeCoords[3])
					for edge in overlapped:
						if self.leftFrame.checkTag(edge) == 'edge':
							self.leftFrame.systemsCanvas.itemconfig(edge, state='hidden')
					self.leftFrame.systemsCanvas.itemconfig(self.index, state='hidden')
				del self.G.node[self.index][x]

		self.updateNodeSizes()

	def saveEdgeAttributes(self):
		# save demands
		for x in self.manager.systems: # for each system
			if self.systemDict[x].get() != None and self.systemDict[x].get() != '': # if there is a value for this demand
				# if system doesn't exist in NetworkX already OR if the curr value in NetworkX isn't updated
				if (x not in self.G.edge[self.nodes[0]][self.nodes[1]]) or (self.G.edge[self.nodes[0]][self.nodes[1]][x] != int(self.systemDict[x].get())):
					self.G.edge[self.nodes[0]][self.nodes[1]][x] = int(self.systemDict[x].get())

			elif x in self.G.edge[self.nodes[0]][self.nodes[1]] and self.systemDict[x].get() == '':
				if self.leftFrame.v.get() != 'All':
					self.leftFrame.systemsCanvas.itemconfig(self.index, state='hidden')
				del self.G.edge[self.nodes[0]][self.nodes[1]][x]

	def repopulateNodeData(self):
		for x in self.manager.systems:
			if x in self.G.node[self.index]:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.node[self.index][x])

	def repopulateEdgeData(self):
		for x in self.manager.systems:
			if x in self.G.edge[self.nodes[0]][self.nodes[1]]:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.edge[self.nodes[0]][self.nodes[1]][x])

	def initUI(self):
		self.demandGroup = LabelFrame(self.parent, text="Demands", bg=self.color)
		self.demandGroup.grid(row=1, padx=10, sticky=E+W)
		self.createDemandLabel()

		if self.nodes == None:
			self.repopulateNodeData()
		else:
			self.repopulateEdgeData()
