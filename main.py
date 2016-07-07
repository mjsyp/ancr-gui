from Tkinter import *
from CanvasFrame import *
import networkx as nx
import tkFileDialog
import pickle
from sys import platform as _platform
#import matplotlib.pyplot as plt

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
         
        self.parent = parent
        self.G = nx.DiGraph()
        self.D = nx.DiGraph()
        self.initUI()

    # exits out of gui when clicked on 
    def exit(self):
        self.quit()

    # will update saved file if 
    def save(self, event=None):
        if hasattr(self, 'filename'):
            pickle.dump(self.G, open(str(self.filename), 'w'))
        else:
            self.save_as()

    # can save network x graph (node/edges and attributes) as any type of text file
    def save_as(self):
        for node in self.G.nodes():
            self.G.node[node]['systems'] = self.geoCanvas.manager.systems
        self.filename = tkFileDialog.asksaveasfilename(defaultextension=".txt")
        if self.filename == '': # asksaveasfile return `None` if dialog closed with "cancel".
            return
        else:
			pickle.dump(self.G, open(str(self.filename), 'w'))

    # can open any previously saved network x graph and plot nodes and edges onto the canvas, and resume all gui functionality 
    def open(self):
        f = tkFileDialog.askopenfilename()
        if f == '':
            return
        else:
            self.G = pickle.load(open(str(f)))
            self.G = nx.convert_node_labels_to_integers(self.G, first_label=1)
            for widget in self.leftFrame.winfo_children():
                widget.destroy()
            self.geoCanvas = CanvasFrame(self.leftFrame, self.rightCanvasFrame, self.G, self.D)
            self.createTabs()

            # redraw nodes
            for nodeNum in self.G.nodes():
                r = 8
                self.geoCanvas.systemsCanvas.create_oval(self.G.node[nodeNum]['x_coord']-r, self.G.node[nodeNum]['y_coord']-r, self.G.node[nodeNum]['x_coord']+r, self.G.node[nodeNum]['y_coord']+r, fill='red', tag='node') 
            
            # redraw edges
            for startNode, endNode in self.G.edges():
                edgeItem=self.geoCanvas.systemsCanvas.create_line(self.G.edge[startNode][endNode]['x1_coord'], self.G.edge[startNode][endNode]['y1_coord'], self.G.edge[startNode][endNode]['x2_coord'], self.G.edge[startNode][endNode]['y2_coord'], tag='edge')
                self.geoCanvas.systemsCanvas.addtag_withtag(str(startNode), edgeItem)
                self.geoCanvas.systemsCanvas.addtag_withtag(str(endNode), edgeItem)
                self.G.edge[startNode][endNode]['edgeID'] = edgeItem
            
            # reload demands
            self.geoCanvas.manager.systems = self.G.node[1]['systems']
            for key in self.geoCanvas.manager.systems:
                self.geoCanvas.optionList.insert(len(self.geoCanvas.optionList)-2, key)
                self.geoCanvas.dropdown.destroy()
                self.geoCanvas.dropdown = OptionMenu(self.geoCanvas.toolbar, self.geoCanvas.v, *self.geoCanvas.optionList, command=self.geoCanvas.newOptionMenu)
                self.geoCanvas.dropdown.configure(bg="light blue")
                self.geoCanvas.dropdown.pack(side='left')

                
    # creates the gui menubar
    def createTabs(self):
        # MAIN MENUBAR
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # File Tab
        fileTab = Menu(menubar)
        fileTab.add_command(label="Open...", accelerator="Command-O", command=self.open)
        fileTab.add_command(label="Save", command=self.save, accelerator="Command-S")
        fileTab.add_command(label="Save As...", command=self.save_as)
        fileTab.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=fileTab)

        # Edit Tab
        editTab = Menu(menubar)
        editTab.add_command(label="Undo", command=self.geoCanvas.undo, accelerator="Command-Z")
        editTab.add_command(label="Redo", command=self.geoCanvas.redo, accelerator="Command-Shift-Z")
        menubar.add_cascade(label="Edit", menu=editTab)

        #View Tab
        viewTab = Menu(menubar)
        viewTab.add_command(label="Show Labels", command=self.geoCanvas.showLabels)
        viewTab.add_command(label="Hide Labels", command=self.geoCanvas.hideLabels)
        viewTab.add_command(label='Log Window', command=self.geoCanvas.logWindow)
        menubar.add_cascade(label="View", menu=viewTab)

        #Analysis Tab
        analysisTab = Menu(menubar)
        analysisTab.add_command(label="Node Degrees", command=self.geoCanvas.nodeDegrees)
        menubar.add_cascade(label="Analysis", menu=analysisTab)

        #Binds submenus to their shortcut key
        self.parent.bind('<Control-z>', self.geoCanvas.undo)
        self.parent.bind('<Command-z>', self.geoCanvas.undo)
        self.parent.bind('<Control-Z>', self.geoCanvas.redo)
        self.parent.bind('<Command-Z>', self.geoCanvas.redo)
        self.parent.bind('<Control-s>', self.save)
        self.parent.bind('<Command-s>', self.save)

    def initUI(self):

        self.parent.title("GUI")

        # Create left and right frames and packs them within the parent frame
        self.leftFrame = Frame(self.parent, bg='light blue', height=700, width=700) #light colored bg to see panel
        if _platform == "win32":
        	self.rightFrame = Frame(self.parent, bg="dark gray", height=700, width=290) #dark colored bg to see panel
        else:
        	self.rightFrame = Frame(self.parent, bg="dark gray", height=700, width=340)


        self.leftFrame.pack(side="left", fill="both", expand=1)
        self.leftFrame.pack_propagate(0)
        self.rightFrame.pack(side="right", fill="y", expand=0)
        self.rightFrame.pack_propagate(0)
        
        # Creates a scrollbar on the right frame and corresponding window which it controls
        self.rightSideCanvas = Canvas(self.rightFrame, height=700, width=300, bg='dark gray', highlightbackground='dark gray')
        self.rightCanvasFrame = Frame(self.rightSideCanvas, bg='dark gray')
        self.vsb = Scrollbar(self.rightFrame, orient="vertical", command=self.rightSideCanvas.yview)
        self.rightSideCanvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.rightSideCanvas.pack(side="left", expand=True)
        self.rightSideCanvas.create_window((0,0), window=self.rightCanvasFrame, anchor="nw")



        # Use CanvasFrame to fill left frame
        self.geoCanvas = CanvasFrame(self.leftFrame, self.rightCanvasFrame, self.G, self.D)

        # enables scrollbar functionality 
        self.rightCanvasFrame.bind("<Configure>", self.onFrameConfigure)

        self.createTabs()

    # set the right frame window to match the scroll bar configure
    def onFrameConfigure(self, event):
        self.rightSideCanvas.configure(scrollregion=self.rightSideCanvas.bbox("all"), width=300, height=700)


def main():
    root = Tk()
    app = Window(root)
    root.mainloop()
    #to see the networkx representation of the graph after exiting the gui:
    #nx.draw(app.G)
    #plt.show()


if __name__ == '__main__':
    main()
    


