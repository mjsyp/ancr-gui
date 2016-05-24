from Tkinter import *
import tkSimpleDialog

class FrontendRight(Frame):
	def __init__(self, parent, nodeIndex):
		Frame.__init__(self, parent)
		
		self.parent = parent
		self.nodeIndex = nodeIndex
		self.color = "dark gray"
		self.initUI()

	def createNewType(self):
		typeLabel = tkSimpleDialog.askstring(title="New Type", prompt="Enter a new type")

		if typeLabel != None:
			self.optionList.append(typeLabel)
			self.v.set(self.optionList[len(self.optionList)-1])
			self.dropdown.grid_forget()
			self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
			self.dropdown.configure(bg=self.color)
			self.dropdown.grid(row=2, column=1)

	def createNewDemand(self):
		label = tkSimpleDialog.askstring(title="Label", prompt="Enter a Label Name") # Prompt for label

		if label != None:
			# Create new label and corresponding entry
			self.numAddedDemands += 1
			self.newDemandLabel = Label(self.parent, text=label, bg=self.color)
			self.newDemandLabel.grid(row=3+self.numAddedDemands, column=1)
			self.newDemandEntry = Entry(self.parent, highlightbackground=self.color)
			self.newDemandEntry.grid(row=3+self.numAddedDemands, column=2)

			# Move all other labels/entries down to make room for new demand label
			self.createDemandBtn.grid_forget()
			self.createDemandBtn.grid(row=4+self.numAddedDemands, column=1)
			self.geometryLabel.grid_forget()
			self.geometryLabel.grid(row=5+self.numAddedDemands, column=0)
			self.xLabel.grid_forget()
			self.xLabel.grid(row=5+self.numAddedDemands, column=1)
			self.xEntry.grid_forget()
			self.xEntry.grid(row=5+self.numAddedDemands, column=2)
			self.yLabel.grid_forget()
			self.yLabel.grid(row=6+self.numAddedDemands, column=1)
			self.yEntry.grid_forget()
			self.yEntry.grid(row=6+self.numAddedDemands, column=2)
			self.zLabel.grid_forget()
			self.zLabel.grid(row=7+self.numAddedDemands, column=1)
			self.zEntry.grid_forget()
			self.zEntry.grid(row=7+self.numAddedDemands, column=2)

	def initUI(self):
		#Title
		self.title = Label(self.parent, text="Node " + str(self.nodeIndex), bg=self.color)
		self.title.grid(row=0, columnspan=3, sticky=N)

		# Name
		self.nameLabel = Label(self.parent, text="Name:", bg=self.color)
		self.nameLabel.grid(row=1, column=0)

		self.nameEntry = Entry(self.parent, highlightbackground=self.color)
		self.nameEntry.grid(row=1, column=1, columnspan=2, sticky=E+W)

		# Type
		self.typeLabel = Label(self.parent, text="Type:", bg=self.color)
		self.typeLabel.grid(row=2, column=0)

		self.typeMenu = Frame(self.parent, highlightbackground=self.color)
		self.typeMenu.grid(row=2, column=1)
		self.optionList = ['Hello', 'World']
		self.v = StringVar()
		self.v.set(self.optionList[0])
		self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
		self.dropdown.config(bg=self.color)
		self.dropdown.grid(row=2, column=1)

		self.createTypeBtn = Button(self.parent, text="Create New", 
			command=self.createNewType, highlightbackground=self.color)
		self.createTypeBtn.grid(row=2, column=2)

		# Demand
		self.demandLabel = Label(self.parent, text="Demand:", bg=self.color)
		self.demandLabel.grid(row=3, column=0)

		self.demandLabel2 = Label(self.parent, text="Electric", bg=self.color)
		self.demandLabel2.grid(row=3, column=1, padx=1, pady=1)
		self.demandEntry2 = Entry(self.parent, highlightbackground=self.color)
		self.demandEntry2.grid(row=3, column=2)

		self.numAddedDemands = 0
		self.createDemandBtn = Button(self.parent, text="Create New", 
			command=self.createNewDemand, highlightbackground=self.color)
		self.createDemandBtn.grid(row=4, column=1)

		# Geometry
		self.geometryLabel = Label(self.parent, text="Geometry:", bg=self.color)
		self.geometryLabel.grid(row=5, column=0)

		self.xLabel = Label(self.parent, text="x", bg=self.color)
		self.xLabel.grid(row=5, column=1, padx=1, pady=1)
		self.xEntry = Entry(self.parent, highlightbackground=self.color)
		self.xEntry.grid(row=5, column=2)

		self.yLabel = Label(self.parent, text="y", bg=self.color)
		self.yLabel.grid(row=6, column=1, padx=1, pady=1)
		self.yEntry = Entry(self.parent, highlightbackground=self.color)
		self.yEntry.grid(row=6, column=2)

		self.zLabel = Label(self.parent, text="z", bg=self.color)
		self.zLabel.grid(row=7, column=1, padx=1, pady=1)
		self.zEntry = Entry(self.parent, highlightbackground=self.color)
		self.zEntry.grid(row=7, column=2)

