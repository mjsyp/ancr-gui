from Tkinter import *
import tkSimpleDialog
import networkx as nx
from datetime import datetime

class NodeEdgeInfo(Frame):
	def __init__(self, parent, leftFrame, index, G, manager, nodes=None):
		Frame.__init__(self, parent)

		self.parent = parent
		self.leftFrame = leftFrame
		self.index = index
		self.G = G
		self.manager = manager
		self.nodes=nodes

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
		self.dropdown.config(highlightbackground=self.color, bg=self.color)
		self.dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)

	def createNewType(self, event):
		if self.v.get() == "Create New":
			typeLabel = tkSimpleDialog.askstring(title="New Type", prompt="Enter a new type")

			if typeLabel != None:
				# select new 'type' in dropdown
				self.optionList.insert(len(self.optionList)-1, typeLabel)
				self.v.set(self.optionList[len(self.optionList)-2])

				# redraw dropdown
				self.dropdown.destroy()
				self.dropdown = OptionMenu(self.propGroup, self.v, *self.optionList, command=self.createNewType)
				self.dropdown.config(highlightbackground=self.color, bg=self.color)
				self.dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)

	def createDemandLabel(self):
		# Demand
 		self.demandLabel = Label(self.propGroup, text="Demands:", bg=self.color, anchor=W)
 		self.demandLabel.grid(row=2, column=0, padx=5, sticky=E)

		self.createDemandBtn = Button(self.propGroup, text="New Demand", command=self.createNewDemand, bg=self.color, highlightbackground=self.color)
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
		self.geoGroup.grid(row=1, padx=10, sticky=E+W)

		# 'Simple' vs 'Advanced' dropdown menu
		self.geoOptionList = ["Simple", "Advanced"]
		self.geoOption = StringVar()
		self.geoOption.set(self.geoOptionList[0])
		self.geoDropdown = OptionMenu(self.geoGroup, self.geoOption, *self.geoOptionList, command=self.geoSwitch)
		self.geoDropdown.config(highlightbackground=self.color, bg=self.color)
		self.geoDropdown.grid(row=0, column=0, columnspan=2, pady=5, sticky=E+W)

		self.createSimpleGeoLabel()

	def geoSwitch(self, event=None):
		# destroy current widgets in this group
		for widget in self.geoGroup.winfo_children():
			if widget != self.geoDropdown:
				widget.grid_forget()

		if self.geoOption.get() == "Simple":
			self.createSimpleGeoLabel()
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, 0)
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, 0)
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, 0)
			self.edgeEntry.delete(0, END)
			self.edgeEntry.insert(0, 0)
		else:
			self.createAdvGeoLabel()
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, 0)
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, 0)
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, 0)
			self.edgeEntry.delete(0, END)
			self.edgeEntry.insert(0, 0)

	def createSimpleGeoLabel(self):
		self.geoGroup.columnconfigure(0, weight=1)
 		self.geoGroup.columnconfigure(1, weight=1)

		# x, y, z coordinate entries
		self.xLabel = Label(self.geoGroup, text="x", bg=self.color)
		self.xLabel.grid(row=1, column=0, padx=5, sticky=E+W)
		self.xEntry = Entry(self.geoGroup, highlightbackground=self.color, width=8)
		self.xEntry.grid(row=1, column=1, padx=5, sticky=E+W)		
		
		self.yLabel = Label(self.geoGroup, text="y", bg=self.color)
		self.yLabel.grid(row=2, column=0, padx=5, sticky=E+W)
		self.yEntry = Entry(self.geoGroup, highlightbackground=self.color, width=8)
		self.yEntry.grid(row=2, column=1, padx=5, sticky=E+W)		
		
		self.zLabel = Label(self.geoGroup, text="z", bg=self.color)
		self.zLabel.grid(row=3, column=0, padx=5, sticky=E+W)
		self.zEntry = Entry(self.geoGroup, highlightbackground=self.color, width=8)
		self.zEntry.grid(row=3, column=1, padx=5, sticky=E+W)		
		
		# Edge Length Parameter
		self.edgeLabel = Label(self.geoGroup, text="Edge Length", bg=self.color)
		self.edgeLabel.grid(row=4, column=0, padx=5, sticky=E+W)
		self.edgeEntry = Entry(self.geoGroup, highlightbackground=self.color, width=8)
		self.edgeEntry.grid(row=4, column=1, padx=5, pady=(1, 5), sticky=E+W)
		

	def createAdvGeoLabel(self):
		self.numCoords = 1
		self.geoDropdown.grid(row=0, column=0, columnspan=7, padx=5, pady=5, sticky=E+W)

		# initilize entry widget lists
		self.xEntryList = []
		self.yEntryList = []
		self.zEntryList = []
		self.edgeEntryList = []
		
		self.createNewGeo()
 
		# create new coord button
		self.newCoordBtn = Button(self.geoGroup, text="Add Row", command=self.createNewGeo, bg=self.color, highlightbackground=self.color)
		self.newCoordBtn.grid(row=0, column=7, columnspan=2, padx=5, pady=5, sticky=E+W)

	def createNewGeo(self):
		idText = str(self.numCoords) + "."
		self.idLabel = Label(self.geoGroup, text=idText, bg=self.color)
		self.idLabel.config(activeforeground='red')
		self.idLabel.grid(row=self.numCoords, column=0, padx=(5, 0), pady=(0, 5))
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

	def deleteGeo(self, event):
		deleteRow = int(event.widget.grid_info()['row'])
		self.G.node[self.index]['x'].pop(deleteRow-1)
		self.G.node[self.index]['y'].pop(deleteRow-1)
		self.G.node[self.index]['z'].pop(deleteRow-1)
		self.G.node[self.index]['EdgeLength'].pop(deleteRow-1)
		self.xEntryList.pop(deleteRow-1)
		self.yEntryList.pop(deleteRow-1)
		self.zEntryList.pop(deleteRow-1)
		self.edgeEntryList.pop(deleteRow-1)

		for widget in self.geoGroup.grid_slaves():
			thisRow = int(widget.grid_info()['row'])

			if thisRow == deleteRow:
				widget.grid_forget()
			elif thisRow > deleteRow:
				widget.grid_configure(row=thisRow-1)
				if int(widget.grid_info()['column']) == 0:
					widget.config(text=str(thisRow-1)+".")

		self.numCoords -= 1

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
		titles = ['Name', 'Type', 'Notes']
		values = [self.nameEntry.get(), self.v.get(), self.notes.get('0.0', END)]
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

		# if node has simple geometry 
		if self.geoOption.get() == 'Simple':
			geolist = ['x', 'y', 'z', 'EdgeLength']
			geovalues = [float(self.xEntry.get()), float(self.yEntry.get()), float(self.zEntry.get()), float(self.edgeEntry.get())]

			# for each field, check if value is updated in NetworkX; if not, save and add to 'updated'
			for i in range(0, len(geolist)):
				if (geolist[i] not in self.G.node[self.index]) or (self.G.node[self.index][geolist[i]] != geovalues[i]):
					self.G.node[self.index][geolist[i]] = geovalues[i]

					# make sure we don't log a save when the value is empty string or endl
					if geovalues[i] != '' and geovalues[i] != '\n':
						updated.append(geolist[i])
		
		else:
			geolist = ['x', 'y', 'z', 'EdgeLength']
			xVals = []
			yVals = []
			zVals = []
			edgeVals = []
			
			for i in range(0, len(self.xEntryList)):
				xVals.append(float(self.xEntryList[i].get()))
				yVals.append(float(self.yEntryList[i].get()))
				zVals.append(float(self.zEntryList[i].get()))
				edgeVals.append(float(self.edgeEntryList[i].get()))
			
			self.G.node[self.index]['x'] = xVals
			self.G.node[self.index]['y'] = yVals
			self.G.node[self.index]['z'] = zVals
			self.G.node[self.index]['EdgeLength'] = edgeVals

		# Demands
		for x in self.manager.systems: # for each system
			if self.systemDict[x].get() == '':
				del self.G.node[self.index][x]
			elif self.systemDict[x].get() != None: # if there is a value for this node
				# if system doesn't exist in NetworkX already OR if the curr value in NetworkX isn't updated
				if (x not in self.G.node[self.index]) or (self.G.node[self.index][x] != int(self.systemDict[x].get())):
					updated.append(x)
					self.G.node[self.index][x] = int(self.systemDict[x].get())

		self.updateNodeSizes()
		self.leftFrame.dockedWindows.showSubNetwork(self.index)

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Saved attributes of node " + str(self.index)
		log = log + " in the following fields: "
		for field in updated:
			log = log + str(field) + ", "
		log = log[:-2]

		self.leftFrame.appendLog(log)

	def saveEdgeAttributes(self):
		titles = ['Name', 'Type', 'Notes']
		values = [self.nameEntry.get(), self.v.get(), self.notes.get('0.0', END)]
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

	def repopulateNodeData(self):
		if 'Name' in self.G.node[self.index] and self.G.node[self.index]['Name'] != None:
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.node[self.index]['Name'])
		if 'Type' in self.G.node[self.index] and self.G.node[self.index]['Type'] != None:
			self.v.set(self.G.node[self.index]['Type'])
		if 'Notes' in self.G.node[self.index]:
			self.notes.delete('0.0', END)
			self.notes.insert('0.0', self.G.node[self.index]['Notes'])
		
		try: 
			int(self.G.node[self.index]['x'])
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
		except TypeError: 
			self.geoOption.set('Advanced')
			self.geoSwitch()

			self.xEntry.delete(0, END)
			self.xEntry.insert(0, self.G.node[self.index]['x'][0])
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, self.G.node[self.index]['y'][0])
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, self.G.node[self.index]['z'][0])
			self.edgeEntry.delete(0, END)
			self.edgeEntry.insert(0, self.G.node[self.index]['EdgeLength'][0])

			for i in range(0, len(self.G.node[self.index]['x'])-1):
				self.createNewGeo()
				self.xEntry.delete(0, END)
				self.xEntry.insert(0, self.G.node[self.index]['x'][i+1])
				self.yEntry.delete(0, END)
				self.yEntry.insert(0, self.G.node[self.index]['y'][i+1])
				self.zEntry.delete(0, END)
				self.zEntry.insert(0, self.G.node[self.index]['z'][i+1])
				self.edgeEntry.delete(0, END)
				self.edgeEntry.insert(0, self.G.node[self.index]['EdgeLength'][i+1])

		for x in self.manager.systems:
			if x in self.G.node[self.index]:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.node[self.index][x])


	def repopulateEdgeData(self):
		if ('Name' in self.G.edge[self.nodes[0]][self.nodes[1]]) and (self.G.edge[self.nodes[0]][self.nodes[1]]['Name'] != None):
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.edge[self.nodes[0]][self.nodes[1]]['Name'])
		if ('Type' in self.G.edge[self.nodes[0]][self.nodes[1]]) and (self.G.edge[self.nodes[0]][self.nodes[1]]['Type'] != None):
			self.v.set(self.G.edge[self.nodes[0]][self.nodes[1]]['Type'])
		if 'Notes' in self.G.edge[self.nodes[0]][self.nodes[1]]:
			self.notes.delete('0.0', END)
			self.notes.insert('0.0', self.G.edge[self.nodes[0]][self.nodes[1]]['Notes'])
        
		for x in self.manager.systems:
			if x in self.G.edge[self.nodes[0]][self.nodes[1]]:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.edge[self.nodes[0]][self.nodes[1]][x])

	def initUI(self):
		self.propGroup = LabelFrame(self.parent, text="Properties", bg=self.color)
		self.propGroup.grid(row=0, padx=10, sticky=E+W)

		self.propGroup.columnconfigure(0, weight=1)
 		self.propGroup.columnconfigure(1, weight=1)

		# Name
		self.nameLabel = Label(self.propGroup, text="Name:", bg=self.color)
		self.nameLabel.grid(row=0, column=0, padx=5, pady=(5, 1), sticky=E)
		self.nameEntry = Entry(self.propGroup, highlightbackground=self.color)
		self.nameEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=(5, 1), sticky=E+W)

		# Type, Demand
		self.createTypeLabel()
		self.createDemandLabel()

		# Notes
		self.notesGroup = LabelFrame(self.parent, text="Notes", bg=self.color)
		self.notesGroup.grid(row=2, padx=10, sticky=E+W)
		self.notes = Text(self.notesGroup, font='TkDefaultFont', width=1, height=12)
		self.notesGroup.columnconfigure(0, weight=1)
		self.notes.grid(row=0, column=0, padx=5, pady=(1, 5), sticky=E+W)

		# if node attributes have been set previously, populate right pane using the existing data
		if self.nodes == None:
			self.creategeoGroup()
			self.repopulateNodeData()
			self.saveBtn = Button(self.parent, text="Save", command=self.saveNodeAttributes, highlightbackground=self.color)
			self.saveBtn.grid(row=3, padx=10, pady=5, sticky=E)

		else:
			self.repopulateEdgeData()
			self.saveBtn = Button(self.parent, text="Save", command=self.saveEdgeAttributes, highlightbackground=self.color)
			self.saveBtn.grid(row=3, padx=10, pady=5, sticky=E)
