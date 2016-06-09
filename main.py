from Tkinter import *
from frontendLeft import *
from frontendRight import *
import networkx as nx
import tkFileDialog
import pickle
#import matplotlib.pyplot as plt

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
         
        self.parent = parent
        self.G = nx.DiGraph()
        self.D = nx.DiGraph()
        self.initUI()

    def exit(self):
        self.quit()

    def save(self, event=None):
        outFile=open('gui.txt', 'w')
        s=str(self.G.nodes(data=True))
        outFile.write(s)
        outFile.close()

    def save_as(self):
        f = tkFileDialog.asksaveasfilename(defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        else:
            pickle.dump(self.G, open(str(f), 'w'))

    def open(self):
        f = tkFileDialog.askopenfilename()
        if f is None:
            return
        else:
            self.G = pickle.load(open(str(f)))
            self.G = nx.convert_node_labels_to_integers(self.G, first_label=1)
            for widget in self.leftFrame.winfo_children():
                widget.destroy()
            self.geoCanvas = FrontendLeft(self.leftFrame, self.rightFrame, self.G, self.D)
            self.createTabs()
            for nodeNum in self.G.nodes():
                r = 8
                self.geoCanvas.systemsCanvas.create_oval(self.G.node[nodeNum]['x_coord']-r, self.G.node[nodeNum]['y_coord']-r, self.G.node[nodeNum]['x_coord']+r, self.G.node[nodeNum]['y_coord']+r, fill='red', tag='node') 
            for startNode, endNode in self.G.edges():
                edgeItem=self.geoCanvas.systemsCanvas.create_line(self.G.edge[startNode][endNode]['x1_coord'], self.G.edge[startNode][endNode]['y1_coord'], self.G.edge[startNode][endNode]['x2_coord'], self.G.edge[startNode][endNode]['y2_coord'], tag='edge')
                self.geoCanvas.systemsCanvas.addtag_withtag(str(startNode), edgeItem)
                self.geoCanvas.systemsCanvas.addtag_withtag(str(endNode), edgeItem)
            for key in self.G.node[1]:
                if key == 'Name' or key == 'y_coord' or key == 'x_coord' or key == 'x' or key == 'y' or key == 'z' or key == 'Type' or key == 'Notes':
                    pass
                else:
                    self.geoCanvas.optionList.insert(len(self.geoCanvas.optionList)-2, key)
                    self.geoCanvas.dropdown.destroy()
                    self.geoCanvas.dropdown = OptionMenu(self.geoCanvas.toolbar, self.geoCanvas.v, *self.geoCanvas.optionList, command=self.geoCanvas.newOptionMenu)
                    self.geoCanvas.dropdown.configure(bg="light blue")
                    self.geoCanvas.dropdown.pack(side='left')


                
            


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

        # Create left and right frames
        self.leftFrame = Frame(self.parent, height=600, width=700, bg='light blue') #light colored bg to see panel
        self.rightFrame = Frame(self.parent, bg="dark gray", height=600, width=300) #dark colored bg to see panel

        self.leftFrame.pack(side="left", fill="both", expand=1)
        self.leftFrame.pack_propagate(0)
        self.rightFrame.pack(side="right", fill="y", expand=0)
        self.rightFrame.pack_propagate(0)

        # Use frontendLeft to fill left frame
        self.geoCanvas = FrontendLeft(self.leftFrame, self.rightFrame, self.G, self.D)

        self.createTabs()


def main():
    root = Tk()
    app = Window(root)
    root.mainloop()  
    #to see the networkx representation of the graph after exiting the gui:
    #nx.draw(app.G)
    #plt.show()


if __name__ == '__main__':
    main()
    


