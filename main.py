from Tkinter import *
from frontendLeft import *

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        # create main frame, divided into two panels
        # create main toolbar
        # call frontend, which will fill in each panel
        pass



def main():
    root = Tk()
    app = Window(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
