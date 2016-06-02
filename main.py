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

    def exit(self):
        self.quit()

    def save(self):
        # saves all networkX info in a text file called 'gui.txt' in current working directory
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

        # MAIN MENUBAR
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # File Tab
        fileTab = Menu(menubar)
        fileTab.add_command(label="Open...")
        fileTab.add_command(label="Save", command=self.save)
        fileTab.add_command(label="Save As...", command=self.save_as)
        fileTab.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=fileTab)

        # Edit Tab
        editTab = Menu(menubar)
        editTab.add_command(label="Undo", command=geoCanvas.undo)
        menubar.add_cascade(label="Edit", menu=editTab)

        self.parent.bind('<Control-z>', geoCanvas.undo)
        self.parent.bind('<Command-z>', geoCanvas.undo)

def main():
    root = Tk()
    app = Window(root)
    root.mainloop()  
    #to see the networkx representation of the graph after exiting the gui:
    #nx.draw(app.G)
    #plt.show()


if __name__ == '__main__':
    main()
    


