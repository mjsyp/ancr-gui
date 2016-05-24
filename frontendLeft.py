from Tkinter import *
from frontendRight import *
import tkSimpleDialog

class FrontendLeft(Frame):
	def __init__(self, parent, rightFrame):
		Frame.__init__(self, parent)

		self.parent = parent
		self.rightFrame = rightFrame
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
		self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red', tag='node') 
	
	def deleteNode(self):
		pass

	def edgeStart(self, event):
		r = 24
		self.startNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(self.startNode)>0:
			self.startNodeCoords=self.systemsCanvas.coords(self.startNode)
			self.startNodeX=(self.startNodeCoords[0]+self.startNodeCoords[2])/2
			self.startNodeY=(self.startNodeCoords[1]+self.startNodeCoords[3])/2

	def createEdge(self, event):
		r = 24
		self.endNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(self.endNode)>0:
			self.endNodeCoords=self.systemsCanvas.coords(self.endNode)
			self.endNodeX=(self.endNodeCoords[0]+self.endNodeCoords[2])/2
			self.endNodeY=(self.endNodeCoords[1]+self.endNodeCoords[3])/2 
			self.systemsCanvas.create_line(self.startNodeX, self.startNodeY, self.endNodeX, self.endNodeY, tag='edge')

	def deleteEdge(self):
		pass

	def selectNode(self, event):
		r = 24
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		if (len(selected) > 0):
			for widget in self.rightFrame.winfo_children():
				widget.destroy()

			self.systemInfo = FrontendRight(self.rightFrame, selected[0])

	def undo(self, event=None):
		itemList=self.systemsCanvas.find_all()
		lastItemIndex=len(itemList)-1
		self.systemsCanvas.delete(itemList[lastItemIndex])

	# creates new system in option menu
	def newOptionMenu(self, event):
		if self.v.get()=="Create New":
			typeLabel = tkSimpleDialog.askstring(title="New System", prompt="Enter a new system")
			if typeLabel != None:
				self.optionList.insert(len(self.optionList)-1, typeLabel)
				self.v.set(self.optionList[len(self.optionList)-2])
				self.dropdown.destroy()
				self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
				self.dropdown.configure(bg="light blue")
				self.dropdown.pack(side='left')
			
		else:
			self.systemsCanvas.delete('edge')


	def initUI(self):
		# TODO: create toolbar
		#       create canvas
		#       implement functionality to draw on canvas

		# toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		self.toolbar = Frame(self.parent, bg=self.color)
		self.toolbar.pack()

		self.optionList = ['Geometry', 'Electric', 'Egress', 'Information', 'Chill Water', 'All', 'Create New']
		self.v = StringVar()
		self.v.set(self.optionList[0])

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
