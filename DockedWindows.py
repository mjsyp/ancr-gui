from Tkinter import *
import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import math

class DockedWindows(Frame):
	def __init__(self, parent, G):
		Frame.__init__(self, parent)

		self.parent = parent
		self.G = G

		self.initUI()
	"""----------------------------------------------------NODE DEGREE ANALYSIS-------------------------------------------------------"""
	# docked window frame to display histogram of node degrees
	def nodeDegrees(self):
		if len(self.G.nodes()) > 0 and \
		  (not hasattr(self, 'nodeDegreeFrame') or self.nodeDegreeFrame.winfo_exists() == 0) and \
		  (not hasattr(self, 'nodeDegreePopup') or self.nodeDegreePopup.winfo_exists() == 0):
			# mini frame to display node degree analysis graph:
			self.frameOrWindow = 0 # 0 - frame, 1 - popup window
			self.nodeDegreeFrame = Frame(self.parent, height=200, width=200, bg='white', borderwidth=3, relief='raised')
			self.nodeDegreeFrame.pack_propagate(0)
			self.nodeDegreeFrame.pack(side='left', anchor='nw', fill='y')

			# toolbar to store max, min, exit buttons
			self.toolbarFrame = Frame(self.nodeDegreeFrame, bg='light gray')
			self.toolbarFrame.pack(side='top', fill='x')

			# toolbar label
			analysisToolbarLabel = Label(self.toolbarFrame, text="Node Degrees", bg='light gray')
			analysisToolbarLabel.pack(side='left')

			# creates images for the buttons on the toolbar
			image = Image.open("exit.png") 
			self.exitImage = ImageTk.PhotoImage(image)
			exitButton = Button(self.toolbarFrame, image=self.exitImage, highlightbackground='light gray', command=self.analysisExit)
			image = Image.open("minimize.png")
			self.minImage = ImageTk.PhotoImage(image)
			minButton = Button(self.toolbarFrame, image=self.minImage, highlightbackground='light gray', command=self.analysisMin)
			image = Image.open("maximize.png")
			self.maxImage = ImageTk.PhotoImage(image)
			maxButton = Button(self.toolbarFrame, image=self.maxImage, highlightbackground='light gray', command=self.analysisMax)

			exitButton.pack(side='right')
			maxButton.pack(side='right')
			minButton.pack(side='right')

			# creates list of nodeDegrees
			nodeDegrees = nx.degree(self.G)
			degrees = []
			for key in nodeDegrees:
				degrees.append(nodeDegrees[key])

			# creates histogram
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

			# saves figure
			fig.savefig("histogramplot.png", bbox_inches='tight') # Produce an image.
			image = Image.open("histogramplot.png")
			photo = ImageTk.PhotoImage(image)

			# displays figure on a label in the frame
			label = Label(self.nodeDegreeFrame, image=photo, bg="white")
			label.image = photo
			label.pack(expand=1, fill=BOTH)

		# updates node degree graph if tab is pressed again
		elif hasattr(self, 'frameOrWindow') and self.frameOrWindow == 0:
			self.nodeDegreeFrame.destroy()
			self.nodeDegrees()
		
		elif hasattr(self, 'frameOrWindow') and self.frameOrWindow == 1:
			self.nodeDegreePopup.destroy()
			self.nodeDegrees()

	# destroys either the node frame or popup when exit button is pressed
	def analysisExit(self):
		if self.frameOrWindow == 0:
			self.nodeDegreeFrame.destroy()
		else:
			self.nodeDegreePopup.destroy()
	
	# docks node popup window into a frame or minimizes frame into just the toolbar when minimize button is pressed
	def analysisMin(self):
		if self.frameOrWindow == 1:
			self.nodeDegreePopup.destroy()
			self.nodeDegrees()
		else:
			self.nodeDegreeFrame.config(height='30')
			self.nodeDegreeFrame.pack_configure(anchor='sw', fill='none')
	
	# maximizes toolbar into a docked frame or maximizes frame into a popup window when maximize button is pressed
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

			# create a frame that makes the toolbar for min, max, and exit buttons
			analysisToolbar = Frame(self.nodeDegreePopup, bg='light gray')
			analysisToolbar.pack(side='top', fill='x')
			analysisToolbar.bind('<ButtonPress-1>', self.dragWindowStart)
			analysisToolbar.bind('<ButtonRelease-1>', lambda event: self.dragWindowEnd(event, self.nodeDegreePopup))

			# toolbar label
			analysisToolbarLabel = Label(analysisToolbar, text="Node Degrees", bg='light gray')
			analysisToolbarLabel.pack(side='left')

			# creates images for toolbar buttons
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
			
			# save the matplotlib plot and open it as a PhotoImage
			fig.savefig("histogramplot.png", bbox_inches='tight')
			image = Image.open("histogramplot.png")
			photo = ImageTk.PhotoImage(image)

			# make label to display image in
			label = Label(self.nodeDegreePopup, image=photo, bg="white")
			label.image = photo
			label.pack()

		elif self.nodeDegreeFrame.winfo_height() == 30:
			self.nodeDegreeFrame.config(height=200)
			self.nodeDegreeFrame.pack_configure(anchor='nw', fill='y')
	"""----------------------------------------------------END NODE DEGREE ANALYSIS-------------------------------------------------------"""
	
	# drags popup window to mouse location upon key press release for node degrees and log window
	def dragWindowStart(self, event):
		self.startDragX = event.x
		self.startDragY = event.y
	
	def dragWindowEnd(self, event, window):
		w = window
		s = w.geometry()
		geometry = s.split('+')
		x = int(geometry[1])+event.x-self.startDragX
		y = int(geometry[2])+event.y-self.startDragY
		# drag window to release button location unless it is out of bounds, then drag window to respective edge of screen
		if x > 0 and y > 0:
			w.geometry(("%dx%d%+d%+d" % (600, 550, x, y)))
		elif x > 0 and y < 0:
			w.geometry(("%dx%d%+d%+d" % (600, 550, x, 0)))
		elif x < 0 and y > 0:
			w.geometry(("%dx%d%+d%+d" % (600, 550, 0, y)))
		else:
			w.geometry(("%dx%d%+d%+d" % (600, 550, 0, 0)))

	"""---------------------------------------------------------LOG WINDOW----------------------------------------------------------------"""
	# add events to the log text
	def appendLog(self, text):
		# if log frame was exited out / it doesn't exist, just keep track of new logs
		# in a string called self.logContents
		if (not hasattr(self, 'logFrame') or  not self.logFrame.winfo_exists()) and \
		   (not hasattr(self, 'logPopUp') or self.logPopUp.winfo_exists() == 0) :
			self.logContents += text

		# if the log frame is in the regular docked state, append text there
		elif self.logFrameOrWindow == 0:
			self.logText.config(state=NORMAL)
			self.logText.insert(END, "\n" + text)
			self.logText.config(state=DISABLED)
			self.logText.see("end")

		# else the log frame is a popup; append text there
		else:
			self.logPopUpText.config(state=NORMAL)
			self.logPopUpText.insert(END, "\n" + text)
			self.logPopUpText.config(state=DISABLED)
			self.logPopUpText.see("end")

	# log window to display all actions done on gui	
	def logWindow(self):
		if (not hasattr(self, 'logFrame') or  not self.logFrame.winfo_exists()) and \
		   (not hasattr(self, 'logPopUp') or self.logPopUp.winfo_exists() == 0) :
			self.logFrameOrWindow = 0
			self.logFrame = Frame(self.parent, height=200, width=200, bg='white', borderwidth=3, relief='raised')
			self.logFrame.pack_propagate(0)
			self.logFrame.pack(side='left', anchor='nw', fill='y')

			self.logToolbar = Frame(self.logFrame, bg='light gray')
			self.logToolbar.pack(side='top', fill='x')

			# toolbar label
			logLabel = Label(self.logToolbar, text="Log", bg='light gray')
			logLabel.pack(side='left')

			# create images for min/max/exit buttons
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
	
	# destroy frame or popup window when exit button is pressed
	def logExit(self):
		if self.logFrameOrWindow == 0:
			self.logContents = self.logText.get('1.0', END)
			self.logFrame.destroy()
		else:
			self.logContents = self.logPopUpText.get('1.0',END)
			self.logPopUp.destroy()

	# docks node popup window into a frame or minimizes frame into just the toolbar when minimize button is pressed
	def logMin(self):
		if self.logFrameOrWindow == 0:
			self.logFrame.config(height='30')
			self.logFrame.pack_configure(anchor='sw', fill='none')
		else:
			contents = self.logPopUpText.get('1.0', END)
			self.logPopUp.destroy()
			self.logWindow()

			self.logText.config(state=NORMAL)
			self.logText.insert(END, contents)
			self.logText.config(state=DISABLED)
			self.logText.see("end")

	# maximizes toolbar into a docked frame or maximizes frame into a popup window when maximize button is pressed
	def logMax(self):
		if self.logFrameOrWindow == 0 and self.logFrame.winfo_height() > 30:
			contents = self.logText.get('1.0', END)
			self.logFrame.destroy()
			
			self.logFrameOrWindow = 1
			self.logPopUp = Toplevel(self.parent, bg='white', bd=2, relief=RIDGE)
			self.logPopUp.overrideredirect(1)
			self.logPopUp.geometry(("%dx%d%+d%+d" % (600, 550, 200, 100)))

			# creates toolbar for log pop up window
			logPopUpToolbar = Frame(self.logPopUp, height=25, width=600, bg='light gray')
			logPopUpToolbar.pack_propagate(0)
			logPopUpToolbar.pack(side='top')
			logPopUpToolbar.bind('<ButtonPress-1>', self.dragWindowStart)
			logPopUpToolbar.bind('<ButtonRelease-1>', lambda event: self.dragWindowEnd(event, self.logPopUp))

			logPopUpLabel = Label(logPopUpToolbar, text="Log", bg='light gray')
			logPopUpLabel.pack(side='left')

			# creates images for min, exit buttons on toolbar
			image = Image.open("exit.png")
			self.exitImage4 = ImageTk.PhotoImage(image)
			exitButton = Button(logPopUpToolbar, image=self.exitImage4, highlightbackground='light gray', command=self.logExit)
			image = Image.open("minimize.png")
			self.minImage4 = ImageTk.PhotoImage(image)
			minButton = Button(logPopUpToolbar, image=self.minImage4, highlightbackground='light gray', command=self.logMin)

			exitButton.pack(side='right')
			minButton.pack(side='right')
			
			# creates scrollbar
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
			self.logFrame.pack_configure(anchor='nw', fill='y')

	''' -----------------------------------------------------END LOG WINDOW-----------------------------------------------------'''



	''' ----------------------------------------------------SUB NETWORK---------------------------------------------------------'''
	# determines x, y, location of a node in order to be equally spaced out in a circle
	def drawPoint(self, r, currPointIndex, totalNumPoints, centerX, centerY):
		theta = (math.pi * 2) / totalNumPoints
		angle = theta * currPointIndex

		x = r * math.cos(angle) + centerX
		y = r * math.sin(angle) + centerY
		return [x, y]
	
	# determines if 2 cubes are touching or overlapping
	def adjacency(self, x1, x2, y1, y2, z1, z2, a1, a2):
		EPSILON = .001
		return math.fabs(x1-x2)-(a1+a2) <= EPSILON and math.fabs(y1-y2)-(a1+a2) <= EPSILON and math.fabs(z1-z2)-(a1+a2) <= EPSILON

	# frame that displays a network of a node's advanced geometry, edges represent cubes are touching/overlapping
	def showSubNetwork(self, node):
		self.selectedNode = node
		if (not hasattr(self, 'subNetworkFrame') or not self.subNetworkFrame.winfo_exists()) and \
		   (not hasattr(self, 'subNetworkPopUp') or self.subNetworkPopUp.winfo_exists() == 0) :

			self.SubNeworkFrameOrWindow = 0 #0 is docked frame, 1 is pop up window
			
			self.subNetworkFrame = Frame(self.parent, height=200, width=200, bg='white', borderwidth=3, relief='raised')
			self.subNetworkFrame.pack_propagate(0)
			self.subNetworkFrame.pack(side='left', anchor='nw', fill='y')

			# toolbar to store max, min, exit buttons
			self.subNetworktoolbar = Frame(self.subNetworkFrame, bg='light gray')
			self.subNetworktoolbar.pack(side='top', fill='x')
			subNetworkLabel = Label(self.subNetworktoolbar, text="Sub-Network", bg='light gray')
			subNetworkLabel.pack(side='left')

			self.frameCanvas = Canvas(self.subNetworkFrame, width=200, height=180, bg='white')
			self.frameCanvas.pack(side='bottom')

			image = Image.open("exit.png") 
			self.exitImage5 = ImageTk.PhotoImage(image)
			exitButton = Button(self.subNetworktoolbar, image=self.exitImage5, highlightbackground='light gray', command=self.subNetworkExit)
			image = Image.open("minimize.png")
			self.minImage5 = ImageTk.PhotoImage(image)
			minButton = Button(self.subNetworktoolbar, image=self.minImage5, highlightbackground='light gray', command=self.subNetworkMin)
			image = Image.open("maximize.png")
			self.maxImage5 = ImageTk.PhotoImage(image)
			maxButton = Button(self.subNetworktoolbar, image=self.maxImage5, highlightbackground='light gray', command=self.subNetworkMax)

			exitButton.pack(side='right')
			maxButton.pack(side='right')
			minButton.pack(side='right')

			x = self.G.node[self.selectedNode]['x']
			try: # simple geometry
				int(x)
				r=6
				# create single node in center of frame
				self.frameCanvas.create_oval(100-r, 90-r, 100+r, 90+r, fill='red')
			except TypeError: # advanced geometry
				for i in range(0, len(x)):
					coord = self.drawPoint(50, i, len(x), 100, 75)
					r=6
					# for n number of nodes, draw n nodes spaced equally apart
					self.frameCanvas.create_oval(coord[0]-r, coord[1]-r, coord[0]+r, coord[1]+r, fill='red')
					self.frameCanvas.create_text(coord[0], coord[1], text=str(i+1), fill='white')
				for i in range(0, len(x)):
					for j in range(i, len(x)):
						if i != j:
							# checks adjacency for every combination of 2 cubes in the adv geometry 
							x1 = self.G.node[self.selectedNode]['x'][i]
							x2 = self.G.node[self.selectedNode]['x'][j]
							y1 = self.G.node[self.selectedNode]['y'][i]
							y2 = self.G.node[self.selectedNode]['y'][j]
							z1 = self.G.node[self.selectedNode]['z'][i]
							z2 = self.G.node[self.selectedNode]['z'][j]
							a1 = self.G.node[self.selectedNode]['EdgeLength'][i]/2
							a2 = self.G.node[self.selectedNode]['EdgeLength'][j]/2
							adj = self.adjacency(x1, x2, y1, y2, z1, z2, a1, a2)
							if adj:
								# if 2 cubes are adjacent, create an edge between them in the docked frame
								x1 = (self.frameCanvas.coords(i*2+1)[0]+self.frameCanvas.coords(i*2+1)[2])/2
								x2 = (self.frameCanvas.coords(j*2+1)[0]+self.frameCanvas.coords(j*2+1)[2])/2
								y1 = (self.frameCanvas.coords(i*2+1)[1]+self.frameCanvas.coords(i*2+1)[3])/2
								y2 = (self.frameCanvas.coords(j*2+1)[1]+self.frameCanvas.coords(j*2+1)[3])/2
								self.frameCanvas.create_line(x1, y1, x2, y2, fill='black')


		# updates node degree graph if tab is pressed again
		elif hasattr(self, 'SubNeworkFrameOrWindow') and self.SubNeworkFrameOrWindow == 0:
			self.subNetworkFrame.destroy()
			self.showSubNetwork(self.selectedNode)
		
		# deletes popUp and updates node degree graph if tab is pressed again
		elif hasattr(self, 'SubNeworkFrameOrWindow') and self.SubNeworkFrameOrWindow == 1:
			self.subNetworkPopUp.destroy()
			self.showSubNetwork(self.selectedNode)
	
	# exits either the subNetwork docked frame or pop up window
	def subNetworkExit(self):
		if self.SubNeworkFrameOrWindow == 0:
			self.subNetworkFrame.destroy()
		else:
			self.subNetworkPopUp.destroy()
	
	# maximizes the toolbar into a docked frame, and a docked frame into a pop up window
	def subNetworkMax(self):
		if self.SubNeworkFrameOrWindow == 0 and self.subNetworkFrame.winfo_height() > 30:
			self.subNetworkFrame.destroy()

			# creates pop up window
			self.SubNeworkFrameOrWindow = 1
			self.subNetworkPopUp = Toplevel(self.parent, bg='white')
			self.subNetworkPopUp.title("Node Degrees")
			self.subNetworkPopUp.overrideredirect(1)
			self.subNetworkPopUp.geometry(("%dx%d%+d%+d" % (600, 550, 200, 100)))

			# creates toolbar for min, exit buttons
			popUpToolbar = Frame(self.subNetworkPopUp, bg='light gray')
			popUpToolbar.pack(side='top', fill='x')
			popUpToolbar.bind('<ButtonPress-1>', self.dragWindowStart)
			popUpToolbar.bind('<ButtonRelease-1>', lambda event: self.dragWindowEnd(event, self.subNetworkPopUp))

			# toolbar label
			subNetworkLabel = Label(self.popUpToolbar, text="Sub-Network", bg='light gray')
			subNetworkLabel.pack(side='left')

			self.PopUpCanvas = Canvas(self.subNetworkPopUp, width=600, height=520, bg='white')
			self.PopUpCanvas.pack(side='bottom')

			# creates images for toolbar buttons
			image = Image.open("exit.png")
			self.exitImage6 = ImageTk.PhotoImage(image)
			exitButton = Button(popUpToolbar, image=self.exitImage6, highlightbackground='light gray', command=self.subNetworkExit)
			image = Image.open("minimize.png")
			self.minImage6 = ImageTk.PhotoImage(image)
			minButton = Button(popUpToolbar, image=self.minImage6, highlightbackground='light gray', command=self.subNetworkMin)

			exitButton.pack(side='right')
			minButton.pack(side='right')

			x = self.G.node[self.selectedNode]['x']
			try: # simple geometry
				int(x)
				r=10
				# for n number of nodes, draw n nodes spaced equally apart
				self.PopUpCanvas.create_oval(300-r, 260-r, 300+r, 260+r, fill='red')
			except TypeError: # advanced geometry
				for i in range(0, len(x)):
					coord = self.drawPoint(200, i, len(x), 300, 260)
					r=10
					self.PopUpCanvas.create_oval(coord[0]-r, coord[1]-r, coord[0]+r, coord[1]+r, fill='red')
					self.PopUpCanvas.create_text(coord[0], coord[1], text=str(i+1), fill='white')
				for i in range(0, len(x)):
					for j in range(i, len(x)):
						if i != j:
							# checks adjacency for every combination of 2 cubes in the adv geometry 
							x1 = self.G.node[self.selectedNode]['x'][i]
							x2 = self.G.node[self.selectedNode]['x'][j]
							y1 = self.G.node[self.selectedNode]['y'][i]
							y2 = self.G.node[self.selectedNode]['y'][j]
							z1 = self.G.node[self.selectedNode]['z'][i]
							z2 = self.G.node[self.selectedNode]['z'][j]
							a1 = self.G.node[self.selectedNode]['EdgeLength'][i]/2
							a2 = self.G.node[self.selectedNode]['EdgeLength'][j]/2
							adj = self.adjacency(x1, x2, y1, y2, z1, z2, a1, a2)
							if adj:
								# if 2 cubes are adjacent, create an edge between them in the pop up window
								x1 = (self.PopUpCanvas.coords(i*2+1)[0]+self.PopUpCanvas.coords(i*2+1)[2])/2
								x2 = (self.PopUpCanvas.coords(j*2+1)[0]+self.PopUpCanvas.coords(j*2+1)[2])/2
								y1 = (self.PopUpCanvas.coords(i*2+1)[1]+self.PopUpCanvas.coords(i*2+1)[3])/2
								y2 = (self.PopUpCanvas.coords(j*2+1)[1]+self.PopUpCanvas.coords(j*2+1)[3])/2
								self.PopUpCanvas.create_line(x1, y1, x2, y2, fill='black')

		# maximizes a toolbar into a docked frame
		elif self.subNetworkFrame.winfo_height() == 30:
			self.subNetworkFrame.config(height=200)
			self.subNetworkFrame.pack_configure(anchor='nw', fill='y')
	
	# minimizes a pop up window into a docked frame, and a docked frame into a toolbar
	def subNetworkMin(self):
		if self.SubNeworkFrameOrWindow == 1:
			self.subNetworkPopUp.destroy()
			self.showSubNetwork(self.selectedNode)
		else:
			self.subNetworkFrame.config(height='30')
			self.subNetworkFrame.pack_configure(anchor='sw', fill='none')
	"""----------------------------------------------------END SUB NETWORK-------------------------------------------------------"""
	
	def initUI(self):
		self.logWindow()

