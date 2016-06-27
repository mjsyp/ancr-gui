from Tkinter import *
from NodeInfo import *
from EdgeInfo import *
import tkSimpleDialog
import networkx as nx
# import matplotlib
# from matplotlib import pyplot as plt
# from PIL import Image, ImageTk

class CanvasFrame(Frame):
	def __init__(self, parent, rightFrame, G, D):
		Frame.__init__(self, parent)

		self.parent = parent
		self.rightFrame = rightFrame
		self.G = G
		self.D = D
		self.color = "light blue"
		self.labels = 0

		# stacks keep track of canvas item ID's as they are created/deleted
		self.undoStack = []
		self.redoStack = []

		self.initUI()

	#toolbar button click events:
	#ALL: first unbinds the old mouse click events 

	#binds mouse clicks to the createNode function when the 'create node' button is pressed 
	def createNodeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.createNode)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')
	
	# binds mouse clicks to the startEdge function and binds mouse click releases to the createEdge
	# function when the 'create edge' button is pressed  
	def createEdgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<ButtonPress-1>', self.edgeStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.createEdge)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')
	
	# binds mouse clicks to the selectEdge function when the 'select edge' button is pressed 
	def selectButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.select)
	
	# binds mouse clicks to the deleteNode function when the 'delete node' button is pressed 
	def deleteButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.delete)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')

	def dragNodeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.dragStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.dragEnd)


	
	"""---------------creation, selection, and deletion of nodes/edges events:---------------"""

	#creates a red circular node of radius r at the location of the mouse click and initilizes node propoerties
	def createNode(self, event):
		r = 8
		item = self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red', tag='node', state='normal') 
		self.G.add_node(item, x=0, y=0, z=0, Name=None, x_coord=event.x, y_coord=event.y)

		self.undoStack.append(item)

		if self.v.get() != "All":
			self.G.node[item][self.v.get()] = 0
			if len(self.rightFrame.winfo_children()) > 0:
				self.systemInfo.repopulateData()

	#determines the x and y coordinates of where the edge will start, checks that starting coords are from a node
	def edgeStart(self, event):
		r = 24
		self.startNode = ()
		self.startNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(self.startNode) > 0:
			self.startNodeCoords = self.systemsCanvas.coords(self.startNode[0])
			self.startNodeX = (self.startNodeCoords[0] + self.startNodeCoords[2]) / 2
			self.startNodeY = (self.startNodeCoords[1] + self.startNodeCoords[3]) / 2

	# determines the x and y coordinates of where the edge will terminate, and then creates a line from startNode to endNode
	# will only allow the creation of an edge to happen between two nodes 
	def createEdge(self, event):
		r = 24
		self.endNode = ()
		self.endNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if (len(self.startNode) > 0) and (len(self.endNode) > 0):
			self.endNodeCoords = self.systemsCanvas.coords(self.endNode[0])
			self.endNodeX = (self.endNodeCoords[0] + self.endNodeCoords[2]) / 2
			self.endNodeY = (self.endNodeCoords[1] + self.endNodeCoords[3]) / 2 	
			item = self.systemsCanvas.create_line(self.startNodeX, self.startNodeY, self.endNodeX, self.endNodeY, tag='edge', state='normal')

			if self.v.get() == 'All':
				self.systemsCanvas.itemconfig(item, arrow='none')
			else:
				self.systemsCanvas.itemconfig(item, arrow='last')


			self.G.add_edge(self.startNode[0], self.endNode[0], x=0, y=0, z=0, Name=None)
			self.systemsCanvas.addtag_withtag(str(self.startNode[0]), item)
			self.systemsCanvas.addtag_withtag(str(self.endNode[0]), item)

			self.G.edge[self.startNode[0]][self.endNode[0]]['x1_coord'] = self.startNodeX
			self.G.edge[self.startNode[0]][self.endNode[0]]['y1_coord'] = self.startNodeY
			self.G.edge[self.startNode[0]][self.endNode[0]]['x2_coord'] = self.endNodeX
			self.G.edge[self.startNode[0]][self.endNode[0]]['y2_coord'] = self.endNodeY

			self.undoStack.append(item)

			if self.v.get() != "All":
				self.G.edge[self.startNode[0]][self.endNode[0]][self.v.get()] = 0
				if len(self.rightFrame.winfo_children()) > 0:
					self.systemInfo.repopulateData()
			

	def select(self, event):
		# clear right pane of any previous info
		for widget in self.rightFrame.winfo_children():
					widget.destroy()

		r = 18
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		# fill all nodes red and all edges black to reset any previously selected item
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')

		if len(selected) > 0:
			if self.systemsCanvas.type(selected[0]) == 'oval':
				self.selectNode(selected[0])
		else:
			r = 4
			selected = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)

			if len(selected) > 0 and self.systemsCanvas.type(selected[0]) == 'line':
				self.selectEdge(selected[0])

	'''changes node color and displays node information'''
	def selectNode(self, item):
		# adjust color of nodes based on selection
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig(item, fill='green')

		self.systemInfo = NodeInfo(self.rightFrame, self, item, self.G, self.optionList)

	'''changes edge color and displays edge information'''
	def selectEdge(self, item):
		# adjust selection color
		self.systemsCanvas.itemconfig('edge', fill='black')
		self.systemsCanvas.itemconfig(item, fill='green')

		# find start and end node of edge
		nodes = [int(n) for n in self.systemsCanvas.gettags(item) if n.isdigit()]
		try:
			self.G[nodes[0]][nodes[1]]
		except KeyError:
			nodes[0], nodes[1] = nodes[1], nodes[0]
		
		self.systemInfo = EdgeInfo(self.rightFrame, self, item, nodes, self.G, self.optionList)


	'''deletes node with ID=item from G_delete; adds node along with attributes to G_add'''
	def deleteNodeNX(self, item, G_delete, G_add):
		G_add.add_node(item)
		for key in G_delete.node[item]:
			G_add.node[item][key] = G_delete.node[item][key]
		#G_delete.remove_node(item)

	'''deletes edge with ID=item from G_delete; adds edge to G_add'''
	def deleteEdgeNX(self, item, G_delete, G_add):
		nodes = [int(n) for n in self.systemsCanvas.gettags(item) if n.isdigit()]

		try:
			self.G[nodes[0]][nodes[1]]
		except KeyError:
			nodes[0], nodes[1] = nodes[1], nodes[0]

		G_add.add_edge(nodes[0], nodes[1])

		# save all attribute info to G_add
		for key in G_delete.edge[nodes[0]][nodes[1]]:
			G_add.edge[nodes[0]][nodes[1]][key] = G_delete.edge[nodes[0]][nodes[1]][key]

		G_delete.remove_edge(nodes[0], nodes[1])


	'''Runs on click of "delete" button; decides whether to call deleteNode or deleteEdge'''
	def delete(self, event):
		r = 18
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		if len(selected) > 0:
			if self.systemsCanvas.type(selected[0]) == 'oval':
				self.deleteNode(event, selected[0])
		else:
			r = 4
			selected = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)

			if len(selected) > 0 and self.systemsCanvas.type(selected[0]) == 'line':
				self.deleteEdge(selected[0])


	'''deletes selected node and any edges overlapping it in both Tkinter and networkX'''
	def deleteNode(self, event, item):
		# find edges overlapping with this node
		r = 16
		overlapped = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)
		numEdges = 0

		for x in overlapped:
			if self.systemsCanvas.type(x) == 'line':
				# add 'deleted' tag to ea. object x, and make it hidden
				self.systemsCanvas.addtag_withtag('deleted', x)
				self.systemsCanvas.itemconfig(x, state='hidden')

				self.undoStack.append(x) # add edge to undo stack
				self.systemsCanvas.dtag(x, 'edge')
				self.deleteEdgeNX(x, self.G, self.D)
				numEdges += 1

		self.systemsCanvas.addtag_withtag('deleted', item)
		self.systemsCanvas.itemconfig(item, state='hidden')
		self.systemsCanvas.dtag(item, 'node')

		self.deleteNodeNX(item, self.G, self.D) # delete node from networkX
		self.G.remove_node(item)
		self.undoStack.append(item) # add node to undo stack; want this to be on top

		# remove label of node if 'Show Labels' is active
		if self.labels == 1:
			self.hideLabels()
			self.showLabels()


	# deletes selected edge with radius r in both Tkinter and networkX
	def deleteEdge(self, item):
		# remove edge from networkX
		self.deleteEdgeNX(item, self.G, self.D)
		
		self.undoStack.append(item)
		self.systemsCanvas.dtag(item, 'edge')
		self.systemsCanvas.addtag_withtag('deleted', item)
		self.systemsCanvas.itemconfig(item, state='hidden')
	
	def dragStart(self, event):
		r = 18
		nodeSelected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(nodeSelected) > 0:
			self.nodeDragItem = nodeSelected[0]
			self.dragStartX = event.x
			self.dragStartY = event.y
		self.edgeItemsDrag = []
		
		edgeSelected = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)
		if (len(edgeSelected) > 0):
			for edge in edgeSelected:
				tag = self.checkTag(edge)
				if tag == 'edge':
					self.edgeItemsDrag.append(edge)



	def dragEnd(self, event):
		# move node:
		self.systemsCanvas.move(self.nodeDragItem, event.x-self.dragStartX, event.y-self.dragStartY)

		# move edges:
		for edge in self.edgeItemsDrag:
			nodes = [int(n) for n in self.systemsCanvas.gettags(edge) if n.isdigit()]
			try:
				self.G[nodes[0]][nodes[1]]
			except KeyError:
				nodes[0], nodes[1] = nodes[1], nodes[0]
			
			edgeCoords = self.systemsCanvas.coords(edge)
			if self.nodeDragItem == nodes[0]:
				self.systemsCanvas.coords(edge, event.x, event.y, edgeCoords[2], edgeCoords[3])
			else:
				self.systemsCanvas.coords(edge, edgeCoords[0], edgeCoords[1], event.x, event.y)


			
			

	
	# shows all node names when' Show Labels' is clicked
	def showLabels(self):
		self.labels = 1
		for item in self.systemsCanvas.find_withtag('node'):
			if self.systemsCanvas.itemcget(item, 'state') !='hidden':
				nodeName = self.G.node[item]['Name']
				if nodeName != None:
					nodeLabel=Label(self.systemsCanvas, text=nodeName)
					nodeLabel.place(x=self.G.node[item]['x_coord'], y=self.G.node[item]['y_coord']-20, anchor='center')

	# hides all node names when 'Hide Labels' is clicked
	def hideLabels(self):
		self.labels = 0
		for widget in self.systemsCanvas.winfo_children():
				widget.destroy()


	def checkTag(self, item):
		for x in self.systemsCanvas.gettags(item):
			if x == 'deleted':
				return 'deleted'
			elif x == 'node':
				return 'node'
			elif x == 'edge':
				return 'edge'
		return 'none'


	def undoRedoAction(self, item):
		tag = self.checkTag(item)

		# check what the tag of the item is to determine which action to undo
		if tag == 'deleted': # item was previously deleted
			self.systemsCanvas.dtag(item, 'deleted') # get rid of 'deleted' tag
			self.systemsCanvas.itemconfig(item, state='normal') # re-show item

			# re-append 'node' or 'edge' tag accordingly
			if self.systemsCanvas.type(item) == 'oval': # node
				self.systemsCanvas.addtag_withtag('node', item)
				self.deleteNodeNX(item, self.D, self.G) # re-add node to networkX

			elif self.systemsCanvas.type(item) == 'line': # edge
				self.systemsCanvas.addtag_withtag('edge', item)
				self.deleteEdgeNX(item, self.D, self.G) # re-add edge to networkX
				
		elif tag == 'node': # node was previously created
			self.deleteNodeNX(item, self.G, self.D) # remove node from networkX

			# remove node and any associated edges from Canvas
			r=4
			coords = self.systemsCanvas.coords(item)
			overlapped = self.systemsCanvas.find_overlapping(coords[0]-r, coords[1]-r, coords[0]+r, coords[1]+r)


			for x in overlapped:
				if self.systemsCanvas.type(x) == 'line':
					# add 'deleted' tag to ea. object x, and make it hidden

					self.systemsCanvas.addtag_withtag('deleted', x)
					self.systemsCanvas.itemconfig(x, state='hidden')

					self.systemsCanvas.dtag(x, 'edge')
					self.deleteEdgeNX(x, self.G, self.D)

			self.systemsCanvas.addtag_withtag('deleted', item)
			self.systemsCanvas.itemconfig(item, state='hidden')
			self.systemsCanvas.dtag(item, 'node')
			self.deleteNodeNX(item, self.G, self.D) # delete node from networkX

		elif tag == 'edge': # edge was previously created
			# remove edge from networkX
			self.deleteEdgeNX(item, self.G, self.D)

			self.systemsCanvas.dtag(item, 'edge')
			self.systemsCanvas.addtag_withtag('deleted', item)
			self.systemsCanvas.itemconfig(item, state='hidden')

		if self.labels == 1:
			self.hideLabels()
			self.showLabels()


	# undo last action performed on canvas (creation or deletion) using a stack
	def undo(self, event=None):
		if len(self.undoStack) > 0:
			item = self.undoStack[len(self.undoStack)-1] # save last item on stack
			self.undoStack.pop() # pop last item from stack
			self.redoStack.append(item) # add to redoStack
			self.undoRedoAction(item)

	def redo(self, event=None):
		if len(self.redoStack) > 0:
			item = self.redoStack[len(self.redoStack)-1]
			self.redoStack.pop()
			self.undoStack.append(item)
			self.undoRedoAction(item)


	# creates new system in option menu and only displays nodes with specific system demands
	def newOptionMenu(self, event):
		if self.v.get() == "Create New":
			typeLabel = tkSimpleDialog.askstring(title="New System", prompt="Enter a new system")
			if typeLabel != None:
				self.optionList.insert(len(self.optionList)-2, typeLabel)
				self.v.set(self.optionList[len(self.optionList)-3])
				self.dropdown.destroy()
				self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
				self.dropdown.configure(bg="light blue")
				self.dropdown.pack(side='left')

				for nodeitem in self.systemsCanvas.find_withtag('node'):
					self.G.node[nodeitem][typeLabel] = None
					self.systemsCanvas.itemconfig(nodeitem, state='hidden')
				for edgeitem in self.systemsCanvas.find_withtag('edge'):
					nodes = [int(n) for n in self.systemsCanvas.gettags(edgeitem) if n.isdigit()]
					try:
						self.G[nodes[0]][nodes[1]]
					except KeyError:
						nodes[0], nodes[1] = nodes[1], nodes[0]
					self.G.edge[nodes[0]][nodes[1]][typeLabel] = None

					self.systemsCanvas.itemconfig(edgeitem, state='hidden')

				# refresh right panel to include new Demand if a node is currently selected
				if len(self.rightFrame.winfo_children()) > 0:
					self.systemInfo.createNewDemand(typeLabel)
					self.systemInfo.systemDict[typeLabel] = None
					self.systemInfo.saveAttributes()

		elif self.v.get() == 'All':
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				self.systemsCanvas.itemconfig(nodeitem, state='normal')
			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				self.systemsCanvas.itemconfig(edgeitem, state='normal')
				self.systemsCanvas.itemconfig(edgeitem, arrow='none')
			
		else:
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				if self.G.node[nodeitem][self.v.get()] == None:
					self.systemsCanvas.itemconfig(nodeitem, state='hidden')
				else:
					self.systemsCanvas.itemconfig(nodeitem, state='normal')

			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				nodes = [int(n) for n in self.systemsCanvas.gettags(edgeitem) if n.isdigit()]
				if (self.systemsCanvas.itemcget(nodes[0], 'state')=='normal') and (self.systemsCanvas.itemcget(nodes[1], 'state')=='normal'):
					self.systemsCanvas.itemconfig(edgeitem, state='normal')
					self.systemsCanvas.itemconfig(edgeitem, arrow='last')
				else:
					self.systemsCanvas.itemconfig(edgeitem, state='hidden')

		if self.labels == 1:
			self.hideLabels()
			self.showLabels()


	# Analysis modules for the networkx graph:

	# shows each nodes degree 
	def nodeDegrees(self):
		# # popout menu to display node degree analysis graph:

		# nodeDegrees = nx.degree(self.G)
		# self.nodeDegreePopup = Toplevel(self.parent)
		# self.nodeDegreePopup.title("Node Degrees")

		# degrees = []
		# for key in nodeDegrees:
		# 	degrees.append(nodeDegrees[key])

	
		# # Create a Figure object.
		# fig = plt.figure(figsize=(6, 5))
		# # Create an Axes object.
		# ax = fig.add_subplot(1,1,1) # one row, one column, first plot
		# # Plot the data.
		# ax.hist(degrees, bins=max(degrees)+1, color="blue", range=(0, max(degrees)+1), align='left')
		# # Add some axis labels.
		# ax.set_xlabel("Degrees")
		# ax.set_ylabel("Frequency")
		# ax.axis([-1, max(degrees)+1, 0, len(degrees)])
		# # Produce an image.
		# fig.savefig("histogramplot.jpg")

		# image = Image.open("histogramplot.jpg")
		# photo = ImageTk.PhotoImage(image)

		# label = Label(self.nodeDegreePopup, image=photo)
		# label.image = photo
		# label.pack()

		# # mini frame to display node degree analysis graph:
		nodeDegreeFrame = Frame(self.miniFrames, height=200, width=200, bg='white', borderwidth=5, relief='sunken')
		nodeDegreeFrame.pack_propagate(0)
		nodeDegreeFrame.pack(side='left')

		toolbarFrame = Frame(nodeDegreeFrame, height=25, width=200, bg='light gray')
		toolbarFrame.pack_propagate(0)
		toolbarFrame.pack(side='top')

		exitButton = Button(toolbarFrame, text='ex', highlightbackground='light gray')
		minButton = Button(toolbarFrame, text='min', highlightbackground='light gray')
		maxButton = Button(toolbarFrame, text='max', highlightbackground='light gray')

		maxButton.pack(side='right')
		minButton.pack(side='right')
		exitButton.pack(side='right')
		
		

		nodeDegrees = nx.degree(self.G)
		degrees = []
		for key in nodeDegrees:
			degrees.append(nodeDegrees[key])

	
		# Create a Figure object.
		fig = plt.figure(figsize=(1.2, 1.2))
		# Create an Axes object.
		ax = fig.add_subplot(1,1,1) # one row, one column, first plot
		# Plot the data.
		ax.hist(degrees, bins=max(degrees)+1, color="blue", range=(0, max(degrees)+1), align='left')
		# Add some axis labels.
		ax.set_xlabel("Degrees")
		ax.set_ylabel("Frequency")
		ax.axis([-1, max(degrees)+1, 0, len(degrees)])
		# Produce an image.
		fig.savefig("histogramplot.jpg")

		image = Image.open("histogramplot.jpg")
		photo = ImageTk.PhotoImage(image)

		label = Label(nodeDegreeFrame, image=photo)
		label.image = photo
		label.pack()


	# Initilizes the toolbar, toolbar buttons, systems menu, and canvas 	
	def initUI(self):
		# creates toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		self.toolbar = Frame(self.parent, bg=self.color)
		self.toolbar.pack()

		#creates systems dropdown menu
		self.optionList = ['All', 'Create New']
		self.v = StringVar()
		self.v.set(self.optionList[len(self.optionList) - 2])

		self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
		self.dropdown.configure(bg=self.color)
		self.dropdown.pack(side='left')

		#creates toolbar buttons, with functionality and binds them to their repsective button click function
		# nodeImage = Image.open('node.gif')
		# nodeImage = nodeImage.resize((50, 50), Image.ANTIALIAS)
		# self.nodeImg = ImageTk.PhotoImage(nodeImage)
		# self.createNodeButton = Button(self.toolbar, image=self.nodeImg, command=self.createNodeButtonClick, 
		# 	highlightbackground=self.color)

		# edgeImage = Image.open('edge.gif')
		# edgeImage = edgeImage.resize((50, 50), Image.ANTIALIAS)		
		# self.edgeImg = ImageTk.PhotoImage(edgeImage)
		# self.createEdgeButton = Button(self.toolbar, image=self.edgeImg, command=self.createEdgeButtonClick,
		# 	highlightbackground=self.color)
		
		# selectImage = Image.open('select.gif')
		# selectImage = selectImage.resize((50, 50), Image.ANTIALIAS)		
		# self.selectImg = ImageTk.PhotoImage(selectImage)
		# self.selectNodeButton = Button(self.toolbar, image=self.selectImg, command=self.selectNodeButtonClick,
		# 	highlightbackground=self.color)
		
		# deleteImage = Image.open('delete.gif')
		# deleteImage = deleteImage.resize((50, 50), Image.ANTIALIAS)		
		# self.deleteImg = ImageTk.PhotoImage(deleteImage)
		# self.deleteNodeButton = Button(self.toolbar, image=self.deleteImg, command=self.deleteNodeButtonClick, 
		# 	highlightbackground=self.color)
		
		self.createNodeButton = Button(self.toolbar, text="create node", command=self.createNodeButtonClick, 
			highlightbackground=self.color)
		self.createEdgeButton = Button(self.toolbar, text="create edge", command=self.createEdgeButtonClick,
			highlightbackground=self.color)
		self.selectButton = Button(self.toolbar, text="select", command=self.selectButtonClick, 
			highlightbackground=self.color)
		self.deleteButton = Button(self.toolbar, text='delete', command=self.deleteButtonClick, 
			highlightbackground=self.color)
		self.dragNodeButton = Button(self.toolbar, text='drag node', command=self.dragNodeButtonClick, 
			highlightbackground=self.color)

		self.dragNodeButton.pack(side='right')
		self.deleteButton.pack(side='right')
		self.selectButton.pack(side='right')
		self.createEdgeButton.pack(side='right')
		self.createNodeButton.pack(side='right')

		#creates canvas 
		self.systemsCanvas = Canvas(self.parent, height=500, width=700, bg='white')
		self.systemsCanvas.pack(fill="both", expand=1)

		self.miniFrames = Frame(self.parent, height=200, width=700, bg='white')
		self.miniFrames.pack_propagate(0)
		self.miniFrames.pack(side='bottom')


