from Tkinter import *
import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

class DockedWindows(Frame):
	def __init__(self, parent, G):
		Frame.__init__(self, parent)

		self.parent = parent
		self.G = G

		self.initUI()

	def nodeDegrees(self):
		if len(self.G.nodes()) > 0 and \
		  (not hasattr(self, 'nodeDegreeFrame') or self.nodeDegreeFrame.winfo_exists() == 0) and \
		  (not hasattr(self, 'nodeDegreePopup') or self.nodeDegreePopup.winfo_exists() == 0):
			# mini frame to display node degree analysis graph:
			self.frameOrWindow = 0 # 0 - frame, 1 - popup window
			self.nodeDegreeFrame = Frame(self.parent, height=200, width=200, bg='white', borderwidth=3, relief='raised')
			self.nodeDegreeFrame.pack_propagate(0)
			self.nodeDegreeFrame.pack(side='left', anchor='sw')

			# toolbar to store max, min, exit buttons
			self.toolbarFrame = Frame(self.nodeDegreeFrame, bg='light gray')
			self.toolbarFrame.pack(side='top', fill='x')

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
		if (not hasattr(self, 'logFrame') or  not self.logFrame.winfo_exists()) and \
		   (not hasattr(self, 'logPopUp') or self.logPopUp.winfo_exists() == 0) :
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
		if (not hasattr(self, 'logFrame') or  not self.logFrame.winfo_exists()) and \
		   (not hasattr(self, 'logPopUp') or self.logPopUp.winfo_exists() == 0) :
			self.logFrameOrWindow = 0
			self.logFrame = Frame(self.parent, height=200, width=200, bg='white', borderwidth=3, relief='raised')
			self.logFrame.pack_propagate(0)
			self.logFrame.pack(side='left', anchor='sw')

			self.logToolbar = Frame(self.logFrame, bg='light gray')
			self.logToolbar.pack(side='top', fill='x')

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


	def initUI(self):
		self.logWindow()
