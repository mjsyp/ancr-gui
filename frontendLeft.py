from Tkinter import *
from frontendRight import *

class FrontendLeft(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.initUI()

	#toolbar button click events
	def nodeButtonClick(self):
		self.systemsCanvas.bind('<Button-1>', self.createNode)
		self.systemsCanvas.unbind('<ButtonRelease-1>')
	
	def edgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.bind('<ButtonPress-1>', self.edgeStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.createEdge)
	
	def selectButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')

	#creates nodes, edges and selction events
	def createNode(self, event):
		r = 8
		self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red')
	
	def edgeStart(self, event):
		self.edgeStartX=event.x
		self.edgeStartY=event.y
	
	def createEdge(self, event):
		self.systemsCanvas.create_line(self.edgeStartX, self.edgeStartY, event.x, event.y)


	def initUI(self):
		# TODO: create toolbar
		#       create canvas
		#       implement functionality to draw on canvas

		# toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		self.toolbar = Frame(self.parent)
		self.toolbar.pack()

		optionList = ('Geometry', '...', 'Create New')
		self.v = StringVar()
		self.v.set(optionList[0])

		dropdown = OptionMenu(self.toolbar, self.v, *optionList)
		dropdown.pack(side='top')

		#creates toolbar buttons, with functionality 
		nodeButton = Button(self.toolbar, text="node", command=self.nodeButtonClick)
		edgeButton = Button(self.toolbar, text="edge", command=self.edgeButtonClick)
		selectButton = Button(self.toolbar, text="select", command=self.selectButtonClick)
		nodeButton.pack(side='left')
		edgeButton.pack(side='left')
		selectButton.pack(side='left')

		#creates canvas 
		self.systemsCanvas = Canvas(self.parent, height=550, width=600, bg='white')
		self.systemsCanvas.pack()
