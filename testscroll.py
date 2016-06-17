from Tkinter import *


class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
         
        self.parent = parent
        self.initUI()



    def initUI(self):
        self.parent.title("GUI")

        # Create left and right frames
        self.leftFrame = Frame(self.parent, height=600, width=700, bg='light blue') #light colored bg to see panel
        self.rightFrame = Frame(self.parent, bg="dark gray", height=600, width=300) #dark colored bg to see panel

        self.leftFrame.pack(side="left", fill="both", expand=1)
        self.leftFrame.pack_propagate(0)
        self.rightFrame.pack(side="right", fill="y", expand=0)
        self.rightFrame.pack_propagate(0)
        
        self.canvas = Canvas(self.rightFrame)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(self.rightFrame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", expand=True)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):
        for row in range(50):
            Label(self.frame, text=row).grid(row=row, column=0)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=300, height=600)
        


def main():
	root = Tk()
	app = Window(root)
	root.mainloop()


if __name__ == '__main__':
    main()
    
