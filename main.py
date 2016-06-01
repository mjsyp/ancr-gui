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
        self.initUI()

    def onExit(self):
        self.quit()

    def save(self, event=None):
        outFile=open('gui.txt', 'w')
        s=str(self.G.nodes(data=True))
        outFile.write(s)
        outFile.close()

    def save_as(self):
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        pickle.dump(self.G, open('gui.txt', 'w'))
        
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
        geoCanvas = FrontendLeft(self.leftFrame, self.rightFrame, self.G)

        # Main Menubar
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileTab = Menu(menubar)
        fileTab.add_command(label="Open...", accelerator="Command-O")
        fileTab.add_command(label="Save", command=self.save, accelerator="Command-S")
        fileTab.add_command(label="Save As...", command=self.save_as)
        fileTab.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileTab)

        editTab = Menu(menubar)
        editTab.add_command(label="Undo", command=geoCanvas.undo, accelerator="Command-Z")
        menubar.add_cascade(label="Edit", menu=editTab)

        viewTab = Menu(menubar)
        viewTab.add_command(label="View Labels")
        menubar.add_cascade(label="View", menu=viewTab)

        analysisTab = Menu(menubar)
        analysisTab.add_command(label="Node Degrees", command=geoCanvas.nodeDegrees)
        menubar.add_cascade(label="Analysis", menu=analysisTab)

        self.parent.bind('<Control-z>', geoCanvas.undo)
        self.parent.bind('<Command-z>', geoCanvas.undo)
        self.parent.bind('<Control-s>', self.save)
        self.parent.bind('<Command-s>', self.save)


def main():
    root = Tk()
    app = Window(root)
    root.mainloop()  
    #to see the networkx representation of the graph after exiting the gui:
    #nx.draw(app.G)
    #plt.show()


if __name__ == '__main__':
    main()
    


