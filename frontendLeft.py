from Tkinter import *

class FrontendLeft(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent;
		self.initUI()

	def createNode(self):
		pass

	def deleteNode(self):
		pass

	def createEdge(self):
		pass

	def deleteEdge(self):
		pass

	def selectNode(self):
		pass

	def multiSelect(self):
		pass

	def undo(self):
		pass

	def initUI(self):
		# TODO: create toolbar
		#       create canvas
		#       implement functionality to draw on canvas

		# toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		toolbar = Frame(self.parent, bg="gray")
		toolbar.pack()

		optionList = ('Geometry', '...', 'Create New')
		self.v = StringVar()
		self.v.set(optionList[0])

		dropdown = OptionMenu(toolbar, self.v, *optionList)
		dropdown.pack()
