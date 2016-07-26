from Tkinter import *
from Component import *
from Compartment import *
import tkSimpleDialog
import networkx as nx
from datetime import datetime

class NodeEdgeInfo(Frame):
	def __init__(self, parent, leftFrame, index, G, manager, nodes=None):
		Frame.__init__(self, parent)

		self.parent = parent
		self.leftFrame = leftFrame
		self.index = index
		self.G = G
		self.manager = manager
		self.nodes = nodes

		self.systemDict = {}
 		self.color = "dark gray" 
		self.initUI()

	def createTypeLabel(self):
		self.typeLabel = Label(self.propGroup, text="Type:", bg=self.color)
		self.typeLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E+W)

		# initialize default options in dropdown to the list in our Manager
		if self.nodes == None:
			self.optionList = self.manager.nodeTypes
		else:
			self.optionList = self.manager.edgeTypes

		# create a StringVar that holds the selected option in the dropdown
		self.v = StringVar()
		self.v.set(self.optionList[0])

		# actual dropdown
		self.dropdown = OptionMenu(self.propGroup, self.v, *self.optionList, command=self.changeType)
		self.dropdown.config(highlightbackground=self.color, bg=self.color)
		self.dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)

	def changeType(self, event):
		#TODO: change types available for edges
		if self.nodes == None: # if a node is selected rather than an edge
			if self.v.get() == "Create New":
				typeLabel = tkSimpleDialog.askstring(title="New Type", prompt="Enter a new type")

				if typeLabel != None:
					# select new 'type' in dropdown
					self.optionList.insert(len(self.optionList)-1, typeLabel)
					self.v.set(self.optionList[len(self.optionList)-2])

					# redraw dropdown
					self.dropdown.destroy()
					self.dropdown = OptionMenu(self.propGroup, self.v, *self.optionList, command=self.changeType)
					self.dropdown.config(highlightbackground=self.color, bg=self.color)
					self.dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)

			elif self.v.get() == "Component":
				for widget in self.parent.grid_slaves():
					if int(widget.grid_info()['row']) == 1:
						widget.destroy()
				try:
					self.leftFrame.dockedWindows.subNetworkExit()
				except AttributeError:
					pass
				self.componentInfo = Component(self.parent, self.leftFrame, self.index, self.G, self.manager)

			elif self.v.get() == "Compartment":
				for widget in self.parent.grid_slaves():
					if int(widget.grid_info()['row']) == 1:
						widget.destroy()
				self.compartmentInfo = Compartment(self.parent, self.leftFrame, self.index, self.G, self.manager)

	def saveNodeAttributes(self):
		titles = ['Name', 'Type', 'Notes']
		values = [self.nameEntry.get(), self.v.get(), self.notes.get('0.0', END)]

		# for each field, check if value is updated in NetworkX; if not, save and add to 'updated'
		for i in range(0, len(titles)):
			if (titles[i] not in self.G.node[self.index]) or (self.G.node[self.index][titles[i]] != values[i]):
				self.G.node[self.index][titles[i]] = values[i]

		if self.leftFrame.labels == 1:
			self.leftFrame.hideLabels()
			self.leftFrame.showLabels()

		if self.G.node[self.index]['Type'] == 'Component':
			self.componentInfo.saveNodeAttributes()
		else:
			self.compartmentInfo.saveNodeAttributes()
			self.leftFrame.systemsCanvas.itemconfig(self.index, fill='blue')

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Saved attributes of node " + str(self.index)
		self.leftFrame.appendLog(log)

	def saveEdgeAttributes(self):
		titles = ['Name', 'Type', 'Notes']
		values = [self.nameEntry.get(), self.v.get(), self.notes.get('0.0', END)]

		# for each field, check if value is updated in NetworkX; if not, save and add to 'updated'
		for i in range(0, len(titles)):
			if (titles[i] not in self.G.edge[self.nodes[0]][self.nodes[1]]) or (self.G.edge[self.nodes[0]][self.nodes[1]][titles[i]] != values[i]):
				self.G.edge[self.nodes[0]][self.nodes[1]][titles[i]] = values[i]

		# add to log file
		log = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Saved attributes of edge between node " 
 		log = log + str(self.nodes[0]) + " and node " + str(self.nodes[1]) + " (ID = " + str(self.index) + ")"
		self.leftFrame.appendLog(log)

	# inserts networkX data for the node into repsective entry box
	def repopulateNodeData(self):
		if 'Name' in self.G.node[self.index] and self.G.node[self.index]['Name'] != None:
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.node[self.index]['Name'])
		if 'Type' in self.G.node[self.index] and self.G.node[self.index]['Type'] != None:
			self.v.set(self.G.node[self.index]['Type'])
		if 'Notes' in self.G.node[self.index]:
			self.notes.delete('0.0', END)
			self.notes.insert('0.0', self.G.node[self.index]['Notes'])

	# inserts networkX data for the edge into repsective entry box
	def repopulateEdgeData(self):
		if ('Name' in self.G.edge[self.nodes[0]][self.nodes[1]]) and (self.G.edge[self.nodes[0]][self.nodes[1]]['Name'] != None):
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.edge[self.nodes[0]][self.nodes[1]]['Name'])
		if ('Type' in self.G.edge[self.nodes[0]][self.nodes[1]]) and (self.G.edge[self.nodes[0]][self.nodes[1]]['Type'] != None):
			self.v.set(self.G.edge[self.nodes[0]][self.nodes[1]]['Type'])
		if 'Notes' in self.G.edge[self.nodes[0]][self.nodes[1]]:
			self.notes.delete('0.0', END)
			self.notes.insert('0.0', self.G.edge[self.nodes[0]][self.nodes[1]]['Notes'])

	def initUI(self):
		self.propGroup = LabelFrame(self.parent, text="Properties", bg=self.color)
		self.propGroup.grid(row=0, padx=10, sticky=E+W)
		self.propGroup.columnconfigure(0, weight=1)
		self.propGroup.columnconfigure(1, weight=1)
		self.propGroup.columnconfigure(2, weight=1)

		# Name, Type
		self.nameLabel = Label(self.propGroup, text="Name:", bg=self.color)
		self.nameLabel.grid(row=0, column=0, padx=5, pady=(5, 1), sticky=E+W)
		self.nameEntry = Entry(self.propGroup, highlightbackground=self.color)
		self.nameEntry.grid(row=0, column=1, columnspan=2, padx=5, pady=(5, 1), sticky=E+W)
		self.createTypeLabel()

		# Notes
		self.notesGroup = LabelFrame(self.parent, text="Notes", bg=self.color)
		self.notesGroup.grid(row=2, padx=10, sticky=E+W)
		self.notes = Text(self.notesGroup, font='TkDefaultFont', width=1, height=12)
		self.notesGroup.columnconfigure(0, weight=1)
		self.notes.grid(row=0, column=0, padx=5, pady=(1, 5), sticky=E+W)

		# if node attributes have been set previously, populate right pane using the existing data
		if self.nodes == None:
			self.repopulateNodeData()
			self.saveBtn = Button(self.parent, text="Save", command=self.saveNodeAttributes, highlightbackground=self.color)
		else:
			self.repopulateEdgeData()
			self.saveBtn = Button(self.parent, text="Save", command=self.saveEdgeAttributes, highlightbackground=self.color)
		self.saveBtn.grid(row=3, padx=10, pady=5, sticky=E)
		self.changeType(None) # call function so it will display the default 'Type' selection
