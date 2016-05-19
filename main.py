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
        # TODO: create main frame, divided into two panels
        #       create main toolbar
        #       call frontendLeft/frontendRight, which will fill in each panel

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
        self.leftFrame = Frame(self.parent, bg="black", height=600, width=600) #colored background to see structure of frames
        self.rightFrame = Frame(self.parent, bg="gray", height=600, width=300)

        self.leftFrame.pack(side="left", fill="both", expand=1)
        self.rightFrame.pack(side="right", fill="both", expand=1)



def main():
    root = Tk()
    app = Window(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
