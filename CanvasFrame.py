from Tkinter import *
from DockedWindows import *
from Manager import *
from NodeEdgeInfo import *
import tkSimpleDialog
import networkx as nx
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
		# undo activefill 
		self.systemsCanvas.itemconfig('node', activefill='red')
		self.systemsCanvas.itemconfig('edge', activefill='black')

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
		# undo activefill 
		self.systemsCanvas.itemconfig('node', activefill='red')
		self.systemsCanvas.itemconfig('edge', activefill='black')

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

		# make nodes and edges green when your cursor scrolls over them
		self.systemsCanvas.itemconfig('node', activefill='green')
		self.systemsCanvas.itemconfig('edge', activefill='green')

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.select)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')
	
	# binds mouse clicks to the deleteNode function when the 'delete node' button is pressed 
	def deleteButtonClick(self):
		# config all buttons as sunken or raised according to what was pressed
		self.buttonRelief(self.deleteButton)

		# make nodes and edges green when your cursor scrolls over them
		self.systemsCanvas.itemconfig('node', activefill='green')
		self.systemsCanvas.itemconfig('edge', activefill='green')

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.delete)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')

	def dragNodeButtonClick(self):
		# config all buttons as sunken or raised according to what was pressed
		self.buttonRelief(self.dragNodeButton)

		# makes nodes green when you scroll over them in All, and undos activefill on edges
		if self.v.get() == 'All':
			self.systemsCanvas.itemconfig('node', activefill='green')
		else:
			self.systemsCanvas.itemconfig('node', activefill='red')
		self.systemsCanvas.itemconfig('edge', activefill='black')

		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.dragStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.dragEnd)
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')
	"""--------------------------------------------------END BUTTON BINDINGS----------------------------------------------------"""

	
	"""----------------------------------------------------CREATE NODE/EDGE------------------------------------------------------------"""
	#creates a red circular node of radius r at the location of the mouse click and initilizes node propoerties
	def createNode(self, event):
		r = 8
		item = self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red', tag='node', state='normal') 
		self.G.add_node(item, x=0, y=0, z=0, x_coord=event.x, y_coord=event.y, EdgeLength=0)

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

			self.G.add_edge(self.startNode[0], self.endNode[0], Name=None)
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


	def edgeEndpoints(self, edgeitem):
		nodes = [int(n) for n in self.systemsCanvas.gettags(edgeitem) if n.isdigit()]
		try:
			self.G[nodes[0]][nodes[1]]
		except KeyError:
			nodes[0], nodes[1] = nodes[1], nodes[0]
		return nodes


	"""----------------------------------------------------------SELECT-------------------------------------------------------------------"""
	def select(self, event):
		# clear right pane of any previous info
		for widget in self.rightFrame.winfo_children():
					widget.destroy()

		# fill all nodes red and all edges black to reset any previously selected item
		self.systemsCanvas.itemconfig('node', fill='red')
		self.systemsCanvas.itemconfig('edge', fill='black')
		
		if self.systemsCanvas.find_withtag(CURRENT):
			item = self.systemsCanvas.find_withtag(CURRENT)[0]
			self.systemsCanvas.itemconfig(CURRENT, fill="green")
			if self.checkTag(item) == 'node':
				self.systemInfo = NodeEdgeInfo(self.rightFrame, self, item, self.G, self.manager)
				self.dockedWindows.showSubNetwork(item)
			if self.checkTag(item) == 'edge':
				nodes = self.edgeEndpoints(item)
				self.systemInfo = NodeEdgeInfo(self.rightFrame, self, item, self.G, self.manager, nodes)

	"""-------------------------------------------------------END SELECT-----------------------------------------------------------"""


	"""---------------------------------------------------------DELETE-------------------------------------------------------------------"""
	'''deletes node with ID=item from G_delete; adds node along with attributes to G_add'''
	def deleteNodeNX(self, item, G_delete, G_add):
		G_add.add_node(item)
		for key in G_delete.node[item]:
			G_add.node[item][key] = G_delete.node[item][key]

	'''deletes edge with ID=item from G_delete; adds edge to G_add'''
	def deleteEdgeNX(self, item, G_delete, G_add):
		nodes = self.edgeEndpoints(item)

		G_add.add_edge(nodes[0], nodes[1])

		# save all attribute info to G_add
		for key in G_delete.edge[nodes[0]][nodes[1]]:
			G_add.edge[nodes[0]][nodes[1]][key] = G_delete.edge[nodes[0]][nodes[1]][key]

		G_delete.remove_edge(nodes[0], nodes[1])

	'''Runs on click after "delete" button is pressed'''
	def delete(self, event):
		if self.systemsCanvas.find_withtag(CURRENT):
			item = self.systemsCanvas.find_withtag(CURRENT)[0]
			'''deletes selected node and any edges overlapping it in both Tkinter and networkX if system is All'''
			if self.v.get() == 'All':
				if self.checkTag(item) == 'node':
					nodeCoords = self.systemsCanvas.coords(item)
					overlapped = self.systemsCanvas.find_overlapping(nodeCoords[0], nodeCoords[1], nodeCoords[2], nodeCoords[3])
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

					# adxsd to log file
					log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Deleted node " + str(item) + " and associated edges"
					self.appendLog(log)
					
				''' deletes selected edge from networkx and Tkinter if system is All'''
				if self.checkTag(item) == 'edge':
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

			else:
				''' if system is not All, then removes that specific demand for that node and its associated edges'''
				if self.checkTag(item) == 'node':
					nodeCoords = self.systemsCanvas.coords(item)
					overlapped = self.systemsCanvas.find_overlapping(nodeCoords[0], nodeCoords[1], nodeCoords[2], nodeCoords[3])
					for x in overlapped:
						if self.checkTag(x) == 'edge':
							self.systemsCanvas.itemconfig(x, state='hidden')
					self.systemsCanvas.itemconfig(item, state='hidden')
					del self.G.node[item][self.v.get()]
				''' if system is not All, then removes that specific demand for the edge'''
				if self.checkTag(item) == 'edge':
					nodes = [int(n) for n in self.systemsCanvas.gettags(item) if n.isdigit()]
					try:				
						self.G[nodes[0]][nodes[1]]
					except KeyError:	
						nodes[0], nodes[1] = nodes[1], nodes[0]
					self.systemsCanvas.itemconfig(item, state='hidden')
					del self.G.edge[nodes[0]][nodes[1]][self.v.get()]

		# refreshes labels if show labels is active
		if self.labels == 1:
			self.hideLabels()
			self.showLabels()

	"""--------------------------------------------------------END DELETE-----------------------------------------------------------------"""

	# selects node on button press and moves node to location at button release
	def dragStart(self, event):
		self.nodeDragItem = None
		if self.systemsCanvas.find_withtag(CURRENT):
			item = self.systemsCanvas.find_withtag(CURRENT)[0]
			if self.checkTag(item) == 'node':
				self.nodeDragItem = item

	def dragEnd(self, event):
		r = 8
		# will only move node if it's in All
		if self.v.get() == 'All':
			# move node:
			if (event.x < 0) or (event.x > self.systemsCanvas.winfo_width()) or (event.y < 0) or (event.y > self.systemsCanvas.winfo_height()):
				return

			if self.nodeDragItem != None:
				self.systemsCanvas.coords(self.nodeDragItem, event.x-r, event.y-r, event.x+r, event.y+r)

				# move edges:
				for startNode, endNode in self.G.out_edges([self.nodeDragItem]):
					edge = self.G.edge[startNode][endNode]['edgeID']
					edgeCoordsInt = self.systemsCanvas.coords(edge)
					self.systemsCanvas.coords(edge, event.x, event.y, edgeCoordsInt[2], edgeCoordsInt[3])
					edgeCoordsFin = self.systemsCanvas.coords(edge)
					# saves new edge coordinates
					self.G.edge[startNode][endNode]['x1_coord'] = edgeCoordsFin[0]
					self.G.edge[startNode][endNode]['y1_coord'] = edgeCoordsFin[1]
					self.G.edge[startNode][endNode]['x2_coord'] = edgeCoordsFin[2]
					self.G.edge[startNode][endNode]['y2_coord'] = edgeCoordsFin[3]
				
				for startNode, endNode in self.G.in_edges([self.nodeDragItem]): 
					edge = self.G.edge[startNode][endNode]['edgeID']
					edgeCoordsInt = self.systemsCanvas.coords(edge)				
					self.systemsCanvas.coords(edge, edgeCoordsInt[0], edgeCoordsInt[1], event.x, event.y)
					edgeCoordsFin = self.systemsCanvas.coords(edge)
					# saves new edge coordinates
					self.G.edge[startNode][endNode]['x1_coord'] = edgeCoordsFin[0]
					self.G.edge[startNode][endNode]['y1_coord'] = edgeCoordsFin[1]
					self.G.edge[startNode][endNode]['x2_coord'] = edgeCoordsFin[2]
					self.G.edge[startNode][endNode]['y2_coord'] = edgeCoordsFin[3]

				# saves new node coordinates
				self.G.node[self.nodeDragItem]['x_coord'] = event.x
				self.G.node[self.nodeDragItem]['y_coord'] = event.y

			# refreshes labels if show labels is active
			if self.labels == 1:
				self.hideLabels()
				self.showLabels()


	# shows all node names when 'Show Labels' is clicked
	def showLabels(self):
		self.labels = 1
		for item in self.systemsCanvas.find_withtag('node'):
			if self.systemsCanvas.itemcget(item, 'state') !='hidden':
				if 'Name' in self.G.node[item]:
					nodeName = self.G.node[item]['Name']
					nodeCoords = self.systemsCanvas.coords(item)
					radius = (nodeCoords[2]-nodeCoords[0])/2
					nodeLabel=Label(self.systemsCanvas, text=nodeName, background="white")
					nodeLabel.place(x=self.G.node[item]['x_coord'], y=self.G.node[item]['y_coord']-12-radius, anchor='center')

	# hides all node names when 'Hide Labels' is clicked
	def hideLabels(self):
		self.labels = 0
		for widget in self.systemsCanvas.winfo_children():
				widget.destroy()

	# check type of item or whether it has been deleted 
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

	# changes radius of item back to 8 and removes '+', '-', or '0' label
	def normalNodeSize(self, item):
		coords = self.systemsCanvas.coords(item)
		midpointX = (coords[0] + coords[2]) / 2
		midpointY = (coords[1] + coords[3]) / 2
		self.systemsCanvas.coords(item, midpointX-8, midpointY-8, midpointX+8, midpointY+8)

	def scaleNodeSize(self, nodeitem):
		# change size of nodes to reflect magnitude of value for this demand
		coords = self.systemsCanvas.coords(nodeitem)
		demand = self.G.node[nodeitem][self.v.get()]
		offset = 10 * (abs(demand) - self.minDemand) / (self.maxDemand - self.minDemand)
		self.systemsCanvas.coords(nodeitem, coords[0]-offset, coords[1]-offset, coords[2]+offset, coords[3]+offset)

		# places a label on each visible node indicating whether the demand is positive or negative
		if demand < 0:
			labelText = '-'
		elif demand > 0:
			labelText = '+'
		else:
			labelText = '0'
		self.systemsCanvas.create_text(self.G.node[nodeitem]['x_coord'], self.G.node[nodeitem]['y_coord'], 
			text=labelText, tag='label', state=DISABLED, fill='white')

	# creates new system in option menu and only displays nodes with specific system demands
	def newOptionMenu(self, event):
		if self.v.get() == "Create New":
			typeLabel = tkSimpleDialog.askstring(title="New System", prompt="Enter a new system")
			# if user didn't hit 'Cancel'
			if typeLabel != None:
				# Update dropdown menu
				self.optionList.insert(len(self.optionList)-2, typeLabel)
				self.dropdown.destroy()
				self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
				self.dropdown.configure(highlightbackground="light blue", bg='light blue')
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
				self.systemsCanvas.delete('label')

			# make all edges visible and remove arrows
			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				self.systemsCanvas.itemconfig(edgeitem, state='normal')
				self.systemsCanvas.itemconfig(edgeitem, arrow='none')

			self.prevOption = "All"

		# switched to a specific system
		else:
			if self.prevOption != self.v.get():
				self.minDemand = 1000000000
				self.maxDemand = -1
				visibleNodes = []

				# loop through nodes to show/hide based on the current system
				# also change sizes of nodes back to normal so they don't keep growing
				# also figure out what the min and max value for the current demand is
				for nodeitem in self.systemsCanvas.find_withtag('node'):
					self.normalNodeSize(nodeitem) # change size of each node back to normal
					self.systemsCanvas.delete('label') # remove '+' or '-' label

					# if nodeitem has a value for this demand (self.v.get())
					if self.v.get() in self.G.node[nodeitem]:
						visibleNodes.append(nodeitem) # add to a list of visible nodes
						self.systemsCanvas.itemconfig(nodeitem, state='normal') # change state back to normal

						# find minimum and maximum values for this demand
						thisDemand = self.G.node[nodeitem][self.v.get()]
						if abs(thisDemand) < self.minDemand:
							self.minDemand = abs(thisDemand)
						if abs(thisDemand) > self.maxDemand:
							self.maxDemand = abs(thisDemand)
					else:
						self.systemsCanvas.itemconfig(nodeitem, state='hidden') # make node hidden
				
				# if they dont all have the same demand (minDemand=maxDemand)
				if self.minDemand != self.maxDemand:
					for nodeitem in visibleNodes:
						self.scaleNodeSize(nodeitem) # then scale nodes based on magnitude of demand

				# loop through edges to show/hide based on whether the nodes are showing or not
				for edgeitem in self.systemsCanvas.find_withtag('edge'):
					nodes = self.edgeEndpoints(edgeitem)
					if (self.systemsCanvas.itemcget(nodes[0], 'state') == 'normal') and \
					   (self.systemsCanvas.itemcget(nodes[1], 'state') == 'normal') and \
					   (self.v.get() in self.G.edge[nodes[0]][nodes[1]]) :
						self.systemsCanvas.itemconfig(edgeitem, state='normal')
						self.systemsCanvas.itemconfig(edgeitem, arrow='last')
					else:
						self.systemsCanvas.itemconfig(edgeitem, state='hidden')

			self.prevOption = self.v.get()

		# refreshes labels if show labels is active
		if self.labels == 1:
			self.hideLabels()
			self.showLabels()


	def appendLog(self, text):
		if (not hasattr(self.dockedWindows, 'logFrame') or not self.dockedWindows.logFrame.winfo_exists()) and \
		   (not hasattr(self.dockedWindows, 'logPopUp') or self.dockedWindows.logPopUp.winfo_exists() == 0) :
			self.dockedWindows.logContents += text
		elif self.dockedWindows.logFrameOrWindow == 0:
			self.dockedWindows.logText.config(state=NORMAL)
			self.dockedWindows.logText.insert(END, "\n" + text)
			self.dockedWindows.logText.config(state=DISABLED)
			self.dockedWindows.logText.see("end")
		else:
			self.dockedWindows.logPopUpText.config(state=NORMAL)
			self.dockedWindows.logPopUpText.insert(END, "\n" + text)
			self.dockedWindows.logPopUpText.config(state=DISABLED)
			self.dockedWindows.logPopUpText.see("end")


	# Initilizes the toolbar, toolbar buttons, systems menu, and canvas 	
	def initUI(self):
		# Create manager object that keeps track of all active systems
		self.manager = Manager(self)

		# initialize some variables
		self.color = "light blue"
		self.labels = 0
		self.prevOption = "All"
		#self.logContents = ""
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
		self.dropdown.configure(bg="light blue", highlightbackground="light blue")
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

		self.dockedWindows = DockedWindows(self.miniFrames, self.G) # creates docked analysis windows
