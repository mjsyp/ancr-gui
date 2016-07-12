from Tkinter import *
from Manager import *
from NodeInfo import *
from EdgeInfo import *
import tkSimpleDialog
import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
from datetime import datetime

class CanvasFrame(Frame):
	def __init__(self, parent, rightFrame, G, D):
		Frame.__init__(self, parent)

		self.parent = parent
		self.rightFrame = rightFrame
		self.G = G
		self.D = D

		self.initUI()

	"""---------------------------------------------------BUTTON BINDINGS----------------------------------------------------------"""
	def buttonRelief(self, widget):
		buttons = [self.createNodeButton, self.createEdgeButton, self.selectButton, self.deleteButton, self.dragNodeButton]

		for button in buttons:
			button.config(relief=RAISED)
		widget.config(relief=SUNKEN)

	#binds mouse clicks to the createNode function when the 'create node' button is pressed 
	def createNodeButtonClick(self):
		# undo activefill if 'select' button was last pressed
		if self.selectButton.cget('relief') == SUNKEN:
			for node in self.systemsCanvas.find_withtag('node'):
				self.systemsCanvas.itemconfig(node, activefill='red')

		# config all buttons as sunken or raised according to what was pressed
		self.buttonRelief(self.createNodeButton)

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.createNode)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')
	
	# binds mouse clicks to the startEdge function and binds mouse click releases to the createEdge
	# function when the 'create edge' button is pressed  
	def createEdgeButtonClick(self):
		# undo activefill if 'select' button was last pressed
		if self.selectButton.cget('relief') == SUNKEN:
			for node in self.systemsCanvas.find_withtag('node'):
				self.systemsCanvas.itemconfig(node, activefill='red')

		# config all buttons as sunken or raised according to what was pressed
		self.buttonRelief(self.createEdgeButton)

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<ButtonPress-1>', self.edgeStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.createEdge)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')
	
	# binds mouse clicks to the selectEdge function when the 'select edge' button is pressed 
	def selectButtonClick(self):
		# config all buttons as sunken or raised according to what was pressed
		self.buttonRelief(self.selectButton)

		# make nodes green when your cursor scrolls over them
		for node in self.systemsCanvas.find_withtag('node'):
			self.systemsCanvas.itemconfig(node, activefill='green')

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.select)
	
	# binds mouse clicks to the deleteNode function when the 'delete node' button is pressed 
	def deleteButtonClick(self):
		# config all buttons as sunken or raised according to what was pressed
		self.buttonRelief(self.deleteButton)

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.delete)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')

	def dragNodeButtonClick(self):
		# config all buttons as sunken or raised according to what was pressed
		self.buttonRelief(self.dragNodeButton)

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.dragStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.dragEnd)
	"""--------------------------------------------------END BUTTON BINDINGS----------------------------------------------------"""

	
	"""----------------------------------------------------CREATE NODE/EDGE------------------------------------------------------------"""
	#creates a red circular node of radius r at the location of the mouse click and initilizes node propoerties
	def createNode(self, event):
		r = 8
		item = self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red', tag='node', state='normal') 
		self.G.add_node(item, x=0, y=0, z=0, Name=None, x_coord=event.x, y_coord=event.y)

		self.undoStack.append(item)

		# if an node isn't created in 'All', initialize the system demand for this node to 0 instead of None
		if self.v.get() != "All":
			self.G.node[item][self.v.get()] = 0
			if len(self.rightFrame.winfo_children()) > 0:
				self.systemInfo.repopulateData()

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Created new node (ID = " + str(item) + ")"
		self.appendLog(log)

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
		if (len(self.startNode) > 0) and (len(self.endNode) > 0) and (self.startNode[0] != self.endNode[0]):
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
			self.G.edge[self.startNode[0]][self.endNode[0]]['edgeID'] = item

			self.undoStack.append(item)

			# if an edge isn't created in 'All', initialize the system demand for this edge to 0 instead of None
			if self.v.get() != "All":
				self.G.edge[self.startNode[0]][self.endNode[0]][self.v.get()] = 0
				if len(self.rightFrame.winfo_children()) > 0:
					self.systemInfo.repopulateData()

			# add to log file
			log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Created new edge between node " + str(self.startNode[0])
			log += " and node " + str(self.endNode[0]) + " (ID = " + str(item) + ")"
			self.appendLog(log)
	"""---------------------------------------------------END CREATE NODE/EDGE--------------------------------------------------------"""


	"""----------------------------------------------------------SELECT-------------------------------------------------------------------"""
	def select(self, event):
		# clear right pane of any previous info
		for widget in self.rightFrame.winfo_children():
					widget.destroy()

		r = 22
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

		self.systemInfo = NodeInfo(self.rightFrame, self, item, self.G, self.manager)

	'''changes edge color and displays edge information'''
	def selectEdge(self, item):
		# adjust selection color
		self.systemsCanvas.itemconfig('edge', fill='black')
		self.systemsCanvas.itemconfig(item, fill='green')

		# find start and end node of edge
		nodes = [int(n) for n in self.systemsCanvas.gettags(item) if n.isdigit()]
		try:				self.G[nodes[0]][nodes[1]]
		except KeyError:	nodes[0], nodes[1] = nodes[1], nodes[0]
		
		self.systemInfo = EdgeInfo(self.rightFrame, self, item, nodes, self.G, self.manager)
	"""-------------------------------------------------------END SELECT-----------------------------------------------------------"""


	"""---------------------------------------------------------DELETE-------------------------------------------------------------------"""
	'''deletes node with ID=item from G_delete; adds node along with attributes to G_add'''
	def deleteNodeNX(self, item, G_delete, G_add):
		G_add.add_node(item)
		for key in G_delete.node[item]:
			G_add.node[item][key] = G_delete.node[item][key]

	'''deletes edge with ID=item from G_delete; adds edge to G_add'''
	def deleteEdgeNX(self, item, G_delete, G_add):
		nodes = [int(n) for n in self.systemsCanvas.gettags(item) if n.isdigit()]
		try:				self.G[nodes[0]][nodes[1]]
		except KeyError:	nodes[0], nodes[1] = nodes[1], nodes[0]

		G_add.add_edge(nodes[0], nodes[1])

		# save all attribute info to G_add
		for key in G_delete.edge[nodes[0]][nodes[1]]:
			G_add.edge[nodes[0]][nodes[1]][key] = G_delete.edge[nodes[0]][nodes[1]][key]

		G_delete.remove_edge(nodes[0], nodes[1])

	'''Runs on click of "delete" button; decides whether to call deleteNode or deleteEdge'''
	def delete(self, event):
		r = 22
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

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Deleted node " + str(item) + " and associated edges"
		self.appendLog(log)

	# deletes selected edge with radius r in both Tkinter and networkX
	def deleteEdge(self, item):
		# remove edge from networkX
		self.deleteEdgeNX(item, self.G, self.D)
		
		self.undoStack.append(item)
		self.systemsCanvas.dtag(item, 'edge')
		self.systemsCanvas.addtag_withtag('deleted', item)
		self.systemsCanvas.itemconfig(item, state='hidden')

		# add to log file
		nodes = [str(n) for n in self.systemsCanvas.gettags(item) if n.isdigit()]
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Deleted edge between node " + nodes[0] + " and node " + nodes[1]
		log += " (ID = " + str(item) + ")"
		self.appendLog(log)
	"""--------------------------------------------------------END DELETE-----------------------------------------------------------------"""

	
	def dragStart(self, event):
		r = 16
		self.nodeDragItem = None
		nodeSelected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(nodeSelected) > 0:
			self.nodeDragItem = nodeSelected[0]

	def dragEnd(self, event):
		r = 8
		
		# move node:
		if (event.x < 0) or (event.x > 700) or (event.y < 0) or (event.y > 500):
			return

		if self.nodeDragItem != None:
			self.systemsCanvas.coords(self.nodeDragItem, event.x-r, event.y-r, event.x+r, event.y+r)

			# move edges:
			for startNode, endNode in self.G.out_edges([self.nodeDragItem]):
				edge = self.G.edge[startNode][endNode]['edgeID']
				edgeCoordsInt = self.systemsCanvas.coords(edge)
				self.systemsCanvas.coords(edge, event.x, event.y, edgeCoordsInt[2], edgeCoordsInt[3])
				edgeCoordsFin = self.systemsCanvas.coords(edge)
				self.G.edge[startNode][endNode]['x1_coord'] = edgeCoordsFin[0]
				self.G.edge[startNode][endNode]['y1_coord'] = edgeCoordsFin[1]
				self.G.edge[startNode][endNode]['x2_coord'] = edgeCoordsFin[2]
				self.G.edge[startNode][endNode]['y2_coord'] = edgeCoordsFin[3]
			
			for startNode, endNode in self.G.in_edges([self.nodeDragItem]): 
				edge = self.G.edge[startNode][endNode]['edgeID']
				edgeCoordsInt = self.systemsCanvas.coords(edge)				
				self.systemsCanvas.coords(edge, edgeCoordsInt[0], edgeCoordsInt[1], event.x, event.y)
				edgeCoordsFin = self.systemsCanvas.coords(edge)
				self.G.edge[startNode][endNode]['x1_coord'] = edgeCoordsFin[0]
				self.G.edge[startNode][endNode]['y1_coord'] = edgeCoordsFin[1]
				self.G.edge[startNode][endNode]['x2_coord'] = edgeCoordsFin[2]
				self.G.edge[startNode][endNode]['y2_coord'] = edgeCoordsFin[3]

			
			self.G.node[self.nodeDragItem]['x_coord'] = event.x
			self.G.node[self.nodeDragItem]['y_coord'] = event.y

		
		if self.labels == 1:
			self.hideLabels()
			self.showLabels()


	# shows all node names when' Show Labels' is clicked
	def showLabels(self):
		self.labels = 1
		for item in self.systemsCanvas.find_withtag('node'):
			if self.systemsCanvas.itemcget(item, 'state') !='hidden':
				nodeName = self.G.node[item]['Name']
				if nodeName != None:
					nodeLabel=Label(self.systemsCanvas, text=nodeName, background="white")
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

	"""----------------------------------------------------------UNDO/REDO-------------------------------------------------------------------"""
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
				self.undoLog = self.undoLog + "deletion of node " + str(item) + ")" # log message

			elif self.systemsCanvas.type(item) == 'line': # edge
				self.systemsCanvas.addtag_withtag('edge', item)
				self.deleteEdgeNX(item, self.D, self.G) # re-add edge to networkX
				self.undoLog = self.undoLog + "deletion of edge " + str(item) + ")" # log message
				
		elif tag == 'node': # node was previously created
			# remove node from networkX
			self.deleteNodeNX(item, self.G, self.D)
			self.G.remove_node(item)

			# remove node from Canvas
			self.systemsCanvas.addtag_withtag('deleted', item)
			self.systemsCanvas.itemconfig(item, state='hidden')
			self.systemsCanvas.dtag(item, 'node')

			# log message
			self.undoLog = self.undoLog + "creation of node " + str(item) + ")"

		elif tag == 'edge': # edge was previously created
			# remove edge from networkX
			self.deleteEdgeNX(item, self.G, self.D)

			# delete from Canvas
			self.systemsCanvas.dtag(item, 'edge')
			self.systemsCanvas.addtag_withtag('deleted', item)
			self.systemsCanvas.itemconfig(item, state='hidden')

			# log message
			self.undoLog = self.undoLog + "creation of edge " + str(item) + ")"

		if self.labels == 1:
			self.hideLabels()
			self.showLabels()

	# undo last action performed on canvas (creation or deletion) using a stack
	def undo(self, event=None):
		if len(self.undoStack) > 0:
			self.undoLog = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Undo last action (" # log message
			item = self.undoStack[len(self.undoStack)-1] # save last item on stack
			self.undoStack.pop() # pop last item from stack
			self.redoStack.append(item) # add to redoStack
			self.undoRedoAction(item)
			self.appendLog(self.undoLog) # append log message

	def redo(self, event=None):
		if len(self.redoStack) > 0:
			log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Redo last undo" # log message
			item = self.redoStack[len(self.redoStack)-1]
			self.redoStack.pop()
			self.undoStack.append(item)
			self.undoRedoAction(item)
			self.appendLog(log) # append log message
	"""------------------------------------------------------END UNDO/REDO---------------------------------------------------------------"""


	# changes radius of item back to 8
	def normalNodeSize(self, item):
		coords = self.systemsCanvas.coords(item)
		midpointX = (coords[0] + coords[2]) / 2
		midpointY = (coords[1] + coords[3]) / 2
		self.systemsCanvas.coords(item, midpointX-8, midpointY-8, midpointX+8, midpointY+8)

	# creates new system in option menu and only displays nodes with specific system demands
	def newOptionMenu(self, event):
		if self.v.get() == "Create New":
			typeLabel = tkSimpleDialog.askstring(title="New System", prompt="Enter a new system")
			# if user didn't hit 'Cancel'
			if typeLabel != None:
				# Update dropdown menu
				self.optionList.insert(len(self.optionList)-2, typeLabel)
				self.v.set(self.optionList[len(self.optionList)-3])
				self.dropdown.destroy()
				self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
				self.dropdown.configure(bg="light blue", highlightbackground=self.color)
				self.dropdown.pack(side='left')

				# add new system to the list in the Manager class
				self.manager.addSystem(typeLabel)

				# refresh right panel to include new Demand if a node is currently selected
				if len(self.rightFrame.winfo_children()) > 0:
					self.systemInfo.createNewDemand(typeLabel)
					self.systemInfo.systemDict[typeLabel] = None

				# set current selection to prev selection (before 'Create New' was pressed) and update prevOption
				self.v.set(self.prevOption)
				self.prevOption = self.v.get()

				# add to log file
				log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Added new system called '" + typeLabel + "'" 
				self.appendLog(log)

		elif self.v.get() == 'All':
			# make all nodes visible and change size back to normal
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				self.systemsCanvas.itemconfig(nodeitem, state='normal')
				self.normalNodeSize(nodeitem)

			# make all edges visible and remove arrows
			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				self.systemsCanvas.itemconfig(edgeitem, state='normal')
				self.systemsCanvas.itemconfig(edgeitem, arrow='none')

			self.prevOption = "All"

		# switched to a specific system
		else:
			self.minDemand = 1000000000
			self.maxDemand = -1000000000
			visibleNodes = []

			# loop through nodes to show/hide based on the current system
			# also change sizes of nodes back to normal so they don't keep growing
			# also figure out what the min and max value for the current demand is
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				self.normalNodeSize(nodeitem) # change size of each node back to normal

				# if nodeitem has a value for this demand (self.v.get())
				if self.v.get() in self.G.node[nodeitem]:
					visibleNodes.append(nodeitem) # add to a list of visible nodes
					self.systemsCanvas.itemconfig(nodeitem, state='normal') # change state back to normal

					# find minimum and maximum values for this demand
					if self.G.node[nodeitem][self.v.get()] < self.minDemand:
						self.minDemand = self.G.node[nodeitem][self.v.get()]
					if self.G.node[nodeitem][self.v.get()] > self.maxDemand:
						self.maxDemand = self.G.node[nodeitem][self.v.get()]
				else:
					self.systemsCanvas.itemconfig(nodeitem, state='hidden') # make node hidden
			
			if self.minDemand != self.maxDemand:
				for nodeitem in visibleNodes:
					# change size of nodes to reflect magnitude of value for this demand
					coords = self.systemsCanvas.coords(nodeitem)
					x = self.G.node[nodeitem][self.v.get()]
					offset = 10 * (x - self.minDemand) / (self.maxDemand - self.minDemand)
					self.systemsCanvas.coords(nodeitem, coords[0]-offset, coords[1]-offset, coords[2]+offset, coords[3]+offset)

			# loop through edges to show/hide based on whether the nodes are showing or not
			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				nodes = [int(n) for n in self.systemsCanvas.gettags(edgeitem) if n.isdigit()]
				if (self.systemsCanvas.itemcget(nodes[0], 'state') == 'normal') and (self.systemsCanvas.itemcget(nodes[1], 'state') == 'normal'):
					self.systemsCanvas.itemconfig(edgeitem, state='normal')
					self.systemsCanvas.itemconfig(edgeitem, arrow='last')
				else:
					self.systemsCanvas.itemconfig(edgeitem, state='hidden')

			self.prevOption = self.v.get()

		if self.labels == 1:
			self.hideLabels()
			self.showLabels()


	"""----------------------------------------------------NODE DEGREE ANALYSIS------------------------------------------------------------"""
	def nodeDegrees(self):
		if (not hasattr(self, 'nodeDegreeFrame') or self.nodeDegreeFrame.winfo_exists() == 0) and (not hasattr(self, 'nodeDegreePopup') or self.nodeDegreePopup.winfo_exists() == 0):
			# mini frame to display node degree analysis graph:
			self.frameOrWindow = 0
			self.nodeDegreeFrame = Frame(self.miniFrames, height=200, width=200, bg='white', borderwidth=3, relief='raised')
			self.nodeDegreeFrame.pack_propagate(0)
			self.nodeDegreeFrame.pack(side='left', anchor='sw')

			self.toolbarFrame = Frame(self.nodeDegreeFrame, height=25, width=200, bg='light gray')
			self.toolbarFrame.pack_propagate(0)
			self.toolbarFrame.pack(side='top')

			image = Image.open("exit.png")
			self.exitImage = ImageTk.PhotoImage(image)
			#self.exitImage = PhotoImage(file="exit.gif")
			exitButton = Button(self.toolbarFrame, image=self.exitImage, highlightbackground='light gray', command=self.analysisExit)
			image = Image.open("minimize.png")
			self.minImage = ImageTk.PhotoImage(image)
			#self.minImage = PhotoImage(file="minimize.gif")
			minButton = Button(self.toolbarFrame, image=self.minImage, highlightbackground='light gray', command=self.analysisMin)
			image = Image.open("maximize.png")
			self.maxImage = ImageTk.PhotoImage(image)
			#self.maxImage = PhotoImage(file="maximize.gif")
			maxButton = Button(self.toolbarFrame, image=self.maxImage, highlightbackground='light gray', command=self.analysisMax)

			exitButton.pack(side='right')
			maxButton.pack(side='right')
			minButton.pack(side='right')

			nodeDegrees = nx.degree(self.G)
			degrees = []
			for key in nodeDegrees:
				degrees.append(nodeDegrees[key])

			fig = plt.figure(figsize=(1.2, 0.9)) 
			ax = fig.add_subplot(1,1,1) # one row, one column, first plot
			ax.hist(degrees, bins=max(degrees)+1, color="blue", range=(0, max(degrees)+1), align='left') # Plot the data.
			ax.tick_params(axis='both', which='major', labelsize=8)
			ax.tick_params(axis='both', which='minor', labelsize=8)
			ya = ax.get_yaxis()
			ya.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
			xa = ax.get_xaxis()
			xa.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

			# Add some axis labels.
			ax.set_xlabel("Degree", fontsize=10)
			ax.set_ylabel("Frequency", fontsize=10)
			ax.axis([min(degrees)-1, max(degrees)+1, 0, len(degrees)])

			fig.savefig("histogramplot.png", bbox_inches='tight') # Produce an image.
			image = Image.open("histogramplot.png")
			photo = ImageTk.PhotoImage(image)

			label = Label(self.nodeDegreeFrame, image=photo, bg="white")
			label.image = photo
			label.pack(expand=1, fill=BOTH)

		elif self.frameOrWindow == 0:
			self.nodeDegreeFrame.destroy()
			self.nodeDegrees()
		
		elif self.frameOrWindow == 1:
			self.nodeDegreePopup.destroy()
			self.nodeDegrees()

	def analysisExit(self):
		if self.frameOrWindow == 0:
			self.nodeDegreeFrame.destroy()
		else:
			self.nodeDegreePopup.destroy()
	
	def analysisMin(self):
		if self.frameOrWindow == 1:
			self.nodeDegreePopup.destroy()
			self.nodeDegrees()
		else:
			self.nodeDegreeFrame.config(height='30')
	
	def analysisMax(self):
		if self.frameOrWindow == 0 and self.nodeDegreeFrame.winfo_height() > 30:
			self.nodeDegreeFrame.destroy()		

			# popout menu to display node degree analysis graph:
			nodeDegrees = nx.degree(self.G)
			self.frameOrWindow = 1
			self.nodeDegreePopup = Toplevel(self.parent, bg='white')
			self.nodeDegreePopup.title("Node Degrees")
			self.nodeDegreePopup.overrideredirect(1)
			self.nodeDegreePopup.geometry(("%dx%d%+d%+d" % (600, 550, 200, 100)))

			analysisToolbar = Frame(self.nodeDegreePopup, bg='light gray')
			analysisToolbar.pack(side='top', fill='x')
			analysisToolbar.bind('<ButtonPress-1>', self.dragWindowStart)
			analysisToolbar.bind('<ButtonRelease-1>', lambda event: self.dragWindowEnd(event, self.nodeDegreePopup))

			image = Image.open("exit.png")
			self.exitImage2 = ImageTk.PhotoImage(image)
			exitButton = Button(analysisToolbar, image=self.exitImage2, highlightbackground='light gray', command=self.analysisExit)
			image = Image.open("minimize.png")
			self.minImage2 = ImageTk.PhotoImage(image)
			minButton = Button(analysisToolbar, image=self.minImage2, highlightbackground='light gray', command=self.analysisMin)

			exitButton.pack(side='right')
			minButton.pack(side='right')

			degrees = []
			for key in nodeDegrees:
				degrees.append(nodeDegrees[key])

			# Create figure object and axes object
			fig = plt.figure(figsize=(6, 5))
			ax = fig.add_subplot(1,1,1) # one row, one column, first plot

			# plot data and set axis info
			ax.hist(degrees, bins=max(degrees)+1, color="blue", range=(0, max(degrees)+1), align='left') # Plot the data.
			ax.tick_params(axis='both', which='major', labelsize=12)
			ya = ax.get_yaxis()
			ya.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
			xa = ax.get_xaxis()
			xa.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

			# Add some axis labels.
			ax.set_xlabel("Degree", fontsize=18)
			ax.set_ylabel("Frequency", fontsize=19)
			ax.axis([min(degrees)-1, max(degrees)+1, 0, len(degrees)])
			# Produce an image.
			fig.savefig("histogramplot.png", bbox_inches='tight')

			image = Image.open("histogramplot.png")
			photo = ImageTk.PhotoImage(image)

			label = Label(self.nodeDegreePopup, image=photo, bg="white")
			label.image = photo
			label.pack()

		elif self.nodeDegreeFrame.winfo_height() == 30:
			self.nodeDegreeFrame.config(height=200)
	"""----------------------------------------------------END NODE DEGREE ANALYSIS-------------------------------------------------------"""

	def dragWindowStart(self, event):
		self.startDragX = event.x
		self.startDragY = event.y
	
	def dragWindowEnd(self, event, window):
		w = window
		s = w.geometry()
		geometry = s.split('+')
		x = int(geometry[1])+event.x-self.startDragX
		y = int(geometry[2])+event.y-self.startDragY
		if x>0 and y>0:
			w.geometry(("%dx%d%+d%+d" % (600, 550, x, y)))
		elif x>0 and y<0:
			w.geometry(("%dx%d%+d%+d" % (600, 550, x, 0)))
		elif x<0 and y>0:
			w.geometry(("%dx%d%+d%+d" % (600, 550, 0, y)))
		else:
			w.geometry(("%dx%d%+d%+d" % (600, 550, 0, 0)))

	"""---------------------------------------------------------LOG WINDOW----------------------------------------------------------------"""
	def appendLog(self, text):
		if (not hasattr(self, 'logFrame') or  not self.logFrame.winfo_exists()) and (not hasattr(self, 'logPopUp') or self.logPopUp.winfo_exists() == 0) :
			self.logContents += text

		elif self.logFrameOrWindow == 0:
			self.logText.config(state=NORMAL)
			self.logText.insert(END, "\n" + text)
			self.logText.config(state=DISABLED)
			self.logText.see("end")

		else:
			self.logPopUpText.config(state=NORMAL)
			self.logPopUpText.insert(END, "\n" + text)
			self.logPopUpText.config(state=DISABLED)
			self.logPopUpText.see("end")

	# log window to display all actions done on gui	
	def logWindow(self):
		if (not hasattr(self, 'logFrame') or  not self.logFrame.winfo_exists()) and (not hasattr(self, 'logPopUp') or self.logPopUp.winfo_exists() == 0) :
			self.logFrameOrWindow = 0
			self.logFrame = Frame(self.miniFrames, height=200, width=200, bg='white', borderwidth=3, relief='raised')
			self.logFrame.pack_propagate(0)
			self.logFrame.pack(side='left', anchor='sw')

			self.logToolbar = Frame(self.logFrame, height=25, width=200, bg='light gray')
			self.logToolbar.pack_propagate(0)
			self.logToolbar.pack(side='top')

			image = Image.open("exit.png")
			self.exitImage3 = ImageTk.PhotoImage(image)
			exitButton = Button(self.logToolbar, image=self.exitImage3, highlightbackground='light gray', command=self.logExit)
			image = Image.open("minimize.png")
			self.minImage3 = ImageTk.PhotoImage(image)
			minButton = Button(self.logToolbar, image=self.minImage3, highlightbackground='light gray', command=self.logMin)
			image = Image.open("maximize.png")
			self.maxImage3 = ImageTk.PhotoImage(image)
			maxButton = Button(self.logToolbar, image=self.maxImage3, highlightbackground='light gray', command=self.logMax)

			exitButton.pack(side='right')
			maxButton.pack(side='right')
			minButton.pack(side='right')

			self.logScroll = Scrollbar(self.logFrame)
			self.logScroll.pack(side='right', fill='y')
			self.logText = Text(self.logFrame, wrap='word', yscrollcommand=self.logScroll.set, bg='white', borderwidth=0)
			self.logText.pack(expand=1, fill='both')
			self.logScroll.config(command=self.logText.yview)

			# if there is a log file already started, repopulate that text
			if hasattr(self, 'logContents'):
				self.logText.insert(END, self.logContents)
				self.logText.see("end")

			self.logText.config(state=DISABLED)
	
	def logExit(self):
		if self.logFrameOrWindow == 0:
			self.logContents = self.logText.get('1.0', END)
			self.logFrame.destroy()
		else:
			self.logPopUp.destroy()

	def logMin(self):
		if self.logFrameOrWindow == 0:
			self.logFrame.config(height='30')
		else:
			contents = self.logPopUpText.get('1.0', END)
			self.logPopUp.destroy()
			self.logWindow()

			self.logText.config(state=NORMAL)
			self.logText.insert(END, contents)
			self.logText.config(state=DISABLED)
			self.logText.see("end")

	def logMax(self):
		if self.logFrameOrWindow == 0 and self.logFrame.winfo_height() > 30:
			contents = self.logText.get('1.0', END)
			self.logFrame.destroy()
			
			self.logFrameOrWindow = 1
			self.logPopUp = Toplevel(self.parent, bg='white', bd=2, relief=RIDGE)
			self.logPopUp.overrideredirect(1)
			self.logPopUp.geometry(("%dx%d%+d%+d" % (600, 550, 200, 100)))

			self.logPopUpToolbar = Frame(self.logPopUp, height=25, width=600, bg='light gray')
			self.logPopUpToolbar.pack_propagate(0)
			self.logPopUpToolbar.pack(side='top')
			self.logPopUpToolbar.bind('<ButtonPress-1>', self.dragWindowStart)
			self.logPopUpToolbar.bind('<ButtonRelease-1>', lambda event: self.dragWindowEnd(event, self.logPopUp))

			image = Image.open("exit.png")
			self.exitImage4 = ImageTk.PhotoImage(image)
			exitButton = Button(self.logPopUpToolbar, image=self.exitImage4, highlightbackground='light gray', command=self.logExit)
			image = Image.open("minimize.png")
			self.minImage4 = ImageTk.PhotoImage(image)
			minButton = Button(self.logPopUpToolbar, image=self.minImage4, highlightbackground='light gray', command=self.logMin)

			exitButton.pack(side='right')
			minButton.pack(side='right')
			
			self.logPopUpScroll = Scrollbar(self.logPopUp)
			self.logPopUpScroll.pack(side='right', fill='y')
			self.logPopUpText = Text(self.logPopUp, wrap='word', yscrollcommand=self.logPopUpScroll.set, bg='white', borderwidth=0)
			self.logPopUpText.insert(END, contents)
			self.logPopUpText.config(state=DISABLED)
			self.logPopUpText.see("end")
			self.logPopUpText.pack(expand=1, fill='both')
			self.logPopUpScroll.config(command=self.logPopUpText.yview)

		elif self.logFrame.winfo_height() == 30:
			self.logFrame.config(height=200)
	"""--------------------------------------------------END LOG WINDOW-----------------------------------------------------------"""


	# Initilizes the toolbar, toolbar buttons, systems menu, and canvas 	
	def initUI(self):
		# Create manager object that keeps track of all active systems
		self.manager = Manager(self)

		# initialize some variables
		self.color = "light blue"
		self.labels = 0
		self.prevOption = "All"
		self.undoStack = []
		self.redoStack = []

		# creates toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		self.toolbar = Frame(self.parent, bg=self.color)
		self.toolbar.pack()

		#creates systems dropdown menu
		self.optionList = ['All', 'Create New']
		self.v = StringVar()
		self.v.set(self.optionList[len(self.optionList) - 2])

		self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
		self.dropdown.configure(bg=self.color, highlightbackground=self.color)
		self.dropdown.pack(side='left')
		
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

		# creates frame for docked windows
		self.miniFrames = Frame(self.parent, height=200, width=700, bg='white', borderwidth=1, relief='sunken')
		self.miniFrames.pack_propagate(0)
		self.miniFrames.pack(side='bottom', fill="both", expand=1)

		# calls log window function
		self.logWindow()


