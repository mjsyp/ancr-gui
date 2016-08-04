'''
 * Compartment.py
 * 
 * Assumes the selected node is of type compartment;
 * adds a box where geometry of this compartment can be
 * specified
 * 
 * Major functionalities include:
 *     geometry box
 *     add/delete rows in geometry
 *     save/repopulate
'''
try:
	from Tkinter import *
	import tkMessageBox
	import networkx as nx
	import matplotlib
	from matplotlib import pyplot as plt
	from mpl_toolkits.mplot3d import Axes3D
	import numpy as np
	from itertools import product, combinations
	import networkx as nx
	from PIL import Image, ImageTk
	from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
	from matplotlib.figure import Figure 
except ImportError, e:
	tkMessageBox.showinfo("Import Error", "Error: " + str(e))

class Compartment(Frame):
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

	def createGeometry(self):
		self.geoGroup = LabelFrame(self.parent, text="Geometry", bg=self.color)
		self.geoGroup.grid(row=1, padx=10, sticky=E+W)

		self.numCoords = 1

		# initilize entry widget lists
		self.xEntryList = []
		self.yEntryList = []
		self.zEntryList = []
		self.edgeEntryList = []
		
		self.createNewGeo()
 
		# create new coord button
		self.newCoordBtn = Button(self.geoGroup, text="Add Row", command=self.createNewGeo, bg=self.color, highlightbackground=self.color)
		self.newCoordBtn.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky=E+W)

		self.showGeoBtn = Button(self.geoGroup, text='Show Geometry', command=self.showGeometry, bg=self.color, highlightbackground=self.color)
		self.showGeoBtn.grid(row=0, column=6, columnspan=4, padx=5, pady=5, sticky=E+W)

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

	def deleteGeo(self, event):
		deleteRow = int(event.widget.grid_info()['row']) # row # to delete
		# delete the info in this row from networkx
		self.G.node[self.index]['x'].pop(deleteRow-1)
		self.G.node[self.index]['y'].pop(deleteRow-1)
		self.G.node[self.index]['z'].pop(deleteRow-1)
		self.G.node[self.index]['EdgeLength'].pop(deleteRow-1)
		# remove the info in this row from our lists of widgets
		self.xEntryList.pop(deleteRow-1)
		self.yEntryList.pop(deleteRow-1)
		self.zEntryList.pop(deleteRow-1)
		self.edgeEntryList.pop(deleteRow-1)

		# for each widget in the geometry box
		for widget in self.geoGroup.grid_slaves():
			thisRow = int(widget.grid_info()['row']) # current row

			# delete specified row to be deleted
			if thisRow == deleteRow:
				widget.grid_forget()
			# move up rows below it and renumber the row
			elif thisRow > deleteRow:
				widget.grid_configure(row=thisRow-1)
				if int(widget.grid_info()['column']) == 0:
					widget.config(text=str(thisRow-1)+".")

		self.numCoords -= 1

	def saveNodeAttributes(self):
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

		self.leftFrame.dockedWindows.showSubNetwork(self.index)

	# inserts networkX data for the node into repsective entry box
	def repopulateNodeData(self):
		try:
			# fill row 0 with data saved in networkx if it exists
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, self.G.node[self.index]['x'][0])
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, self.G.node[self.index]['y'][0])
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, self.G.node[self.index]['z'][0])
			self.edgeEntry.delete(0, END)
			self.edgeEntry.insert(0, self.G.node[self.index]['EdgeLength'][0])

			# add a new row for each row of saved data that exists
			# and fill it with data saved in networkx
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
		
		# no data in networkx yet
		except TypeError:
			self.xEntry.insert(0, 0) # undo the delete of xEntry before exception was caught
	
	def showGeometry(self):
		geoWindow = Toplevel(height=300, width=500)
		geoWindow.title('Compartment/Component Geometry')

		fig = Figure()
		canvas = FigureCanvasTkAgg(fig, master=geoWindow)
		
		ax = fig.add_subplot(111, projection='3d')
		xs = []
		ys = []
		zs = []

		# loops through each node with type: component and builds a 3D scatterplot of their x, y, z coordinates
		for node in nx.all_neighbors(self.G, self.index):
			if 'Type' in self.G.node[node]:
				if self.G.node[node]['Type'] == 'Component':
					xs.append(int(self.G.node[node]['x']))
					ys.append(int(self.G.node[node]['y']))
					zs.append(int(self.G.node[node]['z']))

		for i in range(0, len(self.G.node[self.index]['x'])):	
			a = self.G.node[self.index]['EdgeLength'][i]
			x = self.G.node[self.index]['x'][i]
			y = self.G.node[self.index]['y'][i]
			z = self.G.node[self.index]['z'][i]
			hSL = float(a/2)
			r = [-hSL, hSL]
			rX = [-hSL + x, hSL + x]
			rY = [-hSL + y, hSL + y]
			rZ = [-hSL + z, hSL + z]
			for s, e in combinations(np.array(list(product(rX,rY,rZ))), 2):
				if not np.sum(np.abs(s-e)) > a+0.0000001:
					ax.plot3D(*zip(s,e), color="b")

		ax.scatter(xs, ys, zs, c='r', marker='o')
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		
		# creates the matplotlib navigation toolbar
		canvas.show()
		canvas.get_tk_widget().configure(borderwidth=0, highlightbackground='gray', highlightcolor='gray', selectbackground='gray')
		canvas.get_tk_widget().pack()
		toolbar = NavigationToolbar2TkAgg(canvas, geoWindow)
		toolbar.update()

	def initUI(self):
		self.createGeometry()
		self.repopulateNodeData()
		self.leftFrame.dockedWindows.showSubNetwork(self.index)
