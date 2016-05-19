from Tkinter import *
from frontendLeft import *

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()

    def onExit(self):
        self.quit()
        
    def initUI(self):
        # TODO:  X  create main frame, divided into two panels
        #        X  create main toolbar
        #           call frontendLeft/frontendRight, which will fill in each panel

        self.parent.title("GUI")

        # Main Menubar
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileTab = Menu(menubar)
        fileTab.add_command(label="Open...")
        fileTab.add_command(label="Save")
        fileTab.add_command(label="Save As...")
        fileTab.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileTab)


        # Create left and right frames
        self.leftFrame = Frame(self.parent, height=600, width=600) 
        self.rightFrame = Frame(self.parent, bg="gray", height=600, width=300) #colored bg to see panels

        self.leftFrame.pack(side="left", fill="both", expand=1)
        self.leftFrame.pack_propagate(0)
        self.rightFrame.pack(side="right", fill="both", expand=1)


        # Use frontendLeft to fill left frame (TODO)
        geoCanvas = FrontendLeft(self.leftFrame)



def main():
    root = Tk()
    app = Window(root)
    root.mainloop()  


if __name__ == '__main__':
    main()


