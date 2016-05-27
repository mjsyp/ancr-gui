from Tkinter import *
from frontendRight import *
import tkSimpleDialog
import networkx as nx

class FrontendLeft(Frame):
	def __init__(self, parent, rightFrame, G):
		Frame.__init__(self, parent)

		self.parent = parent
		self.rightFrame = rightFrame
		self.G = G
		self.color = "light blue"
		self.initUI()

	#toolbar button click events
	def nodeButtonClick(self):
		self.nodeButton.configure(relief=SUNKEN)
		self.systemsCanvas.bind('<Button-1>', self.createNode)
		self.systemsCanvas.unbind('<ButtonRelease-1>')
	
	def edgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.bind('<ButtonPress-1>', self.edgeStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.createEdge)
	
	def selectButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.selectNode)

	#creates nodes, edges and selection events
	def createNode(self, event):
		r = 8
		item=self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red', tag='node') 
		self.G.add_node(item, Geometry=0, Electric=0, Egress=0, Information=0, x=0, y=0, z=0, Name=None)
		self.G.node[item]['Chill Water']=0

	def deleteNode(self):
		pass

	def edgeStart(self, event):
		r = 24
		self.startNode=()
		self.startNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(self.startNode)>0:
			self.startNodeCoords=self.systemsCanvas.coords(self.startNode[0])
			self.startNodeX=(self.startNodeCoords[0]+self.startNodeCoords[2])/2
			self.startNodeY=(self.startNodeCoords[1]+self.startNodeCoords[3])/2

	def createEdge(self, event):
		r = 24
		self.endNode=()
		self.endNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if (len(self.startNode)>0) and (len(self.endNode)>0):
			self.endNodeCoords=self.systemsCanvas.coords(self.endNode[0])
			self.endNodeX=(self.endNodeCoords[0]+self.endNodeCoords[2])/2
			self.endNodeY=(self.endNodeCoords[1]+self.endNodeCoords[3])/2 	
			item=self.systemsCanvas.create_line(self.startNodeX, self.startNodeY, self.endNodeX, self.endNodeY, tag='edge')
			self.G.add_edge(self.startNode[0], self.endNode[0])
			self.systemsCanvas.addtag_withtag(str(self.startNode[0]), item)
			self.systemsCanvas.addtag_withtag(str(self.endNode[0]), item)
			


	def deleteEdge(self):
		pass

	def selectNode(self, event):
		r = 24
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		if (len(selected) > 0):
			for widget in self.rightFrame.winfo_children():
				widget.destroy()

			self.systemInfo = FrontendRight(self.rightFrame, selected[0], self.G, self.optionList)

	# deletes last object created on the canvas
	def undo(self, event=None):
		itemList=self.systemsCanvas.find_all()
		if len(itemList)>0:
			lastItemIndex=len(itemList)-1
			lastItemTag=self.systemsCanvas.gettags(itemList[lastItemIndex])[0]
			if lastItemTag=='node':
				self.G.remove_node(itemList[lastItemIndex])
			elif lastItemTag=='edge':
				self.G.remove_edge(int(self.systemsCanvas.gettags(itemList[lastItemIndex])[1]), int(self.systemsCanvas.gettags(itemList[lastItemIndex])[2]))
			self.systemsCanvas.delete(itemList[lastItemIndex])




	# creates new system in option menu and only displays nodes with specific system demands
	def newOptionMenu(self, event):
		if self.v.get()=="Create New":
			typeLabel = tkSimpleDialog.askstring(title="New System", prompt="Enter a new system")
			if typeLabel != None:
				for nodeitem in self.systemsCanvas.find_withtag('node'):
					self.G.node[nodeitem][typeLabel] = 0

				self.optionList.insert(len(self.optionList)-2, typeLabel)
				self.v.set(self.optionList[len(self.optionList)-2])
				self.dropdown.destroy()
				self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
				self.dropdown.configure(bg="light blue")
				self.dropdown.pack(side='left')



		elif self.v.get()=='All':
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				self.systemsCanvas.itemconfig(nodeitem, state='normal')
			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				self.systemsCanvas.itemconfig(edgeitem, state='normal')
			
		else:
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				if int(self.G.node[nodeitem][self.v.get()]) != int(0):
					print "Node " + str(nodeitem) + ": " + str(self.G.node[nodeitem][self.v.get()])
					self.systemsCanvas.itemconfig(nodeitem, state='normal')
				else:
					self.systemsCanvas.itemconfig(nodeitem, state='hidden')

			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				if (self.systemsCanvas.itemcget(int(self.systemsCanvas.gettags(edgeitem)[1]), 'state')=='normal') and (self.systemsCanvas.itemcget(int(self.systemsCanvas.gettags(edgeitem)[2]), 'state')=='normal'):
					self.systemsCanvas.itemconfig(edgeitem, state='normal')
				else:
					self.systemsCanvas.itemconfig(edgeitem, state='hidden')
				

			


	def initUI(self):
		# toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		self.toolbar = Frame(self.parent, bg=self.color)
		self.toolbar.pack()

		self.optionList = ['Geometry', 'Electric', 'Egress', 'Information', 'Chill Water', 'All', 'Create New']
		self.v = StringVar()
		self.v.set(self.optionList[5])

		self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
		self.dropdown.configure(bg=self.color)
		self.dropdown.pack(side='left')

		#creates toolbar buttons, with functionality 
		self.nodeButton = Button(self.toolbar, text="node", command=self.nodeButtonClick,
                        highlightbackground=self.color)
		self.edgeButton = Button(self.toolbar, text="edge", command=self.edgeButtonClick,
                        highlightbackground=self.color)
		self.selectButton = Button(self.toolbar, text="select", command=self.selectButtonClick,
                          highlightbackground=self.color)
		self.selectButton.pack(side='right')
		self.edgeButton.pack(side='right')
		self.nodeButton.pack(side='right')

		#creates canvas 
		self.systemsCanvas = Canvas(self.parent, height=570, width=600, bg='white')
		self.systemsCanvas.pack(fill="both", expand=1)

