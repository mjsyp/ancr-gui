from Tkinter import *
import tkSimpleDialog
import networkx as nx
#from datetime import datetime

class Compartment(Frame):
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

	def createGeoGroup(self):
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

		# if switching between simple and advanced geometry, erase old information and replace entries with zeroes
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

	def saveNodeAttributes(self):
		if self.leftFrame.labels == 1:
			self.leftFrame.hideLabels()
			self.leftFrame.showLabels()

		# if node has simple geometry 
		if self.geoOption.get() == 'Simple':
			geolist = ['x', 'y', 'z', 'EdgeLength']
			# get the geometric values from their respective entries
			geovalues = [float(self.xEntry.get()), float(self.yEntry.get()), float(self.zEntry.get()), float(self.edgeEntry.get())]

			# for each field, check if value is updated in NetworkX; if not, save and add to 'updated'
			for i in range(0, len(geolist)):
				if (geolist[i] not in self.G.node[self.index]) or (self.G.node[self.index][geolist[i]] != geovalues[i]):
					self.G.node[self.index][geolist[i]] = geovalues[i]

		# else node has advanced geometry
		else:
			# initilize lists of geometric values
			xVals = []
			yVals = []
			zVals = []
			edgeVals = []
			
			# loop through x, y, z, edge entry lists and get the values from each of those and store in x, y, z,edge vals lists
			for i in range(0, len(self.xEntryList)):
				xVals.append(float(self.xEntryList[i].get()))
				yVals.append(float(self.yEntryList[i].get()))
				zVals.append(float(self.zEntryList[i].get()))
				edgeVals.append(float(self.edgeEntryList[i].get()))
			
			# store each geo vals list to network x
			self.G.node[self.index]['x'] = xVals
			self.G.node[self.index]['y'] = yVals
			self.G.node[self.index]['z'] = zVals
			self.G.node[self.index]['EdgeLength'] = edgeVals

	# inserts networkX data for the node into repsective entry box
	def repopulateNodeData(self):
		try: #simple geometry
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
		except TypeError: #advanced geometry
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

	def initUI(self):
		if self.nodes == None:
			self.createGeoGroup()
			self.repopulateNodeData()
