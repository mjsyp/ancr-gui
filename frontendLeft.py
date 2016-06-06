from Tkinter import *
from frontendRight import *
import tkSimpleDialog
import networkx as nx

class FrontendLeft(Frame):
	def __init__(self, parent, rightFrame, G, D):
		Frame.__init__(self, parent)

		self.parent = parent
		self.rightFrame = rightFrame
		self.G = G
		self.D = D
		self.color = "light blue"

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
	
	# binds mouse clicks to the startEdge function and binds mouse click releases to the createEdge
	# function when the 'create edge' button is pressed  
	def createEdgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<ButtonPress-1>', self.edgeStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.createEdge)
	
	# binds mouse clicks to the selectNode function when the 'select node' button is pressed 
	def selectNodeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.selectNode)
	
	# binds mouse clicks to the selectEdge function when the 'select edge' button is pressed 
	def selectEdgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.selectEdge)
	
	# binds mouse clicks to the deleteNode function when the 'delete node' button is pressed 
	def deleteNodeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.deleteNode)
	
	# binds mouse clicks to the deleteEdge function when the 'delete edge' button is pressed 
	def deleteEdgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.deleteEdge)


	
	#creation, selection, and deletion of nodes/edges events:

	#creates a red circular node of radius r at the location of the mouse click and initilizes node propoerties
	def createNode(self, event):
		r = 8
		item = self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red', tag='node') 
		self.G.add_node(item, x=0, y=0, z=0, Name=None, x_coord=event.x, y_coord=event.y)

		self.undoStack.append(item)

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
			item = self.systemsCanvas.create_line(self.startNodeX, self.startNodeY, self.endNodeX, self.endNodeY, tag='edge')
			self.G.add_edge(self.startNode[0], self.endNode[0])
			self.systemsCanvas.addtag_withtag(str(self.startNode[0]), item)
			self.systemsCanvas.addtag_withtag(str(self.endNode[0]), item)

			self.undoStack.append(item)
			
	# finds node enclosed by mouse click with a radius of r and displays node information
	def selectNode(self, event):
		r = 24
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		if (len(selected) > 0):
			for widget in self.rightFrame.winfo_children():
				widget.destroy()

			self.systemInfo = FrontendRight(self.rightFrame, selected[0], self.G, self.optionList, 'node')

	# finds edge overlapping mouse click with a radius of r 
	def selectEdge(self, event):
		r = 4
		selected = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(selected) > 0:
			selected_tag = self.systemsCanvas.gettags(selected[0])[0]
			if selected_tag == 'edge':
				for widget in self.rightFrame.winfo_children():
					widget.destroy()

				self.systemInfo = FrontendRight(self.rightFrame, selected[0], self.G, self.optionList, 'edge')
	
	def deleteNodeNX(self, item):
		self.D.add_node(item)
		for key in self.G.node[item]:
			self.D.node[item][key] = self.G.node[item][key]
		self.G.remove_node(item)

	def reAddNodeNX(self, item):
		self.G.add_node(item)
		for key in self.D.node[item]:
			self.G.node[item][key] = self.D.node[item][key]
		self.D.remove_node(item)

	# deletes selected node with radius r and any edges overlapping it in both Tkinter and networkX
	def deleteNode(self, event):
		r = 24
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		if (len(selected) > 0):
			itemTag = self.systemsCanvas.gettags(selected)[0]

			if itemTag == 'node':
				# remove node and any associated edges from NetworkX
				self.deleteNodeNX(selected[0])

				# remove node and any associated edges from Canvas
				overlapped = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)
				for x in overlapped:
					self.undoStack.append(x) # add item to undo stack

					# update tags of item
					self.systemsCanvas.dtag(x, 'node')
					self.systemsCanvas.dtag(x, 'edge')
					self.systemsCanvas.addtag_withtag('deleted', x)
					self.systemsCanvas.itemconfig(x, state='hidden')


	# deletes selected edge with radius r in both Tkinter and networkX
	def deleteEdge(self, event):
		r = 4
		selected = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)

		if len(selected) > 0:
			if self.systemsCanvas.type(selected[0]) == 'line':
				# remove edge from networkX
				nodes = [n for n in self.systemsCanvas.gettags(selected[0]) if n.isdigit()]
				self.G.remove_edge(int(nodes[0]), int(nodes[1]))
				
				self.undoStack.append(selected[0])
				self.systemsCanvas.dtag(selected[0], 'edge')
				self.systemsCanvas.addtag_withtag('deleted', selected[0])
				self.systemsCanvas.itemconfig(selected[0], state='hidden')


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
				#coords = self.systemsCanvas.coords(item)
				#self.G.add_node(item, x=0, y=0, z=0, Name=None, x_coord=coords[0], y_coord=coords[1])
				self.reAddNodeNX(item)
				self.systemsCanvas.addtag_withtag('node', item)

			elif self.systemsCanvas.type(item) == 'line': # edge
				self.systemsCanvas.addtag_withtag('edge', item)

				# re-add edge to networkX
				nodes = [n for n in self.systemsCanvas.gettags(item) if n.isdigit()]
				self.G.add_edge(int(nodes[0]), int(nodes[1]))

		elif tag == 'node': # node was previously created
			self.deleteNodeNX(item) # remove node from networkX

			# remove node and any associated edges from Canvas
			r=4
			coords = self.systemsCanvas.coords(item)
			overlapped = self.systemsCanvas.find_overlapping(coords[0]-r, coords[1]-r, coords[0]+r, coords[1]+r)

			for x in overlapped:
				self.systemsCanvas.dtag(x, 'node')
				self.systemsCanvas.dtag(x, 'edge')
				self.systemsCanvas.addtag_withtag('deleted', x)
				self.systemsCanvas.itemconfig(x, state='hidden')

		elif tag == 'edge': # edge was previously created
			# remove edge from networkX
			nodes = [n for n in self.systemsCanvas.gettags(item) if n.isdigit()]
			self.G.remove_edge(int(nodes[0]), int(nodes[1]))

			self.systemsCanvas.dtag(item, 'edge')
			self.systemsCanvas.addtag_withtag('deleted', item)
			self.systemsCanvas.itemconfig(item, state='hidden')


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
					self.systemsCanvas.itemconfig(edgeitem, state='hidden')

				# refresh right panel to include new Demand
				try:
					self.systemInfo.createNewDemand(typeLabel)
					self.systemInfo.systemDict[typeLabel] = None
					self.systemInfo.saveAttributes()
				# if right panel hasn't been created yet, there will be an Attribute Error
				# there is no point in refreshing so just pass
				except AttributeError: 
					pass

		elif self.v.get() == 'All':
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				self.systemsCanvas.itemconfig(nodeitem, state='normal')
			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				self.systemsCanvas.itemconfig(edgeitem, state='normal')
			
		else:
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				if int(self.G.node[nodeitem][self.v.get()])==0:
					self.systemsCanvas.itemconfig(nodeitem, state='hidden')
				else:
					self.systemsCanvas.itemconfig(nodeitem, state='normal')

			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				if (self.systemsCanvas.itemcget(int(self.systemsCanvas.gettags(edgeitem)[1]), 'state')=='normal') and (self.systemsCanvas.itemcget(int(self.systemsCanvas.gettags(edgeitem)[2]), 'state')=='normal'):
					self.systemsCanvas.itemconfig(edgeitem, state='normal')
				else:
					self.systemsCanvas.itemconfig(edgeitem, state='hidden')

	# Analysis modules for the networkx graph:

	# shows each nodes degree 
	def nodeDegrees(self):
		degrees=nx.degree(self.G)
				

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
		self.createNodeButton = Button(self.toolbar, text="create node", command=self.createNodeButtonClick, 
			highlightbackground=self.color)
		self.createEdgeButton = Button(self.toolbar, text="create edge", command=self.createEdgeButtonClick,
			highlightbackground=self.color)
		self.selectNodeButton = Button(self.toolbar, text="select node", command=self.selectNodeButtonClick,
			highlightbackground=self.color)
		self.selectEdgeButton = Button(self.toolbar, text="select edge", command=self.selectEdgeButtonClick, 
			highlightbackground=self.color)
		self.deleteNodeButton = Button(self.toolbar, text='delete node', command=self.deleteNodeButtonClick, 
			highlightbackground=self.color)
		self.deleteEdgeButton = Button(self.toolbar, text='delete edge', command=self.deleteEdgeButtonClick, 
			highlightbackground=self.color)

		self.deleteEdgeButton.pack(side='right')
		self.deleteNodeButton.pack(side='right')
		self.selectEdgeButton.pack(side='right')
		self.selectNodeButton.pack(side='right')
		self.createEdgeButton.pack(side='right')
		self.createNodeButton.pack(side='right')

		#creates canvas 
		self.systemsCanvas = Canvas(self.parent, height=570, width=700, bg='white')
		self.systemsCanvas.pack(fill="both", expand=1)

